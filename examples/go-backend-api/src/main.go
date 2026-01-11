package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	_ "github.com/lib/pq"
)

// User represents a user in the system
type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// Server holds dependencies
type Server struct {
	db *sql.DB
	mux *http.ServeMux
}

// NewServer creates a new server with dependencies
func NewServer(db *sql.DB) *Server {
	s := &Server{
		db:  db,
		mux: http.NewServeMux(),
	}
	s.setupRoutes()
	return s
}

// setupRoutes registers all HTTP handlers
func (s *Server) setupRoutes() {
	s.mux.HandleFunc("GET /users", s.ListUsers)
	s.mux.HandleFunc("GET /users/{id}", s.GetUser)
	s.mux.HandleFunc("POST /users", s.CreateUser)
	s.mux.HandleFunc("DELETE /users/{id}", s.DeleteUser)
}

// ListUsers returns all users
func (s *Server) ListUsers(w http.ResponseWriter, r *http.Request) {
	rows, err := s.db.QueryContext(r.Context(), "SELECT id, name, email FROM users ORDER BY id")
	if err != nil {
		http.Error(w, "Failed to query users", http.StatusInternalServerError)
		log.Printf("Query error: %v", err)
		return
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Name, &u.Email); err != nil {
			http.Error(w, "Failed to scan user", http.StatusInternalServerError)
			log.Printf("Scan error: %v", err)
			return
		}
		users = append(users, u)
	}

	if err := rows.Err(); err != nil {
		http.Error(w, "Error iterating users", http.StatusInternalServerError)
		log.Printf("Rows error: %v", err)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(users)
}

// GetUser returns a single user by ID
func (s *Server) GetUser(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid user ID", http.StatusBadRequest)
		return
	}

	var u User
	err = s.db.QueryRowContext(r.Context(),
		"SELECT id, name, email FROM users WHERE id = $1",
		id,
	).Scan(&u.ID, &u.Name, &u.Email)

	if err == sql.ErrNoRows {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}
	if err != nil {
		http.Error(w, "Failed to query user", http.StatusInternalServerError)
		log.Printf("Query error: %v", err)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(u)
}

// CreateUser creates a new user
func (s *Server) CreateUser(w http.ResponseWriter, r *http.Request) {
	var input struct {
		Name  string `json:"name"`
		Email string `json:"email"`
	}

	if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Basic validation
	if input.Name == "" || input.Email == "" {
		http.Error(w, "Name and email are required", http.StatusBadRequest)
		return
	}

	var u User
	err := s.db.QueryRowContext(r.Context(),
		"INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email",
		input.Name, input.Email,
	).Scan(&u.ID, &u.Name, &u.Email)

	if err != nil {
		http.Error(w, "Failed to create user", http.StatusInternalServerError)
		log.Printf("Insert error: %v", err)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(u)
}

// DeleteUser deletes a user by ID
func (s *Server) DeleteUser(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid user ID", http.StatusBadRequest)
		return
	}

	result, err := s.db.ExecContext(r.Context(),
		"DELETE FROM users WHERE id = $1",
		id,
	)
	if err != nil {
		http.Error(w, "Failed to delete user", http.StatusInternalServerError)
		log.Printf("Delete error: %v", err)
		return
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		http.Error(w, "Failed to get affected rows", http.StatusInternalServerError)
		return
	}

	if rowsAffected == 0 {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// initDB initializes the database connection and schema
func initDB(databaseURL string) (*sql.DB, error) {
	db, err := sql.Open("postgres", databaseURL)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// Configure connection pool
	db.SetMaxOpenConns(25)
	db.SetMaxIdleConns(5)
	db.SetConnMaxLifetime(5 * time.Minute)

	// Test connection
	if err := db.Ping(); err != nil {
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	// Create schema if not exists
	schema := `
	CREATE TABLE IF NOT EXISTS users (
		id SERIAL PRIMARY KEY,
		name VARCHAR(255) NOT NULL,
		email VARCHAR(255) NOT NULL UNIQUE,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	`
	if _, err := db.Exec(schema); err != nil {
		return nil, fmt.Errorf("failed to create schema: %w", err)
	}

	return db, nil
}

func main() {
	// Get configuration
	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		databaseURL = "postgres://postgres:postgres@localhost:5432/playbook_db?sslmode=disable"
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Initialize database
	db, err := initDB(databaseURL)
	if err != nil {
		log.Fatalf("Database initialization failed: %v", err)
	}
	defer db.Close()

	// Create server
	server := NewServer(db)

	// HTTP server
	httpServer := &http.Server{
		Addr:         ":" + port,
		Handler:      server.mux,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Handle graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

	go func() {
		sig := <-sigChan
		log.Printf("Received signal: %v", sig)

		ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
		defer cancel()

		if err := httpServer.Shutdown(ctx); err != nil {
			log.Printf("Server shutdown error: %v", err)
		}
	}()

	log.Printf("Starting server on %s", httpServer.Addr)
	if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server error: %v", err)
	}

	log.Println("Server stopped")
}
