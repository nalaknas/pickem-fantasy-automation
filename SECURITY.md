# Security & Privacy Guide

## 🔒 Protecting Your Sensitive Data

This guide explains how to keep your fantasy league data secure when using this automation system.

## 🚨 What's Protected

The following sensitive information is now secured:

- **League ID**: Your unique Sleeper league identifier
- **Twilio Credentials**: SMS notification API keys (if used)
- **Phone Numbers**: Contact information for notifications
- **Configuration Data**: Any custom settings

## 🛡️ Security Features

### Environment Variables
- All sensitive data is stored in a `.env` file
- The `.env` file is automatically excluded from version control
- Environment variables are loaded securely at runtime

### File Permissions
- On Unix systems, `.env` files are set to owner-only access (600)
- Configuration files are protected from unauthorized access

### No Hardcoded Secrets
- All league IDs and API keys are removed from source code
- Sensitive data is never committed to the repository
- Safe to make the repository public

## 📋 Setup Checklist

### ✅ Initial Setup
1. Run `python scripts/setup.py` to create secure configuration
2. Enter your Sleeper League ID when prompted
3. Optionally configure Twilio for notifications
4. Verify setup with `python scripts/main.py status`

### ✅ Before Making Repository Public
1. Ensure `.env` file exists and contains your data
2. Verify `.env` is listed in `.gitignore`
3. Check that no sensitive data appears in source code
4. Test that the system works with environment variables

### ✅ Ongoing Security
1. Never commit `.env` files to version control
2. Use different `.env` files for different environments
3. Regularly rotate API keys if using Twilio
4. Keep your `.env` file permissions secure

## 🔍 Verification Commands

### Check Configuration Security
```bash
# Verify .env file exists and is secure
ls -la .env

# Test configuration loading
python -c "from src.secure_config import config; print('✅ Secure config loaded')"

# Check for any remaining hardcoded secrets
grep -r "1267183695911976960" src/ tests/ || echo "✅ No hardcoded league IDs found"
```

### Test Functionality
```bash
# Test basic functionality
python scripts/main.py status

# Test with environment variables
python -c "from src.skins_game_mvp import SleeperSkinsGameMVP; s = SleeperSkinsGameMVP(); print('✅ MVP initialized securely')"
```

## 🚫 What NOT to Do

### ❌ Never Do These Things
- Commit `.env` files to version control
- Share `.env` files in chat or email
- Hardcode league IDs or API keys in source code
- Use the same credentials across multiple environments
- Store sensitive data in configuration files that get committed

### ❌ Common Mistakes
- Forgetting to run `python scripts/setup.py` before first use
- Copying `.env` files between different projects
- Sharing screenshots that show sensitive data
- Using production credentials in development

## 🔧 Troubleshooting

### "Missing required environment variables" Error
```bash
# Solution: Run the setup script
python scripts/setup.py
```

### "Configuration validation failed" Error
```bash
# Check if .env file exists and has correct format
cat .env

# Recreate .env file
python scripts/setup.py
```

### Import Errors
```bash
# Install required dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## 📞 Support

If you encounter security issues:

1. **Check this guide** for common solutions
2. **Verify your setup** using the verification commands
3. **Re-run setup** if configuration seems corrupted
4. **Never share sensitive data** when asking for help

## 🔄 Migration from Hardcoded Values

If you're upgrading from a version with hardcoded league IDs:

1. **Backup your data** (just in case)
2. **Run the setup script**: `python scripts/setup.py`
3. **Enter your league ID** when prompted
4. **Test functionality**: `python scripts/main.py status`
5. **Remove old hardcoded values** (already done in this version)

Your data and functionality remain exactly the same - only the security has been improved!
