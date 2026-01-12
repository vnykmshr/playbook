# Security Patterns & Microservice Security

## Overview

Security in microservices requires a multi-layered approach: authentication proves *who* you are, authorization proves *what* you can do, and data protection ensures information stays safe. Rather than bolting security on at the end, effective architectures embed security patterns throughout design.

This guide covers proven security patterns for microservices, showing when to use each and real-world trade-offs.

**Caveat:** Security patterns can add significant complexity. Use `/pb-preamble` thinking: question threat models, challenge assumed attack surfaces, and surface the real risk vs. implementation cost trade-off.

---

## Authentication Patterns

Authentication answers: "Are you who you claim to be?"

### Pattern 1: OAuth 2.0 with Authorization Code Flow

**When to use**: Third-party integrations, user-facing APIs, token-based access

**How it works**:
1. User requests access to their data
2. App redirects to authorization server
3. User grants permission
4. Authorization server returns authorization code
5. App exchanges code for access token (backend-to-backend)
6. App uses access token to call APIs

**Python Example**:
```python
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, url_for

app = Flask(__name__)
client_id = "your-client-id"
client_secret = "your-client-secret"
authorization_base_url = "https://auth.example.com/authorize"
token_url = "https://auth.example.com/token"

@app.route("/login")
def login():
    oauth = OAuth2Session(client_id, redirect_uri=url_for('callback', _external=True))
    authorization_url, state = oauth.authorization_url(authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    oauth = OAuth2Session(client_id, state=session['oauth_state'])
    token = oauth.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url
    )
    session['oauth_token'] = token
    return redirect(url_for('dashboard'))

@app.route("/api/user-data")
def get_user_data():
    oauth = OAuth2Session(client_id, token=session['oauth_token'])
    user_data = oauth.get("https://api.example.com/user").json()
    return user_data
```

**JavaScript Example**:
```javascript
// Frontend: Using OAuth 2.0 Authorization Code Flow with PKCE
const clientId = 'your-client-id';
const redirectUri = 'https://yourapp.com/callback';
const authorizationUrl = 'https://auth.example.com/authorize';

function generateCodeChallenge(codeVerifier) {
  return btoa(String.fromCharCode.apply(null,
    new Uint8Array(codeVerifier)
  )).replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

function loginWithOAuth() {
  const codeVerifier = generateRandomString(128);
  sessionStorage.setItem('code_verifier', codeVerifier);

  const codeChallenge = generateCodeChallenge(codeVerifier);
  const params = new URLSearchParams({
    client_id: clientId,
    response_type: 'code',
    scope: 'openid profile email',
    redirect_uri: redirectUri,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256'
  });

  window.location.href = `${authorizationUrl}?${params}`;
}

// After redirect back to app
async function handleCallback(authCode) {
  const codeVerifier = sessionStorage.getItem('code_verifier');
  const response = await fetch('/api/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'authorization_code',
      code: authCode,
      code_verifier: codeVerifier,
      client_id: clientId
    })
  });

  const { access_token } = await response.json();
  localStorage.setItem('access_token', access_token);
}
```

