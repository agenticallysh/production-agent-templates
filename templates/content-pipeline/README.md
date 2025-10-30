# Content Pipeline Agent Template

## Overview

Production-ready AI agent system for automated content creation, optimization, and multi-platform publishing. Built with CrewAI for coordinated content workflows between research, writing, editing, and publishing agents.

## Quick Deploy

```bash
# Clone and deploy
git clone https://github.com/agenticallysh/production-agent-templates.git
cd production-agent-templates/templates/content-pipeline
docker-compose up -d

# Your content pipeline API will be available at: http://localhost:8080
```

## Features

- **✍️ Multi-Format Content**: Blog posts, social media, newsletters, documentation
- **🔍 Research Integration**: Automated fact-checking and source gathering
- **📝 SEO Optimization**: Keyword research and content optimization
- **🎨 Multi-Platform Publishing**: WordPress, Medium, LinkedIn, Twitter/X
- **📊 Performance Tracking**: Analytics and engagement monitoring
- **🔄 Content Workflows**: Draft → Review → Approve → Publish pipelines

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Research   │───▶│   Content    │───▶│   Editor     │───▶│  Publisher   │
│   Agent      │    │   Writer     │    │   Agent      │    │   Agent      │
│              │    │              │    │              │    │              │
│ • Topic      │    │ • Drafting   │    │ • Review     │    │ • Platform   │
│   research   │    │ • Structure  │    │ • SEO opt    │    │   publishing │
│ • Fact check │    │ • Voice/tone │    │ • Quality    │    │ • Scheduling │
│ • Sources    │    │ • Citations  │    │   control    │    │ • Analytics  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Agent Roles

### Research Agent
- **Role**: Content research and fact-checking specialist  
- **Tools**: Web search, academic databases, trend analysis
- **Responsibilities**:
  - Topic research and trend analysis
  - Fact verification and source gathering
  - Competitive content analysis
  - SEO keyword research

### Content Writer Agent
- **Role**: Creative writing and content creation expert
- **Tools**: Writing templates, style guides, grammar checkers
- **Responsibilities**:
  - Draft creation in multiple formats
  - Tone and voice consistency
  - Content structure optimization
  - Citation and reference integration

### Editor Agent
- **Role**: Quality assurance and optimization specialist
- **Tools**: Grammar checkers, SEO tools, readability analyzers
- **Responsibilities**:
  - Content review and editing
  - SEO optimization
  - Quality control checks
  - Brand guidelines compliance

### Publisher Agent  
- **Role**: Multi-platform publishing and distribution expert
- **Tools**: CMS APIs, social media APIs, scheduling tools
- **Responsibilities**:
  - Content formatting for different platforms
  - Automated publishing workflows
  - Content scheduling and distribution
  - Performance tracking setup

## API Endpoints

### Create Content Project
```bash
curl -X POST http://localhost:8080/api/content/create \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI in Customer Service",
    "content_types": ["blog_post", "social_media", "newsletter"],
    "target_platforms": ["wordpress", "linkedin", "twitter"],
    "deadline": "2024-11-01T10:00:00Z"
  }'
```

### Get Content Status
```bash
curl http://localhost:8080/api/content/{project_id}/status
```

### Review and Approve Content
```bash
curl -X POST http://localhost:8080/api/content/{project_id}/approve \
  -H "Content-Type: application/json" \
  -d '{
    "stage": "final_review",
    "approved": true,
    "feedback": "Looks great, ready to publish"
  }'
```

### Schedule Publishing
```bash
curl -X POST http://localhost:8080/api/content/{project_id}/schedule \
  -H "Content-Type: application/json" \
  -d '{
    "publish_times": {
      "blog_post": "2024-11-01T09:00:00Z",
      "social_media": "2024-11-01T12:00:00Z"
    }
  }'
```

## Configuration

### Environment Variables

```bash
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Content Settings
DEFAULT_VOICE_TONE=professional_friendly
SEO_OPTIMIZATION_LEVEL=high
FACT_CHECK_REQUIRED=true
PLAGIARISM_CHECK=true

# Platform Integration
WORDPRESS_API_URL=https://your-site.com/wp-json/wp/v2
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_app_password

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/content_pipeline
REDIS_URL=redis://localhost:6379/0
```

### Content Configuration

```yaml
# app/config/content_config.yaml
content_types:
  blog_post:
    min_words: 800
    max_words: 2500
    required_sections: ['introduction', 'main_content', 'conclusion']
    seo_keywords: 3-5
    internal_links: 2-4
    
  social_media:
    platforms:
      twitter:
        max_chars: 280
        hashtags: 3-5
      linkedin:
        max_chars: 3000
        professional_tone: true
      
  newsletter:
    sections: ['header', 'main_content', 'cta', 'footer']
    personalization: true
    
writing_guidelines:
  voice: "professional yet approachable"
  tone: "informative and engaging"
  reading_level: "grade_8"
  
seo_settings:
  keyword_density: "1-3%"
  meta_description_length: "150-160"
  title_length: "50-60"
  heading_structure: "h1,h2,h3"
```

