# Quick Start Guide - Deploy in 5 Minutes

Get your first production AI agent running in under 5 minutes with our streamlined deployment process.

## Prerequisites ⚡

Before you begin, ensure you have:

- [ ] Docker and Docker Compose installed
- [ ] Git installed
- [ ] OpenAI API key (or alternative LLM provider)
- [ ] 5 minutes of your time

## Option 1: One-Command Deploy 🚀

The fastest way to get started:

```bash
# Install the Agentically CLI
pip install agentically-deploy

# Deploy your first agent (customer support example)
agentically deploy customer-support --provider local

# Your agent will be available at: http://localhost:8080
```

## Option 2: Manual Setup 🛠️

### Step 1: Clone and Navigate

```bash
git clone https://github.com/agenticallysh/production-agent-templates.git
cd production-agent-templates/templates/customer-support
```

### Step 2: Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys (use your favorite editor)
nano .env
```

**Required environment variables:**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Agent Configuration
AGENT_NAME="Your Company Support"
AGENT_DESCRIPTION="24/7 AI customer support"

# Optional: Advanced Features
ENABLE_MONITORING=true
ENABLE_ANALYTICS=true
```

### Step 3: Launch with Docker

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

### Step 4: Verify Deployment

```bash
# Test the API endpoint
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help with my order"}'

# Expected response:
# {
#   "response": "Hello! I'd be happy to help you with your order...",
#   "session_id": "session_123...",
#   "timestamp": "2024-10-30T..."
# }
```

## Step 5: Access Your Agent 🎉

### Web Interface
Open http://localhost:8080 in your browser for the complete chat interface.

### API Access
Your agent is now available via REST API:

```bash
# Health check
curl http://localhost:8080/health

# Chat endpoint
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Your message here"}'

# Conversation history
curl http://localhost:8080/api/conversations/session_id
```

### Monitoring Dashboard
Visit http://localhost:3000 for Grafana monitoring dashboard (if enabled).

## Common Use Cases 💡

### Customer Support Agent
```bash
# Deploy customer support template
agentically deploy customer-support --provider local

# Test with support queries
curl -X POST http://localhost:8080/api/chat \
  -d '{"message": "I need to return a product"}'
```

### Content Generation
```bash
# Deploy content pipeline template  
agentically deploy content-pipeline --provider local

# Generate blog content
curl -X POST http://localhost:8080/api/generate \
  -d '{"type": "blog", "topic": "AI in customer service"}'
```

### Data Analysis
```bash
# Deploy data analysis template
agentically deploy data-analysis --provider local

# Upload and analyze data
curl -X POST http://localhost:8080/api/analyze \
  -F "file=@data.csv" \
  -F "analysis_type=trends"
```

## Customization Quick Tips 🎨

### Change Agent Personality
Edit `app/config/agent_config.yaml`:

```yaml
personality:
  tone: "friendly and professional"
  style: "concise and helpful"
  expertise_areas:
    - "customer service"
    - "product support"
    - "technical troubleshooting"
```

### Add Custom Tools
Create `app/tools/custom_tool.py`:

```python
from crewai_tools import BaseTool

class CustomTool(BaseTool):
    name: str = "custom_tool"
    description: str = "Your custom tool description"
    
    def _run(self, query: str) -> str:
        # Your custom logic here
        return f"Processed: {query}"
```

### Environment-Specific Config
```bash
# Development
cp .env.development .env

# Staging  
cp .env.staging .env

# Production
cp .env.production .env
```

## Troubleshooting 🔧

### Port Already in Use
```bash
# Check what's using the port
lsof -i :8080

# Use different port
export PORT=8081
docker-compose up -d
```

### API Key Issues
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Container Issues
```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Memory Issues
```bash
# Check container memory usage
docker stats

# Increase memory limits in docker-compose.yml
# mem_limit: 2g
```

## Performance Optimization ⚡

### For Development
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  agent:
    environment:
      - DEBUG=true
      - HOT_RELOAD=true
    volumes:
      - ./app:/app  # Enable hot reload
```

### For Production
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  agent:
    environment:
      - DEBUG=false
      - WORKERS=4
      - MAX_REQUESTS_PER_WORKER=1000
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
```

## Next Steps 🚀

Now that your agent is running, you can:

1. **[Customize Your Agent](./customization.md)** - Adapt it to your specific needs
2. **[Deploy to Production](./deployment.md)** - Scale to handle real traffic  
3. **[Set Up Monitoring](./monitoring.md)** - Track performance and usage
4. **[API Integration](./api.md)** - Integrate with your existing systems
5. **[Advanced Configuration](./advanced.md)** - Unlock advanced features

## Template Gallery 🎨

Explore other templates:

```bash
# List all available templates
agentically list-templates

# Quick deploy other templates
agentically deploy data-analysis --provider local
agentically deploy content-pipeline --provider local  
agentically deploy code-review --provider local
```

## Community & Support 💬

### Get Help
- **Discord**: [Join our community](https://discord.gg/agentically) for real-time help
- **GitHub Issues**: [Report bugs or request features](https://github.com/agenticallysh/production-agent-templates/issues)
- **Documentation**: Browse our [complete docs](https://docs.agentically.sh)

### Share Your Success
- **Twitter**: Share your agent with [@agenticallysh](https://twitter.com/agenticallysh)
- **Discord**: Show off in #success-stories
- **Blog**: Write about your experience

---

**🎉 Congratulations!** You now have a production-ready AI agent running. The template includes everything you need: error handling, monitoring, scaling, and security - all configured and ready to go.

*Need help? Join our [Discord community](https://discord.gg/agentically) for instant support.*