**Go Example**:
```go
package main

import (
  "context"
  "log"
  "net/http"

  "github.com/coreos/go-oidc/v3/oidc"
  "golang.org/x/oauth2"
)

var (
  googleOauthConfig *oauth2.Config
  googleOidcProvider *oidc.Provider
)

func init() {
  var err error
  googleOidcProvider, err = oidc.NewProvider(context.Background(), "https://accounts.google.com")
  if err != nil {
    log.Fatal(err)
  }

  googleOauthConfig = &oauth2.Config{
    ClientID:     "your-client-id",
    ClientSecret: "your-client-secret",
    RedirectURL:  "http://localhost:8080/auth/google/callback",
    Scopes: []string{
      oidc.ScopeOpenID,
      "profile",
      "email",
    },
    Endpoint: googleOidcProvider.Endpoint(),
  }
}

func handleGoogleLogin(w http.ResponseWriter, r *http.Request) {
  state := generateRandomString(16)
  http.SetCookie(w, &http.Cookie{
    Name:  "oauth_state",
    Value: state,
    Path:  "/",
  })

  authURL := googleOauthConfig.AuthCodeURL(state, oauth2.AccessTypeOffline)
  http.Redirect(w, r, authURL, http.StatusTemporaryRedirect)
}

func handleGoogleCallback(w http.ResponseWriter, r *http.Request) {
  cookie, _ := r.Cookie("oauth_state")
  if r.URL.Query().Get("state") != cookie.Value {
    http.Error(w, "State mismatch", http.StatusBadRequest)
    return
  }

  code := r.URL.Query().Get("code")
  token, err := googleOauthConfig.Exchange(r.Context(), code)
  if err != nil {
    http.Error(w, "Failed to exchange token", http.StatusInternalServerError)
    return
  }

  // Verify and use token
  idToken, err := googleOidcProvider.Verifier(&oidc.Config{
    ClientID: googleOauthConfig.ClientID,
  }).Verify(r.Context(), token.Extra("id_token").(string))
  if err != nil {
    http.Error(w, "Failed to verify ID token", http.StatusInternalServerError)
    return
  }

  var claims struct {
    Email string `json:"email"`
    Name  string `json:"name"`
  }
  idToken.Claims(&claims)

  // Create user session or JWT
  userJWT := createJWT(claims.Email)
  http.SetCookie(w, &http.Cookie{
    Name:  "auth_token",
    Value: userJWT,
    Path:  "/",
  })

  http.Redirect(w, r, "/dashboard", http.StatusSeeOther)
}
```

**Trade-offs**:
- ✅ Industry standard, well-supported
- ✅ Doesn't expose user password to application
- ✅ Easy delegation to third-party identity providers
- ❌ More complex than basic authentication
- ❌ Requires redirect flow (not suitable for server-to-server)

**Antipatterns**:
- ❌ Storing authorization codes indefinitely
- ❌ Sending access tokens through unsecured channels
- ❌ Not validating state parameter (CSRF vulnerability)
- ❌ Storing user password instead of using OAuth

---

### Pattern 2: JWT (JSON Web Tokens) for API Authentication

**When to use**: Stateless API authentication, microservice-to-microservice, mobile apps

**How it works**:
1. Client authenticates with credentials
2. Server creates JWT (Header.Payload.Signature)
3. Client includes JWT in Authorization header for each request
4. Server validates signature to verify authenticity

**JWT Structure**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiJ1c2VyMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Python Example**:
```python
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)
secret_key = "your-secret-key-keep-safe"

def create_jwt(user_id, email):
    payload = {
        'user_id': user_id,
        'email': email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

@app.route('/login', methods=['POST'])
def login():
    credentials = request.get_json()
    # Verify username/password (simplified)
    if verify_password(credentials['username'], credentials['password']):
        user = get_user(credentials['username'])
        token = create_jwt(user['id'], user['email'])
        return jsonify({'access_token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.before_request
def verify_token():
    if request.path.startswith('/api/'):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing token'}), 401

        try:
            token = auth_header.split(' ')[1]  # "Bearer <token>"
            payload = verify_jwt(token)
            if not payload:
                return jsonify({'error': 'Invalid token'}), 401
            request.user_id = payload['user_id']
        except:
            return jsonify({'error': 'Invalid token'}), 401

@app.route('/api/user-profile')
def user_profile():
    user = get_user_by_id(request.user_id)
    return jsonify(user)
```

