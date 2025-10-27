# Docker Security Best Practices

This document outlines the security measures implemented in the Docker configuration.

## .dockerignore File

The `.dockerignore` file prevents sensitive and unnecessary files from being copied into the Docker image.

### What's Excluded

#### Security-Critical Files

- `.env` and `.env.*` - Environment variables with secrets
- `*.pem`, `*.key`, `*.crt` - SSL certificates and private keys
- `secrets/`, `credentials/` - Credential directories
- `.git/` - Git history that may contain sensitive data

#### Development Files

- `venv/`, `.venv/` - Virtual environments
- `__pycache__/`, `*.pyc` - Python bytecode
- `.vscode/`, `.idea/` - IDE configurations
- Test files and coverage reports

#### Documentation

- Most markdown files (except README.md in root)
- License files
- Contributing guides

#### CI/CD and Build Files

- `.github/` - GitHub Actions workflows
- `docker-compose*.yml` - Compose files
- `Dockerfile*` - Dockerfile itself
- Pre-commit configurations

## Dockerfile Security Improvements

### 1. Explicit File Copying

Instead of `COPY . .`, we explicitly copy only what's needed:

```dockerfile
COPY app/ ./app/
COPY run.py .
COPY .env.example .
```text

**Benefits:**

- Reduces attack surface
- Prevents accidental inclusion of sensitive files
- Makes dependencies explicit
- Smaller image size

### 2. Non-Root User

The container runs as a non-root user (`appuser`):

```dockerfile
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser
```text

**Benefits:**

- Limits damage if container is compromised
- Follows principle of least privilege
- Required by many Kubernetes security policies

### 3. Minimal Base Image

Uses `python:3.11-slim` instead of full Python image:

**Benefits:**

- Smaller attack surface (fewer packages)
- Faster builds and deployments
- Reduced CVE exposure

### 4. Clean Package Cache

```dockerfile
RUN apt-get update && apt-get install -y \
    ... \
    && rm -rf /var/lib/apt/lists/*
```text

**Benefits:**

- Reduces image size
- Removes unnecessary package metadata

## Additional Security Recommendations

### 1. Environment Variables

**Never commit `.env` files!**

```bash
# Good - use example file
git add .env.example

# Bad - never do this!
git add .env
```text

For production:

- Use Docker secrets
- Use Kubernetes secrets
- Use cloud provider secret managers (AWS Secrets Manager, Azure Key Vault, etc.)

### 2. Volume Mounts for Sensitive Data

Instead of copying into image:

```yaml
# docker-compose.yml
services:
  web:
    volumes:
      - ./models:/app/models:ro  # Read-only mount
      - ./uploads:/app/uploads
    environment:
      - SECRET_KEY=${SECRET_KEY}  # From environment
```text

### 3. Image Scanning

Regularly scan images for vulnerabilities:

```bash
# Using Docker Scout
docker scout cves recognize:latest

# Using Trivy
trivy image recognize:latest

# Using Snyk
snyk container test recognize:latest
```text

### 4. Multi-Stage Builds (Future Enhancement)

For even better security:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ ./app/
COPY run.py .
ENV PATH=/root/.local/bin:$PATH
```text

### 5. Read-Only Filesystem (Advanced)

Run container with read-only root filesystem:

```yaml
services:
  web:
    read_only: true
    tmpfs:
      - /tmp
      - /app/uploads
```text

## Verification Checklist

Before deploying:

- [ ] `.dockerignore` file is present and comprehensive
- [ ] No `.env` files in git history
- [ ] Container runs as non-root user
- [ ] Sensitive files are volume-mounted, not copied
- [ ] Image has been scanned for vulnerabilities
- [ ] Environment variables are injected at runtime
- [ ] File permissions are correct (`chown` commands)
- [ ] Only necessary ports are exposed
- [ ] SSL/TLS certificates are managed externally

## Testing Security

### 1. Check What's in the Image

```bash
# Build image
docker build -t recognize:test .

# Inspect contents
docker run --rm recognize:test ls -la /app

# Check for sensitive files (should return nothing)
docker run --rm recognize:test find /app -name ".env" -o -name "*.pem"
```text

### 2. Verify Non-Root User

```bash
# Should show 'appuser', not 'root'
docker run --rm recognize:test whoami

# Should show UID 1000
docker run --rm recognize:test id
```text

### 3. Test File Permissions

```bash
# Should not be able to write to /app
docker run --rm recognize:test touch /app/test.txt
# Expected: Permission denied
```text

## Incident Response

If sensitive data is accidentally committed:

1. **Remove from Git history immediately:**

   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/sensitive/file" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Rotate all exposed credentials**

3. **Force push to remote:**

   ```bash
   git push origin --force --all
   ```

4. **Notify team and security**

## References

- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Snyk Docker Security](https://snyk.io/learn/docker-security/)
