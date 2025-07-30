#!/usr/bin/env python3
"""
Local Development Environment Switcher
Utility to switch back to local development environment
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

class LocalDevSwitcher:
    def __init__(self):
        self.config_file = Path(".local_dev_config.json")
        self.env_file = Path(".env")
        
    def save_current_config(self, name: str = "current"):
        """Save current environment configuration"""
        config = {
            "name": name,
            "timestamp": str(Path().stat().st_mtime),
            "environment_variables": dict(os.environ),
            "python_path": sys.executable,
            "working_directory": str(Path.cwd()),
            "git_branch": self._get_git_branch(),
            "git_remote": self._get_git_remote()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Saved current configuration as '{name}'")
        return config
    
    def switch_to_local(self, config_name: str = "local"):
        """Switch to local development environment"""
        print(f"🔄 Switching to local development environment...")
        
        # 1. Set local environment variables
        self._set_local_env_vars()
        
        # 2. Switch to local git branch (if exists)
        self._switch_to_local_branch()
        
        # 3. Update .env file for local development
        self._update_env_file()
        
        # 4. Install local dependencies
        self._install_local_deps()
        
        print("✅ Switched to local development environment!")
    
    def _set_local_env_vars(self):
        """Set environment variables for local development"""
        local_vars = {
            "ENVIRONMENT": "local",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
            "DATABASE_URL": "sqlite:///./local_dev.db",
            "REDIS_URL": "redis://localhost:6379",
            "API_BASE_URL": "http://localhost:8000",
            "FRONTEND_URL": "http://localhost:3000"
        }
        
        for key, value in local_vars.items():
            os.environ[key] = value
            print(f"  Set {key}={value}")
    
    def _switch_to_local_branch(self):
        """Switch to local development branch"""
        try:
            # Check if we're in a git repository
            result = subprocess.run(["git", "rev-parse", "--git-dir"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Try to switch to local branch
                local_branches = ["local", "dev", "development", "main", "master"]
                for branch in local_branches:
                    result = subprocess.run(["git", "checkout", branch], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"  Switched to git branch: {branch}")
                        return
                
                print("  No local branch found, staying on current branch")
        except Exception as e:
            print(f"  Git operation failed: {e}")
    
    def _update_env_file(self):
        """Update .env file for local development"""
        if not self.env_file.exists():
            self._create_env_file()
        else:
            self._backup_and_update_env()
    
    def _create_env_file(self):
        """Create a new .env file for local development"""
        env_content = """# Local Development Environment
ENVIRONMENT=local
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DATABASE_URL=sqlite:///./local_dev.db

# Redis
REDIS_URL=redis://localhost:6379

# API Configuration
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# OpenAI (replace with your key)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Pushover for notifications
PUSHOVER_TOKEN=your_pushover_token_here
PUSHOVER_USER=your_pushover_user_here
"""
        with open(self.env_file, 'w') as f:
            f.write(env_content)
        print("  Created new .env file for local development")
    
    def _backup_and_update_env(self):
        """Backup existing .env and update for local development"""
        backup_file = Path(".env.backup")
        if not backup_file.exists():
            with open(self.env_file, 'r') as src, open(backup_file, 'w') as dst:
                dst.write(src.read())
            print("  Backed up existing .env file")
        
        # Update .env with local settings
        self._create_env_file()
    
    def _install_local_deps(self):
        """Install local development dependencies"""
        requirements_files = [
            "requirements.txt",
            "requirements_local_agent.txt", 
            "pyproject.toml",
            "setup.py"
        ]
        
        for req_file in requirements_files:
            if Path(req_file).exists():
                try:
                    if req_file.endswith('.txt'):
                        subprocess.run([sys.executable, "-m", "pip", "install", "-r", req_file])
                        print(f"  Installed dependencies from {req_file}")
                    elif req_file == 'pyproject.toml':
                        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."])
                        print(f"  Installed package in editable mode")
                except Exception as e:
                    print(f"  Failed to install from {req_file}: {e}")
    
    def _get_git_branch(self) -> str:
        """Get current git branch"""
        try:
            result = subprocess.run(["git", "branch", "--show-current"], 
                                  capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            return "unknown"
    
    def _get_git_remote(self) -> str:
        """Get current git remote"""
        try:
            result = subprocess.run(["git", "remote", "get-url", "origin"], 
                                  capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except:
            return "unknown"
    
    def show_status(self):
        """Show current environment status"""
        print("📊 Current Environment Status:")
        print("=" * 40)
        
        # Environment
        print(f"Environment: {os.getenv('ENVIRONMENT', 'unknown')}")
        print(f"Debug Mode: {os.getenv('DEBUG', 'unknown')}")
        print(f"Log Level: {os.getenv('LOG_LEVEL', 'unknown')}")
        
        # Database
        print(f"Database URL: {os.getenv('DATABASE_URL', 'not set')}")
        
        # API
        print(f"API Base URL: {os.getenv('API_BASE_URL', 'not set')}")
        
        # Git
        print(f"Git Branch: {self._get_git_branch()}")
        print(f"Git Remote: {self._get_git_remote()}")
        
        # Python
        print(f"Python Path: {sys.executable}")
        print(f"Working Directory: {Path.cwd()}")

def main():
    """Main function"""
    switcher = LocalDevSwitcher()
    
    if len(sys.argv) < 2:
        print("Local Development Environment Switcher")
        print("=" * 40)
        print("Usage:")
        print("  python local_dev_switch.py switch    # Switch to local environment")
        print("  python local_dev_switch.py save      # Save current configuration")
        print("  python local_dev_switch.py status    # Show current status")
        return
    
    command = sys.argv[1].lower()
    
    if command == "switch":
        switcher.switch_to_local()
    elif command == "save":
        name = sys.argv[2] if len(sys.argv) > 2 else "current"
        switcher.save_current_config(name)
    elif command == "status":
        switcher.show_status()
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 