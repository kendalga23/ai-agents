# WSL Setup Guide for Windows - Complete with Debugging

## Overview
This guide documents the complete setup process for WSL (Windows Subsystem for Linux) to run AI agents that require MCP servers, which only work properly in Linux environments.

## Prerequisites
- Windows 10/11
- PowerShell with administrator privileges
- Internet connection

## Part 1: Install WSL

### Step 1: Install WSL
```powershell
wsl --install
```

**Expected Output:**
```
Installing: Ubuntu
Ubuntu has been installed.
Launching Ubuntu...
Installing, this may take a few minutes...
```

### Step 2: Create Ubuntu User Account
When prompted, create your Ubuntu username and password:
```
Enter new UNIX username: [your-username]
New password: [your-password]
Retype new password: [your-password]
```

**Expected Output:**
```
Installation successful!
Welcome to Ubuntu 24.04.1 LTS
```

## Part 2: Install uv and Clone Repository

### Step 3: Access WSL Ubuntu
From PowerShell, run:
```powershell
ubuntu
```

**Expected Prompt:**
```
[username]@[hostname]:~$
```

### Step 4: Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**⚠️ Common Error:**
```
curl: option -LsSF: is badly used here
```
**Solution:** Use lowercase `f` in `-LsSf`, not uppercase `F`

**Expected Output:**
```
Downloading uv...
Installing uv...
To add $HOME/.local/bin to your PATH, either restart your shell or run:
    source $HOME/.local/bin/env (sh, bash, zsh)
```

### Step 5: Update PATH
```bash
source $HOME/.local/bin/env
```

**⚠️ Common Error:**
```
-bash: syntax error near unexpected token '('
```
**Solution:** Don't include the shell type indicators `(sh, bash, zsh)` - just run:
```bash
source $HOME/.local/bin/env
```

### Step 6: Verify uv Installation
```bash
uv --version
```

**Expected Output:**
```
uv [version number]
```

### Step 7: Create Projects Directory
```bash
mkdir projects
cd projects
```

### Step 8: Clone Repository
```bash
git clone https://github.com/ed-donner/agents.git
```

### Step 9: Navigate to Project
```bash
cd agents
```

### Step 10: Install Dependencies
```bash
uv sync
```

## Part 3: Configure Cursor for WSL

### Step 11: Install WSL Extension
1. Open Cursor
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "WSL" by Anysphere
4. Install the WSL extension

### Step 12: Open WSL Window
1. Press Ctrl+Shift+P
2. Search for "Remote-WSL: New Window"
3. Select "Remote-WSL: New Window"

### Step 13: Open Project in WSL
1. Select "Open Project"
2. Navigate to your WSL projects directory: `/home/[username]/projects/agents`
3. Click "Open" or "Select Folder"

### Step 14: Install Python Extensions in WSL
1. Go to Extensions (Ctrl+Shift+X)
2. Install these extensions in WSL:
   - Python (ms-python)
   - Jupyter (microsoft)
3. Click "Install in WSL-Ubuntu" for each

## Part 4: Environment Setup

### Step 15: Create .env File
Create a `.env` file in the agents directory with your API keys:
```bash
touch .env
nano .env
```

Add your environment variables:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
# Add other API keys as needed
```

### Step 16: Select Python Kernel
1. Open any Python file or Jupyter notebook
2. Click "Select Kernel"
3. Choose "Python Environment..."
4. Select the uv-managed environment

## Common Issues and Solutions

### Issue 1: Wrong Environment
**Problem:** Running commands in Windows PowerShell instead of WSL
**Solution:** Always use `ubuntu` command to access WSL environment

### Issue 2: curl Command Error
**Problem:** `curl: option -LsSF: is badly used here`
**Solution:** Use `-LsSf` (lowercase f), not `-LsSF` (uppercase F)

### Issue 3: PATH Not Updated
**Problem:** `uv: command not found` after installation
**Solution:** Run `source $HOME/.local/bin/env` or restart WSL

### Issue 4: Wrong Directory
**Problem:** Trying to access Windows paths in WSL
**Solution:** Use WSL paths: `/home/[username]/` instead of `C:\Users\...`

### Issue 5: Permission Denied
**Problem:** `Permission denied` errors
**Solution:** Use `sudo` for system-level operations

## Verification Checklist

- [ ] WSL Ubuntu installed and accessible
- [ ] uv installed and working (`uv --version`)
- [ ] Repository cloned successfully
- [ ] Dependencies installed (`uv sync` completed)
- [ ] Cursor configured for WSL
- [ ] Python extensions installed in WSL
- [ ] .env file created with API keys
- [ ] Python kernel selected in Cursor

## Notes

- WSL provides a Linux environment within Windows
- All AI agent work should be done in the WSL environment
- The Windows file system is accessible at `/mnt/c/` in WSL
- Use `exit` to return to Windows PowerShell from WSL
- Use `ubuntu` to return to WSL from Windows PowerShell

## Troubleshooting Commands

```bash
# Check WSL status
wsl --list --verbose

# Restart WSL
wsl --shutdown
wsl

# Check disk space
df -h

# Check memory usage
free -h

# Update Ubuntu packages
sudo apt update && sudo apt upgrade
```

This guide should help you set up WSL on any Windows machine for AI agent development. 