**Go Example**:
```go
package main

import (
  "fmt"
  "time"

  "github.com/golang-jwt/jwt/v5"
)

type CustomClaims struct {
  UserID int
  Email  string
  jwt.RegisteredClaims
}

func createJWT(userID int, email string, secretKey string) (string, error) {
  claims := CustomClaims{
    UserID: userID,
    Email:  email,
    RegisteredClaims: jwt.RegisteredClaims{
      IssuedAt:  jwt.NewNumericDate(time.Now()),
      ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
    },
  }

  token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
  tokenString, err := token.SignedString([]byte(secretKey))
  return tokenString, err
}

func verifyJWT(tokenString string, secretKey string) (*CustomClaims, error) {
  token, err := jwt.ParseWithClaims(tokenString, &CustomClaims{}, func(token *jwt.Token) (interface{}, error) {
    return []byte(secretKey), nil
  })

  if err != nil {
    return nil, err
  }

  claims, ok := token.Claims.(*CustomClaims)
  if !ok || !token.Valid {
    return nil, fmt.Errorf("invalid token")
  }

  return claims, nil
}

func authMiddleware(secretKey string) func(http.Handler) http.Handler {
  return func(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
      authHeader := r.Header.Get("Authorization")
      if authHeader == "" {
        http.Error(w, "Missing token", http.StatusUnauthorized)
        return
      }

      tokenString := authHeader[7:] // Remove "Bearer "
      claims, err := verifyJWT(tokenString, secretKey)
      if err != nil {
        http.Error(w, "Invalid token", http.StatusUnauthorized)
        return
      }

      // Add claims to request context
      r.Header.Set("X-User-ID", fmt.Sprintf("%d", claims.UserID))
      next.ServeHTTP(w, r)
    })
  }
}
```

**Trade-offs**:
- ✅ Stateless (no server session needed)
- ✅ Scalable across multiple servers
- ✅ Works well for APIs and microservices
- ❌ Token size larger than session cookies
- ❌ Can't revoke tokens immediately (use token blacklists for logout)