## Usage Examples

### Blog Post Creation

```python
import requests

# Create blog post project
response = requests.post(
    'http://localhost:8080/api/content/create',
    json={
        'topic': 'The Future of Remote Work',
        'content_types': ['blog_post'],
        'target_audience': 'business_professionals',
        'seo_keywords': ['remote work', 'digital transformation', 'productivity'],
        'word_count': 1500
    }
)

project_id = response.json()['project_id']

# Monitor progress
status = requests.get(f'http://localhost:8080/api/content/{project_id}/status')
print(f"Status: {status.json()['current_stage']}")

# Review generated content
content = requests.get(f'http://localhost:8080/api/content/{project_id}/draft')
print(content.json()['content'])
```

### Multi-Platform Campaign

```bash
# Create comprehensive content campaign
curl -X POST http://localhost:8080/api/content/campaign \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "Product Launch Q4",
    "main_topic": "New AI Features Release",
    "content_calendar": [
      {
        "date": "2024-11-01",
        "content_type": "blog_post",
        "platforms": ["wordpress", "medium"]
      },
      {
        "date": "2024-11-02", 
        "content_type": "social_media",
        "platforms": ["linkedin", "twitter"]
      },
      {
        "date": "2024-11-05",
        "content_type": "newsletter", 
        "platforms": ["mailchimp"]
      }
    ]
  }'
```

### Automated SEO Content

```bash
# Generate SEO-optimized content
curl -X POST http://localhost:8080/api/content/seo-optimized \
  -H "Content-Type: application/json" \
  -d '{
    "target_keywords": ["AI automation", "business efficiency"],
    "competitor_urls": ["https://competitor1.com/ai-article"],
    "content_type": "blog_post",
    "optimize_for": "google_ranking"
  }'
```

## Content Templates

### Blog Post Template

```markdown
# {{ title }}

## Introduction
{{ hook_paragraph }}

{{ problem_statement }}

## Main Content
### {{ section_1_title }}
{{ section_1_content }}

### {{ section_2_title }}  
{{ section_2_content }}

### {{ section_3_title }}
{{ section_3_content }}

## Conclusion
{{ summary_paragraph }}

{{ call_to_action }}

---
**Meta Description**: {{ meta_description }}
**Keywords**: {{ primary_keywords }}
**Word Count**: {{ word_count }}
```

### Social Media Templates

```yaml
# templates/social_media.yaml
twitter:
  format: |
    {{ hook_line }}
    
    {{ key_points }}
    
    {{ hashtags }}
    {{ link }}
    
linkedin:
  format: |
    {{ professional_intro }}
    
    {{ detailed_content }}
    
    What's your experience with {{ topic }}?
    
    {{ hashtags }}
    
instagram:
  format: |
    {{ visual_description }}
    
    {{ engaging_caption }}
    
    {{ hashtags }}
```

## Workflow Stages

### 1. Research Stage
- Topic analysis and trend research
- Competitor content analysis  
- SEO keyword research
- Fact-checking and source gathering

### 2. Content Creation Stage
- Initial draft generation
- Structure optimization
- Voice and tone application
- Citation integration

### 3. Review and Editing Stage
- Grammar and style checking
- SEO optimization
- Brand guidelines compliance
- Quality assurance

### 4. Approval Stage
- Stakeholder review
- Feedback incorporation
- Final approval workflow
- Legal/compliance checks

### 5. Publishing Stage
- Platform-specific formatting
- Scheduled publishing
- Cross-platform distribution
- Performance tracking setup

## Platform Integrations

### WordPress Integration

```python
# app/publishers/wordpress_publisher.py
class WordPressPublisher:
    def __init__(self, site_url, username, password):
        self.api_url = f"{site_url}/wp-json/wp/v2"
        self.auth = (username, password)
    
    def publish_post(self, content, title, excerpt=None):
        post_data = {
            'title': title,
            'content': content,
            'excerpt': excerpt,
            'status': 'publish'
        }
        
        response = requests.post(
            f"{self.api_url}/posts",
            json=post_data,
            auth=self.auth
        )
        return response.json()
```

### Social Media Integration

```python
# app/publishers/social_publisher.py
class SocialMediaPublisher:
    def publish_to_linkedin(self, content, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        post_data = {
            'author': 'urn:li:person:PERSON_ID',
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {'text': content},
                    'shareMediaCategory': 'NONE'
                }
            }
        }
        
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            json=post_data,
            headers=headers
        )
        return response.json()
```

