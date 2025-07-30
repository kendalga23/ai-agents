import asyncio
import requests
from bs4 import BeautifulSoup
from typing import Annotated, TypedDict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import Tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables
load_dotenv(override=True)

class State(TypedDict):
    messages: Annotated[list, add_messages]

# Push notification tool (same as in notebook)
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_user = os.getenv("PUSHOVER_USER")
pushover_url = "https://api.pushover.net/1/messages.json"

def push(text: str):
    """Send a push notification to the user"""
    if pushover_token and pushover_user:
        requests.post(pushover_url, data={
            "token": pushover_token, 
            "user": pushover_user, 
            "message": text
        })
        return f"Push notification sent: {text}"
    else:
        return "Push notification not configured (missing PUSHOVER_TOKEN or PUSHOVER_USER)"

# Web browsing tools using requests instead of Playwright
def browse_website(url: str):
    """Browse a website and return its content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Limit text length to avoid token limits
        if len(text) > 8000:
            text = text[:8000] + "... [Content truncated]"
        
        return f"Successfully browsed {url}\n\nContent:\n{text}"
    except Exception as e:
        return f"Error browsing {url}: {str(e)}"

def search_web(query: str):
    """Search the web using a simple approach (you can replace with actual search API)"""
    try:
        # This is a placeholder - you can integrate with actual search APIs
        # For now, we'll return a mock response
        return f"Search results for '{query}':\n\nThis is a placeholder search result. To implement real web search, you would need to integrate with services like:\n- Google Custom Search API\n- Bing Search API\n- DuckDuckGo API\n- SerpAPI\n\nFor now, you can use the browse_website tool with specific URLs."
    except Exception as e:
        return f"Error searching for '{query}': {str(e)}"

def extract_links(url: str):
    """Extract all links from a website"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        
        link_list = []
        for link in links[:20]:  # Limit to first 20 links
            href = link['href']
            text = link.get_text().strip()
            if href.startswith('http'):
                link_list.append(f"- {text}: {href}")
        
        return f"Links found on {url}:\n\n" + '\n'.join(link_list)
    except Exception as e:
        return f"Error extracting links from {url}: {str(e)}"

# Create tools
tool_push = Tool(
    name="send_push_notification",
    func=push,
    description="useful for when you want to send a push notification to the user's device"
)

tool_browse = Tool(
    name="browse_website",
    func=browse_website,
    description="useful for browsing websites and getting their content. Input should be a URL."
)

tool_search = Tool(
    name="search_web",
    func=search_web,
    description="useful for searching the web for information. Input should be a search query."
)

tool_links = Tool(
    name="extract_links",
    func=extract_links,
    description="useful for extracting all links from a website. Input should be a URL."
)

# Combine all tools
all_tools = [tool_push, tool_browse, tool_search, tool_links]

def create_web_agent():
    """Create and return a web browsing agent"""
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(all_tools)
    
    # Define chatbot function
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    
    # Build the graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", ToolNode(tools=all_tools))
    graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    
    # Compile with memory
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    
    return graph

async def chat_with_agent(user_input: str, thread_id: str = "default"):
    """Chat with the web browsing agent"""
    graph = create_web_agent()
    config = {"configurable": {"thread_id": thread_id}}
    
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]}, 
        config=config
    )
    
    return result["messages"][-1].content

def main():
    """Main function to run the agent interactively"""
    print("🌐 Local Web Browsing Agent")
    print("=" * 50)
    print("Available tools:")
    print("- browse_website: Browse any website")
    print("- search_web: Search the web")
    print("- extract_links: Extract links from a website")
    print("- send_push_notification: Send push notifications")
    print("\nType 'quit' to exit")
    print("-" * 50)
    
    thread_id = "local_session"
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAgent is thinking...")
            response = asyncio.run(chat_with_agent(user_input, thread_id))
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main() 