/**
 * Tests for the user management API.
 *
 * Uses Jest and supertest for HTTP testing.
 */

import request from 'supertest';
import { createApp } from '../src/main';

describe('User API', () => {
  const app = createApp();

  describe('GET /health', () => {
    it('should return health status', async () => {
      const response = await request(app).get('/health');

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('status', 'ok');
      expect(response.body).toHaveProperty('timestamp');
    });
  });

  describe('GET /users', () => {
    it('should return list of users', async () => {
      const response = await request(app).get('/users');

      expect(response.status).toBe(200);
      expect(Array.isArray(response.body)).toBe(true);
    });
  });

  describe('POST /users', () => {
    it('should create a user with valid input', async () => {
      const newUser = {
        name: 'Alice',
        email: `alice-${Date.now()}@example.com`,
      };

      const response = await request(app).post('/users').send(newUser);

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
      expect(response.body).toHaveProperty('name', newUser.name);
      expect(response.body).toHaveProperty('email', newUser.email);
    });

    it('should reject request without name', async () => {
      const response = await request(app)
        .post('/users')
        .send({ email: 'test@example.com' });

      expect(response.status).toBe(400);
      expect(response.body).toHaveProperty('error');
    });

    it('should reject request without email', async () => {
      const response = await request(app)
        .post('/users')
        .send({ name: 'Test User' });

      expect(response.status).toBe(400);
    });

    it('should reject invalid email format', async () => {
      const response = await request(app)
        .post('/users')
        .send({ name: 'Test', email: 'not-an-email' });

      expect(response.status).toBe(400);
    });
  });

  describe('GET /users/:id', () => {
    let userId: number;

    beforeAll(async () => {
      // Create a user for testing
      const response = await request(app)
        .post('/users')
        .send({
          name: 'Test User',
          email: `test-${Date.now()}@example.com`,
        });
      userId = response.body.id;
    });

    it('should return user by ID', async () => {
      const response = await request(app).get(`/users/${userId}`);

      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('id', userId);
      expect(response.body).toHaveProperty('name', 'Test User');
    });

    it('should return 404 for non-existent user', async () => {
      const response = await request(app).get('/users/99999');

      expect(response.status).toBe(404);
      expect(response.body).toHaveProperty('error');
    });

    it('should return 400 for invalid ID', async () => {
      const response = await request(app).get('/users/invalid');

      expect(response.status).toBe(400);
    });
  });

  describe('DELETE /users/:id', () => {
    let userId: number;

    beforeAll(async () => {
      // Create a user for testing
      const response = await request(app)
        .post('/users')
        .send({
          name: 'Delete Test',
          email: `delete-${Date.now()}@example.com`,
        });
      userId = response.body.id;
    });

    it('should delete user by ID', async () => {
      const response = await request(app).delete(`/users/${userId}`);

      expect(response.status).toBe(204);
    });

    it('should return 404 when deleting non-existent user', async () => {
      const response = await request(app).delete('/users/99999');

      expect(response.status).toBe(404);
    });

    it('should return 400 for invalid ID', async () => {
      const response = await request(app).delete('/users/invalid');

      expect(response.status).toBe(400);
    });
  });

  describe('Request ID tracking', () => {
    it('should include request ID in response headers', async () => {
      const response = await request(app)
        .get('/users')
        .set('x-request-id', 'test-request-123');

      expect(response.headers).toHaveProperty('x-request-id', 'test-request-123');
    });

    it('should generate request ID if not provided', async () => {
      const response = await request(app).get('/users');

      expect(response.headers).toHaveProperty('x-request-id');
      const requestId = response.headers['x-request-id'];
      expect(typeof requestId).toBe('string');
      expect(requestId.length).toBeGreaterThan(0);
    });
  });
});
