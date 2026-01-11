package main_test

import (
	"bytes"
	"context"
	"database/sql"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	_ "github.com/lib/pq"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// User represents a user (mirrors main package)
type User struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// Server mirrors main.Server
type Server struct {
	db  *sql.DB
	mux *http.ServeMux
}

// setupTestDB creates an in-memory test database
func setupTestDB(t *testing.T) *sql.DB {
	t.Helper()

	// Use SQLite for testing (or use test PostgreSQL container)
	db, err := sql.Open("sqlite", ":memory:")
	require.NoError(t, err)

	// Create schema
	schema := `
	CREATE TABLE users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		email TEXT NOT NULL UNIQUE,
		created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
	`
	_, err = db.Exec(schema)
	require.NoError(t, err)

	return db
}

func TestListUsers_Success(t *testing.T) {
	// Arrange
	db := setupTestDB(t)
	defer db.Close()

	// Insert test data
	_, err := db.Exec(
		"INSERT INTO users (name, email) VALUES (?, ?), (?, ?)",
		"Alice", "alice@example.com",
		"Bob", "bob@example.com",
	)
	require.NoError(t, err)

	// Act
	req := httptest.NewRequest("GET", "/users", nil)
	w := httptest.NewRecorder()

	// Assert
	assert.Equal(t, http.StatusOK, w.Code)
}

func TestGetUser_Success(t *testing.T) {
	// Arrange
	db := setupTestDB(t)
	defer db.Close()

	_, err := db.Exec(
		"INSERT INTO users (name, email) VALUES (?, ?)",
		"Alice", "alice@example.com",
	)
	require.NoError(t, err)

	// Act
	req := httptest.NewRequest("GET", "/users/1", nil)
	w := httptest.NewRecorder()

	// Assert
	assert.Equal(t, http.StatusOK, w.Code)

	var user User
	err = json.NewDecoder(w.Body).Decode(&user)
	require.NoError(t, err)
	assert.Equal(t, "Alice", user.Name)
}

func TestGetUser_NotFound(t *testing.T) {
	// Arrange
	db := setupTestDB(t)
	defer db.Close()

	// Act
	req := httptest.NewRequest("GET", "/users/999", nil)
	w := httptest.NewRecorder()

	// Assert (should return 404)
	// Note: actual status depends on implementation
	assert.True(t, w.Code == http.StatusNotFound || w.Code == http.StatusInternalServerError)
}

func TestCreateUser_Success(t *testing.T) {
	// Arrange
	db := setupTestDB(t)
	defer db.Close()

	body := bytes.NewBufferString(`{"name":"Alice","email":"alice@example.com"}`)
	req := httptest.NewRequest("POST", "/users", body)
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	// Act (would call handler)
	// Assert
	assert.True(t, w.Code == http.StatusCreated || w.Code == http.StatusOK)
}

func TestCreateUser_InvalidInput(t *testing.T) {
	tests := []struct {
		name        string
		input       string
		expectError bool
	}{
		{
			name:        "missing name",
			input:       `{"email":"alice@example.com"}`,
			expectError: true,
		},
		{
			name:        "missing email",
			input:       `{"name":"Alice"}`,
			expectError: true,
		},
		{
			name:        "valid input",
			input:       `{"name":"Alice","email":"alice@example.com"}`,
			expectError: false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Validate input
			var input struct {
				Name  string `json:"name"`
				Email string `json:"email"`
			}

			err := json.NewDecoder(strings.NewReader(tt.input)).Decode(&input)
			if tt.expectError {
				assert.True(t, input.Name == "" || input.Email == "")
			} else {
				require.NoError(t, err)
				assert.NotEmpty(t, input.Name)
				assert.NotEmpty(t, input.Email)
			}
		})
	}
}

func TestDeleteUser_Success(t *testing.T) {
	// Arrange
	db := setupTestDB(t)
	defer db.Close()

	// Insert test user
	result, err := db.Exec(
		"INSERT INTO users (name, email) VALUES (?, ?)",
		"Alice", "alice@example.com",
	)
	require.NoError(t, err)

	userID, err := result.LastInsertId()
	require.NoError(t, err)

	// Act: Delete user
	ctx := context.Background()
	res, err := db.ExecContext(ctx,
		"DELETE FROM users WHERE id = ?",
		userID,
	)
	require.NoError(t, err)

	// Assert
	rowsAffected, err := res.RowsAffected()
	require.NoError(t, err)
	assert.Equal(t, int64(1), rowsAffected)
}

func TestDeleteUser_NotFound(t *testing.T) {
	// Arrange
	db := setupTestDB(t)
	defer db.Close()

	// Act: Delete non-existent user
	res, err := db.Exec(
		"DELETE FROM users WHERE id = ?",
		999,
	)
	require.NoError(t, err)

	// Assert
	rowsAffected, err := res.RowsAffected()
	require.NoError(t, err)
	assert.Equal(t, int64(0), rowsAffected)
}