**Antipatterns**:
- ❌ Storing sensitive data in JWT (it's base64-encoded, not encrypted)
- ❌ Using weak secret keys
- ❌ Not validating expiration
- ❌ Storing JWT in local storage (use httpOnly cookies for web apps)

---

### Pattern 3: mTLS (Mutual TLS) for Service-to-Service Authentication

**When to use**: Internal microservice communication, service mesh, high-security requirements

**How it works**:
1. Both client and server present certificates
2. Both verify each other's certificates
3. TLS handshake establishes encrypted connection
4. Communication is authenticated and encrypted

**Go Example (mTLS Server)**:
```go
package main

import (
  "crypto/tls"
  "log"
  "net/http"
)

func main() {
  // Load server certificate and key
  cert, err := tls.LoadX509KeyPair("server.crt", "server.key")
  if err != nil {
    log.Fatal(err)
  }

  // Load client CA certificate for verification
  caCert, err := ioutil.ReadFile("client-ca.crt")
  if err != nil {
    log.Fatal(err)
  }

  caCertPool := x509.NewCertPool()
  caCertPool.AppendCertsFromPEM(caCert)

  // Configure TLS with client certificate verification
  tlsConfig := &tls.Config{
    Certificates: []tls.Certificate{cert},
    ClientCAs:    caCertPool,
    ClientAuth:   tls.RequireAndVerifyClientCert,
    MinVersion:   tls.VersionTLS12,
  }

  server := &http.Server{
    Addr:      ":8443",
    TLSConfig: tlsConfig,
  }

  http.HandleFunc("/api/data", func(w http.ResponseWriter, r *http.Request) {
    // Client cert is verified by TLS layer
    clientName := r.TLS.PeerCertificates[0].Subject.CommonName
    log.Printf("Request from service: %s\n", clientName)
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("Authenticated service data"))
  })

  log.Println("mTLS server listening on :8443")
  log.Fatal(server.ListenAndServeTLS("", ""))
}
```

**Go Example (mTLS Client)**:
```go
func createMTLSClient(certFile, keyFile, caFile string) (*http.Client, error) {
  // Load client certificate
  cert, err := tls.LoadX509KeyPair(certFile, keyFile)
  if err != nil {
    return nil, err
  }

  // Load server CA certificate
  caCert, err := ioutil.ReadFile(caFile)
  if err != nil {
    return nil, err
  }

  caCertPool := x509.NewCertPool()
  caCertPool.AppendCertsFromPEM(caCert)

  // Configure TLS
  tlsConfig := &tls.Config{
    Certificates: []tls.Certificate{cert},
    RootCAs:      caCertPool,
    MinVersion:   tls.VersionTLS12,
  }

  client := &http.Client{
    Transport: &http.Transport{
      TLSClientConfig: tlsConfig,
    },
  }

  return client, nil
}

// Usage
client, _ := createMTLSClient("client.crt", "client.key", "ca.crt")
resp, _ := client.Get("https://internal-service:8443/api/data")
```

**Trade-offs**:
- ✅ Strongest authentication (mutual verification)
- ✅ Encrypted in transit
- ✅ No shared secrets
- ❌ Certificate management overhead
- ❌ More complex to set up than API keys
- ❌ Performance cost of TLS handshake

---

## Authorization Patterns

Authorization answers: "What are you allowed to do?"

### Pattern 1: RBAC (Role-Based Access Control)

**When to use**: Most common authorization, clear role definitions

**How it works**: Users have roles, roles have permissions. Check if user's role has required permission.

**Python Example**:
```python
from enum import Enum
from functools import wraps

class Role(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.MANAGE_USERS],
    Role.MANAGER: [Permission.READ, Permission.WRITE, Permission.DELETE],
    Role.USER: [Permission.READ],
}

def require_permission(required_permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = get_current_user_role()
            if required_permission not in ROLE_PERMISSIONS.get(user_role, []):
                raise PermissionError(f"User role {user_role} lacks {required_permission}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/api/data', methods=['POST'])
@require_permission(Permission.WRITE)
def create_data():
    # Only users with WRITE permission can access this
    return jsonify({'created': True})

@app.route('/api/users/<user_id>', methods=['DELETE'])
@require_permission(Permission.MANAGE_USERS)
def delete_user(user_id):
    # Only admins can delete users
    return jsonify({'deleted': user_id})
```

**Go Example**:
```go
type Role string

const (
  RoleAdmin    Role = "admin"
  RoleManager  Role = "manager"
  RoleUser     Role = "user"
)

type Permission string

const (
  PermissionRead       Permission = "read"
  PermissionWrite      Permission = "write"
  PermissionDelete     Permission = "delete"
  PermissionManageUsers Permission = "manage_users"
)

var rolePermissions = map[Role][]Permission{
  RoleAdmin:    {PermissionRead, PermissionWrite, PermissionDelete, PermissionManageUsers},
  RoleManager:  {PermissionRead, PermissionWrite, PermissionDelete},
  RoleUser:     {PermissionRead},
}

func hasPermission(userRole Role, requiredPerm Permission) bool {
  permissions := rolePermissions[userRole]
  for _, p := range permissions {
    if p == requiredPerm {
      return true
    }
  }
  return false
}

func requirePermission(perm Permission) func(http.Handler) http.Handler {
  return func(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
      userRole := getUserRole(r)
      if !hasPermission(userRole, perm) {
        http.Error(w, "Insufficient permissions", http.StatusForbidden)
        return
      }
      next.ServeHTTP(w, r)
    })
  }
}

// Usage
mux.HandleFunc("/api/data", requirePermission(PermissionWrite)(createDataHandler))
mux.HandleFunc("/api/users/{id}", requirePermission(PermissionManageUsers)(deleteUserHandler))
```

**Trade-offs**:
- ✅ Simple and understandable
- ✅ Easy to implement
- ❌ Inflexible for fine-grained control
- ❌ Doesn't account for context (time, location, resource)

---

### Pattern 2: ABAC (Attribute-Based Access Control)

**When to use**: Fine-grained control, context-dependent access, complex business rules

**How it works**: Access decisions based on attributes of user, resource, action, and environment.

**Python Example**:
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AccessContext:
    user_id: int
    user_dept: str
    resource_owner: int
    resource_type: str
    resource_sensitivity: str
    action: str
    time_of_day: int
    is_vpn: bool

def check_access(context: AccessContext) -> bool:
    """
    Complex access control rules:
    - Users can only read/write their own data
    - Managers can read team data
    - High-sensitivity resources only accessible during business hours on VPN
    - Admins have unrestricted access
    """

    rules = [
        # Rule 1: Owner can always access their own data
        lambda ctx: ctx.user_id == ctx.resource_owner,

        # Rule 2: Managers can read team data
        lambda ctx: (ctx.user_dept == "management" and
                    ctx.action == "read" and
                    ctx.resource_type == "team_data"),

        # Rule 3: High-sensitivity only during business hours on VPN
        lambda ctx: not (ctx.resource_sensitivity == "high" and
                        (ctx.time_of_day < 9 or ctx.time_of_day > 17 or not ctx.is_vpn)),

        # Rule 4: Admins bypass all checks
        lambda ctx: ctx.user_dept == "admin",
    ]

    return any(rule(context) for rule in rules)

# Usage
context = AccessContext(
    user_id=123,
    user_dept="engineering",
    resource_owner=123,
    resource_type="personal_data",
    resource_sensitivity="high",
    action="read",
    time_of_day=14,
    is_vpn=True
)

if check_access(context):
    return get_resource()
else:
    raise PermissionError("Access denied")
```

**Trade-offs**:
- ✅ Highly flexible
- ✅ Handles complex business logic
- ❌ Hard to understand and maintain
- ❌ Performance overhead of evaluation

---

## Secret Management Patterns

### Pattern 1: Encrypted Secret Vault

**When to use**: Production applications, sensitive credentials (API keys, database passwords)

**Go Example with HashiCorp Vault**:
```go
import "github.com/hashicorp/vault/api"

func getSecretFromVault(secretPath string) (string, error) {
  config := api.DefaultConfig()
  config.Address = "https://vault.example.com:8200"

  client, err := api.NewClient(config)
  if err != nil {
    return "", err
  }

  // Authenticate with service token or approle
  auth := client.Auth().Token()
  secret, err := auth.RenewSelf(1, 3600)
  if err != nil {
    return "", err
  }

  // Read secret
  secret, err = client.Logical().Read(secretPath)
  if err != nil {
    return "", err
  }

  // Extract value
  dbPassword := secret.Data["data"].(map[string]interface{})["password"].(string)
  return dbPassword, nil
}

// Usage
dbPassword, _ := getSecretFromVault("secret/database/prod")
db.Connect(dbPassword)
```

**Trade-offs**:
- ✅ Centralized secret management
- ✅ Audit trail of secret access
- ✅ Rotation without app restart
- ❌ Additional infrastructure
- ❌ Single point of failure

---

## Data Protection Patterns

### Pattern 1: Encryption at Rest

**When to use**: Sensitive data in databases, file systems, backups

**Python Example**:
```python
from cryptography.fernet import Fernet
import base64
import hashlib

def encrypt_field(plaintext: str, encryption_key: str) -> str:
    """Encrypt a single field using Fernet (AES)"""
    key = base64.urlsafe_b64encode(
        hashlib.sha256(encryption_key.encode()).digest()
    )
    cipher = Fernet(key)
    encrypted = cipher.encrypt(plaintext.encode())
    return encrypted.decode()

def decrypt_field(ciphertext: str, encryption_key: str) -> str:
    """Decrypt a field"""
    key = base64.urlsafe_b64encode(
        hashlib.sha256(encryption_key.encode()).digest()
    )
    cipher = Fernet(key)
    decrypted = cipher.decrypt(ciphertext.encode())
    return decrypted.decode()

# Usage in ORM
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    ssn = Column(String)  # Always encrypted

    @property
    def ssn_decrypted(self):
        return decrypt_field(self.ssn, app.config['ENCRYPTION_KEY'])

    @ssn_decrypted.setter
    def ssn_decrypted(self, value):
        self.ssn = encrypt_field(value, app.config['ENCRYPTION_KEY'])

# In database: ssn is stored encrypted
user = User(email='user@example.com')
user.ssn_decrypted = '123-45-6789'  # Automatically encrypted on save
session.add(user)
session.commit()  # Stored as encrypted ciphertext

# On retrieval: transparently decrypted
retrieved_user = session.query(User).first()
print(retrieved_user.ssn_decrypted)  # '123-45-6789'
```

**Trade-offs**:
- ✅ Protects data at rest (database breaches)
- ✅ Compliance requirement (PCI-DSS, HIPAA, GDPR)
- ❌ Key management complexity
- ❌ Performance overhead (encrypt/decrypt on every access)

---

## Input Validation Pattern

### Validate All External Input

**When to use**: Every entry point (APIs, forms, file uploads, external systems)

**Python Example**:
```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=0, le=150)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v

    @validator('password')
    def password_complexity(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('must contain uppercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('must contain number')
        return v

@app.post("/api/users")
def create_user(user: UserCreateRequest):
    # pydantic validates automatically
    # Invalid input returns 422 error
    db_user = create_in_db(user.dict())
    return db_user
```

**Go Example**:
```go
type UserCreateRequest struct {
  Email    string `json:"email" binding:"required,email"`
  Username string `json:"username" binding:"required,min=3,max=50"`
  Password string `json:"password" binding:"required,min=8"`
  Age      int    `json:"age" binding:"required,min=0,max=150"`
}

func createUser(c *gin.Context) {
  var req UserCreateRequest

  // Validate input
  if err := c.ShouldBindJSON(&req); err != nil {
    c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
    return
  }

  // Additional validation
  if !isStrongPassword(req.Password) {
    c.JSON(http.StatusBadRequest, gin.H{"error": "weak password"})
    return
  }

  user := createInDB(req)
  c.JSON(http.StatusCreated, user)
}

func isStrongPassword(pwd string) bool {
  hasUpper := false
  hasDigit := false
  for _, c := range pwd {
    if unicode.IsUpper(c) {
      hasUpper = true
    }
    if unicode.IsDigit(c) {
      hasDigit = true
    }
  }
  return hasUpper && hasDigit && len(pwd) >= 8
}
```

---

## Common Security Antipatterns

❌ **Storing passwords in plaintext** — Always hash with bcrypt/scrypt
❌ **Logging sensitive data** — Never log passwords, tokens, PII
❌ **Hardcoding secrets** — Use vault or environment variables
❌ **SQL injection** — Use parameterized queries, never string concatenation
❌ **XSS vulnerabilities** — Always encode/escape output
❌ **Trusting client-side validation** — Always validate server-side
❌ **Weak TLS versions** — Use TLS 1.2+ minimum
❌ **Ignoring certificate expiration** — Monitor and rotate regularly

---

## When to Use Security Patterns

**Use these patterns when**:
- Building APIs with external users
- Handling sensitive data (PII, payments, health)
- Meeting compliance requirements (HIPAA, GDPR, PCI-DSS, SOC 2)
- Building multi-tenant systems
- Microservices with inter-service communication

**Don't over-engineer**:
- Internal tools with limited users: simple auth is fine
- Publicly documented data: encryption not needed
- MVPs: start simple, add security as you scale

---

## Related Commands

- See `/pb-security` for security review checklist
- See `/pb-review-microservice` for microservice security review
- See `/pb-patterns-core` for OWASP patterns overview
- See `/pb-logging` for secure logging practices

---

**Use these patterns as building blocks. Security is layered, not single-solution.**
