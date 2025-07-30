#!/usr/bin/env python3
"""
Setup script for Local Web Agent
This script helps you set up the local web browsing agent on your Windows machine.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_local_agent.txt"
        ])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  No .env file found. Creating template...")
        with open(env_file, "w") as f:
            f.write("""# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Pushover credentials (optional - for push notifications)
PUSHOVER_TOKEN=your_pushover_token_here
PUSHOVER_USER=your_pushover_user_here
""")
        print("📝 Created .env template. Please edit it with your actual API keys.")
        return False
    
    # Check if OpenAI API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in .env file. Please add your OpenAI API key.")
        return False
    
    print("✅ Environment variables configured!")
    return True

def test_agent():
    """Test the agent with a simple query"""
    print("\n🧪 Testing the agent...")
    try:
        from local_web_agent import chat_with_agent
        import asyncio
        
        # Test with a simple query
        test_query = "Hello! Can you tell me what tools you have available?"
        print(f"Testing with: {test_query}")
        
        response = asyncio.run(chat_with_agent(test_query, "test_session"))
        print(f"✅ Agent response: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error testing agent: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Local Web Agent for Windows")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Setup failed at package installation step.")
        return
    
    # Step 2: Check environment
    if not check_env_file():
        print("⚠️  Please configure your .env file and run setup again.")
        return
    
    # Step 3: Test the agent
    if test_agent():
        print("\n🎉 Setup completed successfully!")
        print("\nTo run the agent:")
        print("python local_web_agent.py")
        print("\nOr import and use in your own code:")
        print("from local_web_agent import chat_with_agent")
    else:
        print("❌ Setup completed but agent test failed.")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main() 