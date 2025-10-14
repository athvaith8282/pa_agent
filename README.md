# PA Agent - Personal Assistant Agent

A sophisticated AI-powered personal assistant built with LangGraph and Streamlit, featuring multi-tool integration, Gmail connectivity, and specialized F1 data capabilities.

## 🔗 Live Demo

Try it now on Streamlit Community: [PA Agent – Live Demo](https://personal-assistent.streamlit.app/)

## 🚀 Features

### Core Architecture
- **LangGraph Integration**: Built on LangGraph for advanced agent orchestration and workflow management
- **Streamlit Frontend**: Modern, interactive web interface for seamless user experience
- **Async SQLite Memory**: Persistent conversation history with thread-based chat management
- **Google Gemini Integration**: Powered by Google's latest generative AI models

### Multi-Tool Ecosystem
- **Gmail Integration**: Full Gmail API access for email management and automation
- **Web Search**: Real-time web search capabilities via Tavily API
- **F1 Data Tools**: Custom MCP server integration for Formula 1 race data, driver standings, and constructor championships
- **RAG System**: Retrieval-Augmented Generation with health blog posts and PDF document processing
- **Task Management**: Built-in TODO list functionality with status tracking and execution planning

### Advanced Capabilities
- **Document Processing**: PDF upload and semantic chunking for health-related content
- **Vector Database**: ChromaDB integration with Google Generative AI embeddings
- **OAuth Authentication**: Secure Google OAuth2 integration for Gmail access
- **Real-time Streaming**: Live response streaming with tool execution visibility
- **Conversation Persistence**: Thread-based chat history with easy conversation switching

## 🏗️ Architecture

```
PA Agent
├── Frontend (Streamlit)
├── LangGraph Agent Core
├── Tool Integration Layer
│   ├── Gmail Tools
│   ├── F1 MCP Server
│   ├── Web Search (Tavily)
│   ├── RAG System (ChromaDB)
│   └── Task Management
└── Memory & State Management
```

## 🛠️ Technology Stack

### Core Framework
- **LangGraph**: Agent orchestration and workflow management
- **Streamlit**: Web application framework
- **LangChain**: LLM framework and tool integration

### AI & ML
- **Google Gemini**: Primary language model
- **Google Generative AI Embeddings**: Vector embeddings for RAG
- **ChromaDB**: Vector database for document retrieval

### Integrations & APIs
- **Gmail API**: Email management and automation
- **Tavily API**: Web search capabilities
- **MCP (Model Context Protocol)**: Custom F1 data server
- **Google OAuth2**: Secure authentication

### Data & Storage
- **SQLite**: Conversation persistence and state management
- **ChromaDB**: Vector storage for document embeddings
- **Async Operations**: Full async/await support for performance

## 📋 Prerequisites

- Python 3.11+
- Google Gemini API key
- Tavily API key (for web search)
- Google OAuth2 credentials (for Gmail integration)

## 🚀 Installation

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PA_AGENT
   ```

2. **Set up secrets configuration**
   ```bash
   # Create secrets.toml file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your API keys
   ```
   
   The `secrets.toml` file should contain:
   ```toml
   [LANGFUSE]
   LANGFUSE_PUBLIC_KEY="your_langfuse_public_key"
   LANGFUSE_SECRET_KEY="your_langfuse_secret_key"
   LANGFUSE_HOST="https://us.cloud.langfuse.com"
   
   [TAVILY]
   TAVILY_API_KEY="your_tavily_api_key"
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:8501`
   
   **Note**: Google Gemini API key and Gmail OAuth credentials are configured through the Streamlit UI when you first run the application.

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PA_AGENT
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up secrets configuration**
   ```bash
   # Create secrets.toml file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your API keys
   ```
   
   **Note**: Google Gemini API key and Gmail OAuth credentials are configured through the Streamlit UI.

4. **Run the application**
   ```bash
   uv run streamlit run main.py
   ```

## 🐳 Docker Deployment

### Quick Start with Docker

The easiest way to run PA Agent is using Docker Compose:

```bash
# Clone and setup
git clone <repository-url>
cd PA_AGENT

# Set up secrets configuration
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your API keys

# Run with Docker Compose
docker-compose up --build
```

### Docker Commands

```bash
# Build the image
docker build -t pa-agent .

# Run the container (secrets.toml must be configured first)
docker run -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/.streamlit:/app/.streamlit \
  pa-agent

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild after code changes
docker-compose up --build --force-recreate
```

### Docker Features

- **Persistent Data**: Database and uploaded files persist between container restarts
- **Health Checks**: Automatic health monitoring and restart on failure
- **Optimized Build**: Multi-stage build with minimal image size
- **Security**: Non-root user and minimal attack surface
- **Environment Isolation**: Clean environment with all dependencies included

## ⚙️ Configuration

### Secrets Management

PA Agent uses Streamlit's `secrets.toml` file for configuration:

1. **Required Secrets** (in `secrets.toml`):
   - `LANGFUSE_PUBLIC_KEY` & `LANGFUSE_SECRET_KEY`: For observability and monitoring
   - `TAVILY_API_KEY`: For web search functionality

2. **UI-Configured Secrets**:
   - **Google Gemini API Key**: Entered through the Streamlit UI when first launching
   - **Gmail OAuth Credentials**: Configured through the UI when enabling Gmail features

### Configuration Files

```toml
# .streamlit/secrets.toml
[LANGFUSE]
LANGFUSE_PUBLIC_KEY="your_langfuse_public_key"
LANGFUSE_SECRET_KEY="your_langfuse_secret_key"
LANGFUSE_HOST="https://us.cloud.langfuse.com"

[TAVILY]
TAVILY_API_KEY="your_tavily_api_key"
```

## 🎯 Usage

### Getting Started
1. Launch the application and enter your Google Gemini API key through the UI
2. Start a new chat or continue from previous conversations
3. Upload PDF documents for health-related queries
4. Authorize Gmail access for email management features (optional)

### Key Features in Action

#### Gmail Integration
- **Email Management**: Read, compose, and manage emails through natural language
- **Smart Filtering**: Intelligent email organization and search
- **Automated Responses**: Context-aware email responses

#### F1 Data Access
- **Race Information**: Get race schedules, dates, and times for any year
- **Driver Standings**: Current and historical driver championship standings
- **Constructor Championships**: Team standings and constructor points

#### Document Processing
- **PDF Upload**: Upload health-related PDFs with custom descriptions
- **Semantic Search**: Ask questions about uploaded documents
- **Health Insights**: Get personalized health advice based on uploaded content

#### Task Management
- **Smart Planning**: AI-powered task planning and execution
- **Progress Tracking**: Real-time TODO list updates with status indicators
- **Workflow Automation**: Multi-step task execution with intermediate updates

## 🔧 Configuration

### MCP Server Setup
The F1 MCP server runs as a separate process:
```bash
# F1 MCP Server Configuration
{
    "F1_MCP": {
        'command': 'uv',
        'args': ['run', 'python', 'my_mcp/mcp_server.py'],
        'transport': 'stdio'
    }
}
```

### Vector Database
- **Collection**: `banner_health_blogs`
- **Embedding Model**: `models/gemini-embedding-001`
- **Persistence**: ChromaDB with local storage

## 📁 Project Structure

```
PA_AGENT/
├── main.py                 # Streamlit application entry point
├── pa_agent.py            # LangGraph agent implementation
├── my_tools.py            # Tool definitions and integrations
├── config.py              # Configuration and constants
├── mystate.py             # Agent state management
├── llms.py                # LLM configuration
├── db.py                  # Database utilities
├── utils.py               # Utility functions
├── my_mcp/                # MCP server for F1 data
│   ├── mcp_server.py      # MCP server entry point
│   ├── f1_tools.py        # F1-specific tools
│   └── mcp_config.py      # MCP configuration
├── retriever/             # RAG system
│   ├── retriever_main.py  # Document processing
│   └── data/              # Uploaded documents
├── data/                  # Application data
│   ├── db/                # SQLite database
│   ├── vectordb/          # ChromaDB storage
│   └── google_tokens/     # OAuth tokens
└── logs/                  # Application logs
```

## 🔍 Key Components

### LangGraph Agent (`pa_agent.py`)
- **State Management**: Handles conversation state and tool execution
- **Memory Integration**: Persistent conversation history with SQLite
- **Tool Orchestration**: Manages multiple tool types and execution flow
- **Streaming Support**: Real-time response streaming with tool visibility

### Tool Ecosystem (`my_tools.py`)
- **Gmail Tools**: Complete email management suite
- **F1 Tools**: Race data, standings, and championship information
- **RAG Tools**: Document retrieval and health content search
- **Task Tools**: TODO list management and execution tracking
- **Utility Tools**: Date/time, web search capabilities

### MCP Integration (`my_mcp/`)
- **Custom Server**: F1 data API integration via MCP protocol
- **Async Operations**: Non-blocking API calls with error handling
- **Data Processing**: Structured F1 data extraction and formatting

### RAG System (`retriever/`)
- **Document Processing**: PDF parsing with semantic chunking
- **Vector Storage**: ChromaDB integration with embedding generation
- **Status Tracking**: Document processing status and metadata management

## 🚀 Advanced Features

### Real-time Streaming
- Live token streaming for responsive user experience
- Tool execution visibility with input/output display
- TODO list updates with status indicators
- Progress tracking for complex multi-step operations

### Conversation Management
- Thread-based chat history
- Conversation switching and resumption
- Persistent state across sessions
- Context-aware responses with memory

### Security & Authentication
- OAuth2 integration for Gmail access
- Secure token management and refresh
- API key protection and environment-based configuration

## 🎯 Use Cases

### Personal Productivity
- Email management and automation
- Task planning and execution
- Document analysis and insights
- Information retrieval and synthesis

### Health & Wellness
- Health document analysis
- Personalized health insights
- Medical information retrieval
- Wellness planning and tracking

### F1 Enthusiast
- Race schedule and results
- Championship standings tracking
- Historical F1 data analysis
- Real-time F1 information

## 🔧 Troubleshooting

### Docker Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs pa-agent

# Rebuild from scratch
docker-compose down
docker system prune -f
docker-compose up --build
```

**Permission issues with data directory:**
```bash
# Fix permissions
sudo chown -R $USER:$USER data/
chmod -R 755 data/
```

**API key not working:**
- Ensure `secrets.toml` file is properly configured
- Check that API keys are valid and have proper permissions
- Verify `secrets.toml` file format (no spaces around `=`)
- For Google Gemini API key, ensure it's entered correctly through the UI

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use different external port
```

### Common Issues

**Gmail integration not working:**
- Verify OAuth2 credentials are correctly configured
- Check redirect URI matches: `http://localhost:8501/component/streamlit_oauth.authorize_button`
- Ensure Gmail API is enabled in Google Cloud Console

**F1 MCP server connection failed:**
- Check that MCP server is running correctly
- Verify stdio transport configuration
- Review logs for connection errors

**RAG system not finding documents:**
- Ensure PDFs are uploaded successfully
- Check ChromaDB is properly initialized
- Verify embedding model access

## 🔮 Future Enhancements

- **Multi-modal Support**: Image and document processing
- **Voice Integration**: Speech-to-text and text-to-speech
- **Calendar Integration**: Google Calendar and scheduling
- **Advanced Analytics**: Usage patterns and insights
- **Mobile Support**: Responsive design and mobile optimization

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👤 Author

**Athvaith**
- GitHub: [@athvaith8282](https://github.com/athvaith8282)
- LinkedIn: [Athvaith.K](https://www.linkedin.com/in/athvaith)
- Email: athvaith.k@gmail.com

## 📞 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using LangGraph, Streamlit, and modern AI technologies**
