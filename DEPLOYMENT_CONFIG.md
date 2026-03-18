# Deployment Configuration Guide

## Overview
This document describes the required GitHub Secrets and environment configuration needed for the CI/CD workflows to function properly.

## Current Status
- ✅ **CI Workflow**: Passing
- ❌ **Deploy Workflow**: Failing (missing secrets)
- ❌ **CD Workflow**: Fixed code issue, but will fail at deployment (missing secrets)

## Required GitHub Secrets

### For Deploy Workflow (`.github/workflows/deploy.yml`)

| Secret Name | Description | Example |
|------------|-------------|---------|
| `SERVER_HOST` | Production server hostname or IP address | `example.com` or `192.168.1.100` |
| `SERVER_USER` | SSH username for server access | `ubuntu` or `root` |
| `SERVER_SSH_KEY` | Private SSH key for authentication | Contents of `~/.ssh/id_rsa` |
| `APP_URL` | Application URL for health checks | `https://example.com` |

### For CD Workflow (`.github/workflows/cd.yml`)

| Secret Name | Description | Example |
|------------|-------------|---------|
| `DEPLOY_HOST` | Production server hostname or IP address | `example.com` or `192.168.1.100` |
| `DEPLOY_USER` | SSH username for server access | `ubuntu` or `root` |
| `DEPLOY_KEY` | Private SSH key for authentication | Contents of `~/.ssh/id_rsa` |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications | `-1001234567890` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token for notifications | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |

## How to Add GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value
5. Click **Add secret**

## SSH Key Setup

### Generate SSH Key Pair (if you don't have one)

```bash
ssh-keygen -t ed25519 -C "github-actions@worldcup-scout-pro"
```

### Add Public Key to Server

```bash
# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server-ip

# Or manually add to ~/.ssh/authorized_keys on the server
cat ~/.ssh/id_ed25519.pub | ssh user@server-ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Add Private Key to GitHub Secrets

```bash
# Display private key (copy this to GitHub Secret)
cat ~/.ssh/id_ed25519
```

## Telegram Bot Setup (Optional)

If you want deployment notifications via Telegram:

1. **Create a Telegram Bot**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` and follow instructions
   - Save the bot token

2. **Get Chat ID**:
   - Add the bot to your group/channel
   - Send a message to the bot
   - Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find the `chat.id` in the response

3. **Add to GitHub Secrets**:
   - `TELEGRAM_BOT_TOKEN`: The token from BotFather
   - `TELEGRAM_CHAT_ID`: The chat ID from the API response

## Server Requirements

### Directory Structure

The deployment scripts expect the following directory on the server:

```
/root/projects/worldcup-scout-pro/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env
└── (git repository)
```

### Docker Compose Setup

Ensure `docker-compose.prod.yml` exists on the server with proper configuration.

### Environment Variables

Create a `.env` file on the server with required environment variables:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/worldcup_scout_pro
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=worldcup_scout_pro

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (if needed)
ANTHROPIC_API_KEY=your-key
OPENAI_API_KEY=your-key
```

## Testing the Configuration

### Test SSH Connection

```bash
ssh -i ~/.ssh/id_ed25519 user@server-ip "echo 'SSH connection successful'"
```

### Test Deployment Manually

```bash
# On the server
cd /root/projects/worldcup-scout-pro
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

## Troubleshooting

### Deploy Workflow Fails with "missing server host"

**Solution**: Add the required secrets (`SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`, `APP_URL`) to GitHub repository settings.

### CD Workflow Fails with "No module named ruff"

**Solution**: This has been fixed in the latest commit. The workflow now installs dev dependencies with `pip install -e ".[dev]"`.

### SSH Connection Fails

**Possible causes**:
1. Wrong SSH key format (ensure it's the private key, not public)
2. Server doesn't have the public key in `~/.ssh/authorized_keys`
3. Wrong username or hostname
4. Firewall blocking SSH port (22)

**Debug**:
```bash
ssh -vvv -i ~/.ssh/id_ed25519 user@server-ip
```

### Docker Compose Fails

**Possible causes**:
1. Missing `.env` file on server
2. Wrong file path in deployment script
3. Docker not installed or not running
4. Insufficient permissions

**Debug**:
```bash
# On the server
docker-compose -f docker-compose.prod.yml config  # Validate config
docker-compose -f docker-compose.prod.yml ps      # Check running containers
docker-compose -f docker-compose.prod.yml logs    # View logs
```

## Next Steps

1. ✅ Fix backend dev dependencies (DONE)
2. ⏳ Add required GitHub Secrets
3. ⏳ Set up production server with Docker
4. ⏳ Configure environment variables
5. ⏳ Test deployment manually
6. ⏳ Enable GitHub Actions workflows

## Code Changes Made

### Fixed: Backend Lint Dependency Issue

**File**: `.github/workflows/cd.yml`

**Change**:
```yaml
# Before
pip install -e .

# After
pip install -e ".[dev]"
```

**Reason**: The workflow needs dev dependencies (ruff, pytest, pytest-cov) for linting and testing, but was only installing production dependencies.

## Summary

- **Code Issue**: Fixed missing dev dependencies in CD workflow
- **Configuration Issues**: Both Deploy and CD workflows require GitHub Secrets to be configured
- **No code bugs**: The application code itself is working correctly
- **CI Workflow**: Already passing, no issues

Once the GitHub Secrets are configured, both workflows should pass successfully.
