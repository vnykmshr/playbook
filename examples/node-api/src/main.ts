/**
 * User management API built with Express and TypeScript.
 *
 * This application demonstrates:
 * - Express.js web framework
 * - Type safety with TypeScript
 * - Error handling middleware
 * - Structured logging
 * - Graceful shutdown
 */

import express, { Express, Request, Response, NextFunction } from 'express';
import { Pool, PoolClient } from 'pg';
import Logger from 'pino';
import { v4 as uuidv4 } from 'uuid';

// Types
interface User {
  id: number;
  name: string;
  email: string;
  created_at?: string;
}

interface CreateUserInput {
  name: string;
  email: string;
}

interface ApiError extends Error {
  status: number;
}

// Initialize logger
const logger = Logger();

// Initialize database pool
const pool = new Pool({
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'playbook_db',
});

// Request ID middleware for tracing
function requestIdMiddleware(req: Request, res: Response, next: NextFunction): void {
  const requestId = req.headers['x-request-id'] || uuidv4();
  res.setHeader('x-request-id', requestId);

  // Add to logger context
  res.locals.logger = logger.child({ requestId });
  next();
}

// Error handling middleware
function errorHandler(err: ApiError, req: Request, res: Response, next: NextFunction): void {
  const log = res.locals.logger || logger;

  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  log.error({ error: err, status }, `Request failed: ${message}`);

  res.status(status).json({
    error: {
      message,
      status,
      requestId: res.getHeader('x-request-id'),
    },
  });
}

// Initialize database schema
async function initializeDatabase(): Promise<void> {
  const client = await pool.connect();

  try {
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
    `);

    logger.info('Database initialized successfully');
  } finally {
    client.release();
  }
}

// Handler: List users
async function listUsers(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const result = await pool.query('SELECT id, name, email, created_at FROM users ORDER BY id');
    res.json(result.rows);
  } catch (err) {
    const error = new Error('Failed to query users') as ApiError;
    error.status = 500;
    next(error);
  }
}

// Handler: Get user by ID
async function getUser(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const { id } = req.params;

    if (!id || isNaN(parseInt(id))) {
      const error = new Error('Invalid user ID') as ApiError;
      error.status = 400;
      throw error;
    }

    const result = await pool.query(
      'SELECT id, name, email, created_at FROM users WHERE id = $1',
      [id]
    );

    if (result.rows.length === 0) {
      const error = new Error('User not found') as ApiError;
      error.status = 404;
      throw error;
    }

    res.json(result.rows[0]);
  } catch (err) {
    next(err);
  }
}

// Handler: Create user
async function createUser(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const { name, email }: CreateUserInput = req.body;

    // Validation
    if (!name || !email) {
      const error = new Error('Name and email are required') as ApiError;
      error.status = 400;
      throw error;
    }

    if (!email.includes('@')) {
      const error = new Error('Invalid email address') as ApiError;
      error.status = 400;
      throw error;
    }

    const result = await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email, created_at',
      [name, email]
    );

    res.status(201).json(result.rows[0]);
  } catch (err) {
    if ((err as Error).message.includes('duplicate key')) {
      const error = new Error('Email already exists') as ApiError;
      error.status = 409;
      next(error);
    } else {
      next(err);
    }
  }
}

// Handler: Delete user
async function deleteUser(req: Request, res: Response, next: NextFunction): Promise<void> {
  try {
    const { id } = req.params;

    if (!id || isNaN(parseInt(id))) {
      const error = new Error('Invalid user ID') as ApiError;
      error.status = 400;
      throw error;
    }

    const result = await pool.query('DELETE FROM users WHERE id = $1', [id]);

    if (result.rowCount === 0) {
      const error = new Error('User not found') as ApiError;
      error.status = 404;
      throw error;
    }

    res.status(204).send();
  } catch (err) {
    next(err);
  }
}

// Create Express app
function createApp(): Express {
  const app = express();

  // Middleware
  app.use(express.json());
  app.use(requestIdMiddleware);

  // Routes
  app.get('/health', (req: Request, res: Response) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  app.get('/users', listUsers);
  app.get('/users/:id', getUser);
  app.post('/users', createUser);
  app.delete('/users/:id', deleteUser);

  // Error handling
  app.use(errorHandler);

  return app;
}

// Main entry point
async function main(): Promise<void> {
  try {
    // Initialize database
    await initializeDatabase();

    // Create app
    const app = createApp();
    const port = process.env.PORT || 3000;

    // Create HTTP server
    const server = app.listen(port, () => {
      logger.info(`Server running on port ${port}`);
    });

    // Graceful shutdown
    process.on('SIGINT', () => {
      logger.info('Received SIGINT, shutting down gracefully');

      server.close(async () => {
        logger.info('HTTP server closed');
        await pool.end();
        logger.info('Database connections closed');
        process.exit(0);
      });

      // Force shutdown after 30 seconds
      setTimeout(() => {
        logger.error('Shutdown timeout exceeded, forcing exit');
        process.exit(1);
      }, 30000);
    });

    process.on('SIGTERM', () => {
      logger.info('Received SIGTERM, shutting down gracefully');
      server.close(() => {
        logger.info('HTTP server closed');
      });
    });
  } catch (err) {
    logger.error(err, 'Application startup failed');
    process.exit(1);
  }
}

// Start application
main();

export { createApp };