## Analytics and Performance

### Content Performance Metrics

```python
# app/analytics/performance_tracker.py
class ContentAnalytics:
    def track_performance(self, content_id, platform):
        metrics = {
            'views': self.get_page_views(content_id, platform),
            'engagement': self.get_engagement_rate(content_id, platform),
            'shares': self.get_share_count(content_id, platform),
            'conversions': self.get_conversion_rate(content_id, platform)
        }
        return metrics
    
    def generate_report(self, campaign_id):
        # Generate comprehensive performance report
        pass
```

### Dashboard Metrics

- **Content Production**: Posts per week, time to publish
- **Engagement**: Views, likes, shares, comments
- **SEO Performance**: Keyword rankings, organic traffic
- **Conversion**: Click-through rates, lead generation

## Customization

### Custom Content Types

```python
# app/content_types/custom_type.py
from app.agents import ContentWriter

class TechnicalDocumentationWriter(ContentWriter):
    def __init__(self):
        super().__init__()
        self.content_type = "technical_documentation"
        self.writing_style = "technical_precise"
    
    def create_content(self, topic, specifications):
        # Custom logic for technical documentation
        sections = self.plan_documentation_structure(topic)
        content = self.write_technical_content(sections, specifications)
        return self.format_documentation(content)
```

### Custom Publishing Platforms

```python
# app/publishers/custom_publisher.py
class CustomPlatformPublisher:
    def __init__(self, api_config):
        self.api_config = api_config
    
    def publish(self, content, metadata):
        # Custom publishing logic
        formatted_content = self.format_for_platform(content)
        response = self.send_to_platform(formatted_content, metadata)
        return response
```

## Deployment

### Docker Compose (Development)

```yaml
version: '3.8'
services:
  content-pipeline:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/content_pipeline
    depends_on:
      - db
      - redis
      - scheduler
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: content_pipeline
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    
  scheduler:
    image: agentically/content-scheduler:latest
    depends_on:
      - redis

volumes:
  postgres_data:
```

### Kubernetes (Production)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: content-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: content-pipeline
  template:
    metadata:
      labels:
        app: content-pipeline
    spec:
      containers:
      - name: content-pipeline
        image: agentically/content-pipeline:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

## Quality Assurance

### Content Quality Checks

```python
# app/quality/content_checker.py
class ContentQualityChecker:
    def check_content(self, content):
        results = {
            'grammar_score': self.check_grammar(content),
            'readability_score': self.check_readability(content),
            'seo_score': self.check_seo_optimization(content),
            'originality_score': self.check_plagiarism(content),
            'brand_compliance': self.check_brand_guidelines(content)
        }
        return results
    
    def meets_quality_standards(self, results):
        return all(score >= 0.8 for score in results.values())
```

### Automated Testing

```bash
# Run content quality tests
pytest tests/content_quality/

# Test publishing workflows
pytest tests/publishing/

# Test platform integrations
pytest tests/integrations/
```

## Troubleshooting

### Common Issues

**Content Generation Slow**
```bash
# Optimize model selection
export CONTENT_MODEL=gpt-3.5-turbo-16k
export ENABLE_CONTENT_CACHING=true
```

**Publishing Failures**
```bash
# Check platform credentials
python scripts/test_platform_connections.py

# Verify API limits
export RATE_LIMIT_BUFFER=0.8
```

**SEO Optimization Issues**
```bash
# Update SEO configuration
export SEO_API_KEY=your_semrush_api_key
export ENABLE_ADVANCED_SEO=true
```

## Performance Optimization

### Content Generation Speed

```python
# app/config/performance.py
PERFORMANCE_CONFIG = {
    'parallel_agent_execution': True,
    'content_caching': True,
    'template_preloading': True,
    'batch_processing': True
}
```

### Publishing Efficiency

```yaml
# docker-compose.prod.yml  
services:
  content-pipeline:
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
    environment:
      - WORKER_PROCESSES=4
      - ASYNC_PUBLISHING=true
```

## Security

- **Content Encryption**: All drafts encrypted at rest
- **API Authentication**: JWT tokens for all endpoints
- **Platform Security**: OAuth 2.0 for social media integrations
- **Content Approval**: Multi-stage approval workflows

## Support

- **Documentation**: [Content API docs](./docs/api.md)
- **Templates**: [Content templates](./templates/)
- **Discord**: [Community support](https://discord.gg/agentically)
- **GitHub**: [Issues and discussions](https://github.com/agenticallysh/production-agent-templates/issues)

---

**🚀 Ready to automate your content?** Follow the [Quick Start Guide](../../docs/quickstart.md) to deploy your content pipeline in 4 minutes.