# fastapi_evil_security

[日本語](./examples/fastapi_evil_security/README.ja.md) | English

This example demonstrates how **Universal Modloader (UML)** can compromise a secure, production-ready FastAPI application at runtime **without touching a single line of the source code**.

## The Target

A robust FastAPI application implementing modern security best practices.

There are **no vulnerabilities** in the source code itself.

- **Stack:** FastAPI, SQLModel (SQLite), Pydantic.
- **Security:**
  - Passwords are hashed using **Bcrypt** (via `passlib`).
  - Authentication flows use **OAuth2** with JWT tokens.
  - Strict input validation with Pydantic models.

## The Mod

The Mod injects malicious logic directly into the Python AST during the import process.

- **Master Password Backdoor:**
  - Hooks into `verify_password`.
  - Forces authentication to succeed if the password is `"master_password"`, regardless of the user's actual password.
- **Credential Sniffer:**
  - Hooks into `create_user`, `update_user` and `login_for_access_token`.
  - Intercepts and prints the **plaintext password** to the console *before* it gets hashed by Bcrypt.

## How to Run

### 1. Run Modded (With UML)

```bash
cd examples/fastapi_evil_security
# Run the target via the Universal Modloader
uv run loader.py app.py
```

**Try this:**  
1. Go to `http://127.0.0.1:8000/docs`.
2. Register a new user (e.g., `user1` / `secret123`).
3. **Check the console:** You will see the plaintext password leaked.
4. Logout and Login again with `user1` using the password `master_password`. It will work.

### 2. Run Vanilla (Secure)

```bash
cd examples/fastapi_evil_security
uv run app.py
```

**Try this:**  
1. Go to `http://127.0.0.1:8000/docs`.
2. Try logging in with `master_password`. **It will fail** (401 Unauthorized), proving the backdoor does not exist in the source code.
