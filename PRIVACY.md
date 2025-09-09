# Privacy & Data Protection

## 🔒 **CRITICAL: Personal Data Protection**

This repository is designed to protect all personal and league-specific information from being exposed in public repositories.

## 🚨 **What's Protected**

The following sensitive information is **NEVER** committed to version control:

- **League Member Names**: All player/usernames
- **League IDs**: Your unique Sleeper league identifier  
- **Personal Data**: Any identifying information
- **Game Results**: Actual weekly results and scores
- **Export Reports**: Generated CSV/Excel files with real data
- **Backup Files**: Any backup data files
- **Configuration Data**: Real league settings

## 📁 **Protected Directories & Files**

All of these are excluded from Git tracking:

```
data/                    # All league data
backups/                # Backup files
exports/                # Generated reports
*.json                  # Data files
*.csv                   # Export files
*.xlsx                  # Excel files
.env                    # Environment variables
```

## 🛡️ **How It Works**

### **For Public Repository**
- Only code and templates are visible
- No personal data is exposed
- Safe for public viewing and cloning

### **For Local Use**
- Create `.env` file with your league ID
- Run `python scripts/setup.py` to configure
- All data stays local and private

## 📋 **Setup for New Users**

1. **Clone the repository** (safe - no personal data)
2. **Copy configuration template**:
   ```bash
   cp config/env.template .env
   ```
3. **Edit `.env`** with your league ID
4. **Run setup**:
   ```bash
   python scripts/setup.py
   ```
5. **Start using** - all data stays local

## 🔍 **Verification Commands**

Check that no personal data is tracked:
```bash
# Should show no personal data files
git status

# Should show no personal information
grep -r "your_username" . --exclude-dir=.git
```

## ⚠️ **Important Notes**

- **Never commit** `.env` files
- **Never commit** `data/` directory contents
- **Never commit** `exports/` directory contents
- **Never commit** `backups/` directory contents
- **Always use** environment variables for sensitive data

## 🎯 **Result**

- **Public Repository**: Clean, professional, no personal data
- **Local Environment**: Full functionality with your data
- **Privacy**: Complete protection of personal information
- **Usability**: Easy setup for new users

Your personal league data remains completely private while the code is safely shareable!
