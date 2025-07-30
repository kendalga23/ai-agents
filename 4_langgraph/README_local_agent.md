# Local Web Browsing Agent

This is a Windows-compatible version of the web browsing agent from the LangGraph notebook, designed to work on your local machine without the Playwright compatibility issues.

## Features

- 🌐 **Web Browsing**: Browse any website and extract content using `requests` and `BeautifulSoup`
- 🔍 **Link Extraction**: Extract all links from websites
- 📱 **Push Notifications**: Send push notifications to your device (optional)
- 💬 **Conversational AI**: Powered by OpenAI's GPT models
- 🧠 **Memory**: Maintains conversation context across interactions
- 🖥️ **Windows Compatible**: No Playwright dependency issues

## Quick Start

### 1. Setup

Run the setup script to install dependencies and configure the environment:

```bash
python setup_local_agent.py
```

### 2. Configure Environment

Edit the `.env` file with your API keys:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for push notifications
PUSHOVER_TOKEN=your_pushover_token_here
PUSHOVER_USER=your_pushover_user_here
```

### 3. Run the Agent

```bash
python local_web_agent.py
```

## Available Tools

### 1. `browse_website`
Browse any website and extract its content.

**Example:**
```
You: Browse https://www.example.com and tell me what's on the homepage
```

### 2. `extract_links`
Extract all links from a website.

**Example:**
```
You: Extract all links from https://www.example.com
```

### 3. `search_web`
Search the web for information (placeholder - can be extended with real search APIs).

**Example:**
```
You: Search for "latest AI news"
```

### 4. `send_push_notification`
Send push notifications to your device (requires Pushover setup).

**Example:**
```
You: Send me a notification saying "Task completed!"
```

## Usage Examples

### Basic Web Browsing
```
You: Can you browse CNN.com and tell me the top headlines?
```

### Link Analysis
```
You: Go to GitHub.com and extract all the main navigation links
```

### Content Summarization
```
You: Browse https://www.wikipedia.org and summarize what you find
```

### Push Notifications
```
You: Send me a push notification when you're done browsing
```

## Integration in Your Code

You can also use the agent programmatically:

```python
from local_web_agent import chat_with_agent
import asyncio

# Chat with the agent
response = asyncio.run(chat_with_agent("Browse https://example.com", "my_session"))
print(response)
```

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**
   - Make sure you have a `.env` file with your OpenAI API key

2. **"Module not found" errors**
   - Run `python setup_local_agent.py` to install dependencies

3. **Website access issues**
   - Some websites may block automated requests
   - The agent uses a realistic user agent to minimize blocking

### Windows-Specific Notes

- This version avoids Playwright which has compatibility issues on Windows
- Uses `requests` and `BeautifulSoup` for web scraping instead
- No browser installation required

## Extending the Agent

### Adding New Tools

To add a new tool, create a function and wrap it with the `Tool` class:

```python
def my_custom_tool(input_text: str):
    """Your custom tool description"""
    # Your tool logic here
    return "Tool result"

tool_custom = Tool(
    name="my_custom_tool",
    func=my_custom_tool,
    description="Description of what this tool does"
)

# Add to all_tools list
all_tools.append(tool_custom)
```

### Adding Real Web Search

Replace the placeholder `search_web` function with a real search API:

```python
def search_web(query: str):
    """Search using Google Custom Search API"""
    # Implement your search logic here
    # Example: Google Custom Search, Bing Search, etc.
    pass
```

## Dependencies

- `langgraph`: For building the agent graph
- `langchain`: For LLM integration
- `langchain-openai`: For OpenAI model integration
- `requests`: For HTTP requests
- `beautifulsoup4`: For HTML parsing
- `python-dotenv`: For environment variable management

## License

This project is part of the AI Agents learning materials. 