# Code Review Agent Template

## Overview

Production-ready AI agent system for automated code review, pull request analysis, and code quality assurance. Built with AutoGen for multi-agent collaboration between static analysis, security review, and documentation agents.

## Quick Deploy

```bash
# Clone and deploy
git clone https://github.com/agenticallysh/production-agent-templates.git
cd production-agent-templates/templates/code-review
docker-compose up -d

# Your code review API will be available at: http://localhost:8080
```

## Features

- **🔍 Automated PR Analysis**: Comprehensive pull request reviews
- **🛡️ Security Scanning**: Vulnerability detection and security best practices
- **📊 Code Quality Metrics**: Complexity analysis, maintainability scores  
- **📚 Documentation Review**: API docs, comments, and README analysis
- **🔄 CI/CD Integration**: GitHub Actions, GitLab CI, Jenkins support
- **📈 Performance Analysis**: Code performance and optimization suggestions

## Architecture

```
┌────────────────┐    ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
│ Static Analysis│───▶│ Security       │───▶│ Documentation  │───▶│ Review         │
│ Agent          │    │ Review Agent   │    │ Agent          │    │ Coordinator    │
│                │    │                │    │                │    │                │
│ • Code quality │    │ • Vuln scan    │    │ • Doc coverage │    │ • Summary      │
│ • Complexity   │    │ • Best practice│    │ • API docs     │    │ • Scoring      │
│ • Standards    │    │ • Dependencies │    │ • Comments     │    │ • Approval     │
│ • Performance  │    │ • Secrets      │    │ • Examples     │    │ • Integration  │
└────────────────┘    └────────────────┘    └────────────────┘    └────────────────┘
```

## Agent Roles

### Static Analysis Agent
- **Role**: Code quality and structure analysis specialist
- **Tools**: AST parsers, linting tools, complexity analyzers
- **Responsibilities**:
  - Code structure and architecture review
  - Complexity and maintainability analysis
  - Coding standards compliance
  - Performance optimization suggestions

### Security Review Agent
- **Role**: Security vulnerability and best practices expert
- **Tools**: Security scanners, dependency checkers, SAST tools
- **Responsibilities**:
  - Vulnerability detection and assessment
  - Security best practices verification
  - Dependency security analysis
  - Secret and credential scanning

### Documentation Agent
- **Role**: Documentation quality and coverage specialist
- **Tools**: Doc parsers, coverage analyzers, style checkers
- **Responsibilities**:
  - Documentation coverage analysis
  - API documentation quality
  - Code comment adequacy
  - README and guide completeness

### Review Coordinator
- **Role**: Review orchestration and decision-making manager
- **Tools**: Review aggregation, scoring algorithms, reporting
- **Responsibilities**:
  - Agent coordination and workflow management
  - Review summary generation
  - Approval/rejection decisions
  - Integration with development platforms

## API Endpoints

### Submit Code for Review
```bash
curl -X POST http://localhost:8080/api/review/submit \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "pull_request": 123,
    "branch": "feature/new-feature",
    "review_type": "comprehensive"
  }'
```

### Get Review Status
```bash
curl http://localhost:8080/api/review/{review_id}/status
```

### Get Review Results
```bash
curl http://localhost:8080/api/review/{review_id}/results
```

### Webhook for PR Events
```bash
# GitHub webhook endpoint
curl -X POST http://localhost:8080/api/webhooks/github \
  -H "X-GitHub-Event: pull_request" \
  -H "Content-Type: application/json" \
  -d @github_webhook_payload.json
```

## Configuration

### Environment Variables

```bash
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# GitHub Integration
GITHUB_TOKEN=your_github_token
GITHUB_WEBHOOK_SECRET=your_webhook_secret
GITHUB_APP_ID=your_app_id
GITHUB_PRIVATE_KEY_PATH=/path/to/private-key.pem

# GitLab Integration (optional)
GITLAB_TOKEN=your_gitlab_token
GITLAB_WEBHOOK_SECRET=your_gitlab_webhook_secret

# Review Settings
AUTO_APPROVE_THRESHOLD=0.85
REQUIRE_SECURITY_PASS=true
REQUIRE_DOCS_COVERAGE=0.80
MAX_COMPLEXITY_SCORE=10

# Analysis Tools
ENABLE_SONARQUBE=true
SONARQUBE_URL=http://sonarqube:9000
SONARQUBE_TOKEN=your_sonar_token

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/code_review
REDIS_URL=redis://localhost:6379/0
```

### Review Configuration

```yaml
# app/config/review_config.yaml
review_criteria:
  code_quality:
    max_complexity: 10
    min_test_coverage: 80
    require_type_hints: true
    max_function_length: 50
    
  security:
    scan_dependencies: true
    check_secrets: true
    validate_input: true
    require_auth_review: true
    
  documentation:
    min_coverage: 70
    require_api_docs: true
    check_readme_updates: true
    validate_examples: true

language_configs:
  python:
    linters: ['pylint', 'flake8', 'mypy']
    formatters: ['black', 'isort']
    security_tools: ['bandit', 'safety']
    
  javascript:
    linters: ['eslint', 'jshint']
    formatters: ['prettier']
    security_tools: ['audit', 'snyk']
    
  java:
    linters: ['checkstyle', 'pmd', 'spotbugs']
    formatters: ['google-java-format']
    security_tools: ['spotbugs-security']
```

## Usage Examples

### Automated PR Review

```python
import requests

# Submit PR for review
response = requests.post(
    'http://localhost:8080/api/review/submit',
    json={
        'repository': 'company/awesome-app',
        'pull_request': 456,
        'review_type': 'comprehensive',
        'priority': 'high'
    }
)

review_id = response.json()['review_id']

# Monitor review progress
status = requests.get(f'http://localhost:8080/api/review/{review_id}/status')
print(f"Review status: {status.json()['status']}")

# Get detailed results
results = requests.get(f'http://localhost:8080/api/review/{review_id}/results')
print(f"Overall score: {results.json()['overall_score']}")
```

### GitHub Integration

```bash
# Set up GitHub webhook for automatic reviews
curl -X POST https://api.github.com/repos/owner/repo/hooks \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{
    "name": "web",
    "config": {
      "url": "http://your-domain.com/api/webhooks/github",
      "content_type": "json",
      "secret": "your_webhook_secret"
    },
    "events": ["pull_request", "push"]
  }'
```

### Custom Review Rules

```bash
# Submit with custom review criteria
curl -X POST http://localhost:8080/api/review/submit \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "pull_request": 789,
    "custom_rules": {
      "max_complexity": 8,
      "require_tests": true,
      "security_level": "strict",
      "doc_coverage_min": 90
    }
  }'
```

## Review Types

### Comprehensive Review
- Full static analysis
- Security vulnerability scan
- Documentation coverage check
- Performance analysis
- Best practices validation

### Security-Focused Review
- Vulnerability scanning
- Dependency security check
- Secret detection
- Authentication/authorization review
- Input validation analysis

### Quick Review
- Basic linting and formatting
- Critical security issues only
- Major code quality violations
- Breaking changes detection

### Documentation Review
- API documentation completeness
- Code comment quality
- README and guide updates
- Example code validation

## GitHub Integration

### GitHub App Configuration

```python
# app/integrations/github_app.py
from github import Github
from app.agents import ReviewCoordinator

class GitHubIntegration:
    def __init__(self, app_id, private_key):
        self.app_id = app_id
        self.private_key = private_key
        self.coordinator = ReviewCoordinator()
    
    def handle_pull_request(self, payload):
        if payload['action'] in ['opened', 'synchronize']:
            pr_data = {
                'repo': payload['repository']['full_name'],
                'pr_number': payload['pull_request']['number'],
                'head_sha': payload['pull_request']['head']['sha']
            }
            
            # Trigger review
            review_id = self.coordinator.start_review(pr_data)
            return review_id
    
    def post_review_comment(self, repo, pr_number, review_results):
        # Post review results as PR comment
        comment_body = self.format_review_comment(review_results)
        
        g = Github(self.get_installation_token(repo))
        repo_obj = g.get_repo(repo)
        pr = repo_obj.get_pull(pr_number)
        pr.create_issue_comment(comment_body)
```

### Review Comment Templates

```markdown
# Code Review Results

## Overall Score: {{ overall_score }}/100

### 📊 Summary
- **Code Quality**: {{ code_quality_score }}/100
- **Security**: {{ security_score }}/100  
- **Documentation**: {{ documentation_score }}/100
- **Performance**: {{ performance_score }}/100

### ✅ Strengths
{% for strength in strengths %}
- {{ strength }}
{% endfor %}

### ⚠️ Issues Found
{% for issue in issues %}
#### {{ issue.severity|title }} - {{ issue.category }}
**File**: `{{ issue.file }}:{{ issue.line }}`
**Issue**: {{ issue.description }}
**Suggestion**: {{ issue.suggestion }}
{% endfor %}

### 📝 Recommendations
{% for recommendation in recommendations %}
- {{ recommendation }}
{% endfor %}

### 🔗 Detailed Reports
- [Full Analysis Report]({{ detailed_report_url }})
- [Security Scan Results]({{ security_report_url }})
- [Performance Analysis]({{ performance_report_url }})

---
*Review conducted by [AI Code Review Agent]({{ agent_url }}) • [Configure Reviews]({{ config_url }})*
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/code-review.yml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run AI Code Review
      run: |
        curl -X POST ${{ secrets.REVIEW_API_URL }}/api/review/submit \
          -H "Authorization: Bearer ${{ secrets.REVIEW_API_TOKEN }}" \
          -H "Content-Type: application/json" \
          -d '{
            "repository": "${{ github.repository }}",
            "pull_request": ${{ github.event.number }},
            "head_sha": "${{ github.event.pull_request.head.sha }}"
          }'
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - review

ai-code-review:
  stage: review
  script:
    - |
      curl -X POST $REVIEW_API_URL/api/review/submit \
        -H "Authorization: Bearer $REVIEW_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "repository": "'$CI_PROJECT_PATH'",
          "merge_request": '$CI_MERGE_REQUEST_IID',
          "head_sha": "'$CI_COMMIT_SHA'"
        }'
  only:
    - merge_requests
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('AI Code Review') {
            when {
                changeRequest()
            }
            steps {
                script {
                    def reviewResponse = httpRequest(
                        httpMode: 'POST',
                        url: "${env.REVIEW_API_URL}/api/review/submit",
                        contentType: 'APPLICATION_JSON',
                        customHeaders: [[name: 'Authorization', value: "Bearer ${env.REVIEW_API_TOKEN}"]],
                        requestBody: """
                        {
                            "repository": "${env.CHANGE_URL}",
                            "pull_request": ${env.CHANGE_ID},
                            "head_sha": "${env.GIT_COMMIT}"
                        }
                        """
                    )
                    
                    def review = readJSON text: reviewResponse.content
                    echo "Review Score: ${review.overall_score}"
                }
            }
        }
    }
}
```

## Analysis Tools Integration

### SonarQube Integration

```python
# app/analyzers/sonarqube_analyzer.py
import requests

class SonarQubeAnalyzer:
    def __init__(self, url, token):
        self.url = url
        self.token = token
    
    def analyze_project(self, project_key):
        # Trigger SonarQube analysis
        analysis_data = self.get_analysis_results(project_key)
        
        return {
            'quality_gate': analysis_data.get('qualityGate'),
            'coverage': analysis_data.get('coverage'),
            'bugs': analysis_data.get('bugs'),
            'vulnerabilities': analysis_data.get('vulnerabilities'),
            'code_smells': analysis_data.get('codeSmells')
        }
```

### ESLint Integration

```python
# app/analyzers/eslint_analyzer.py
import subprocess
import json

class ESLintAnalyzer:
    def analyze_javascript(self, file_paths):
        cmd = ['eslint', '--format', 'json'] + file_paths
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {'errors': result.stderr}
```

## Custom Review Rules

### Rule Definition

```python
# app/rules/custom_rules.py
from app.analyzers import BaseRule

class ComplexityRule(BaseRule):
    def __init__(self):
        self.name = "complexity_check"
        self.severity = "warning"
        self.max_complexity = 10
    
    def check(self, code_node):
        complexity = self.calculate_complexity(code_node)
        if complexity > self.max_complexity:
            return {
                'rule': self.name,
                'severity': self.severity,
                'message': f'Function complexity ({complexity}) exceeds maximum ({self.max_complexity})',
                'suggestion': 'Consider breaking this function into smaller, more focused functions'
            }
        return None

class SecurityRule(BaseRule):
    def __init__(self):
        self.name = "sql_injection_check"
        self.severity = "error"
    
    def check(self, code_node):
        if self.contains_sql_injection_pattern(code_node):
            return {
                'rule': self.name,
                'severity': self.severity,
                'message': 'Potential SQL injection vulnerability detected',
                'suggestion': 'Use parameterized queries or ORM methods'
            }
        return None
```

### Rule Configuration

```yaml
# app/config/custom_rules.yaml
rules:
  complexity:
    enabled: true
    max_complexity: 10
    apply_to: ['python', 'javascript', 'java']
    
  security:
    sql_injection:
      enabled: true
      severity: 'error'
    
    hardcoded_secrets:
      enabled: true
      patterns: ['password', 'api_key', 'secret']
      
  documentation:
    function_docs:
      enabled: true
      min_length: 10
      require_params: true
      require_returns: true
```

## Performance Monitoring

### Review Performance Metrics

```python
# app/monitoring/performance.py
class ReviewPerformanceMonitor:
    def track_review_metrics(self, review_id, duration, results):
        metrics = {
            'review_id': review_id,
            'duration_seconds': duration,
            'lines_analyzed': results.get('lines_analyzed'),
            'issues_found': len(results.get('issues', [])),
            'overall_score': results.get('overall_score'),
            'agent_performance': {
                'static_analysis_time': results.get('static_analysis_duration'),
                'security_scan_time': results.get('security_scan_duration'),
                'documentation_check_time': results.get('docs_check_duration')
            }
        }
        
        self.store_metrics(metrics)
        return metrics
```

### Dashboard Metrics

- **Review Throughput**: Reviews per hour/day
- **Quality Trends**: Average scores over time  
- **Issue Detection**: Common issues by category
- **Performance**: Analysis time by repository size

## Deployment

### Docker Compose (Development)

```yaml
version: '3.8'
services:
  code-review:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - DATABASE_URL=postgresql://postgres:password@db:5432/code_review
    depends_on:
      - db
      - redis
      - sonarqube
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: code_review
      POSTGRES_PASSWORD: password
  
  redis:
    image: redis:7-alpine
    
  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"
    environment:
      - SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonar
      - SONAR_JDBC_USERNAME=postgres
      - SONAR_JDBC_PASSWORD=password

volumes:
  postgres_data:
  sonarqube_data:
```

### Kubernetes (Production)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: code-review-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: code-review-agent
  template:
    metadata:
      labels:
        app: code-review-agent
    spec:
      containers:
      - name: code-review
        image: agentically/code-review:latest
        ports:
        - containerPort: 8080
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: GITHUB_TOKEN
          valueFrom:
            secretKeyRef:
              name: github-secret
              key: token
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

## Testing

### Unit Tests

```bash
# Run unit tests
pytest tests/unit/

# Test individual agents
pytest tests/unit/test_static_analysis_agent.py
pytest tests/unit/test_security_agent.py
```

### Integration Tests

```bash
# Test GitHub integration
pytest tests/integration/test_github_integration.py

# Test review workflows
pytest tests/integration/test_review_workflow.py
```

### Performance Tests

```bash
# Load testing
pytest tests/performance/test_review_throughput.py

# Memory usage tests
pytest tests/performance/test_memory_usage.py
```

## Security

- **Secure Code Access**: Repository access via secure tokens
- **Encrypted Communications**: TLS for all API communications
- **Audit Logging**: Complete audit trail of all reviews
- **Access Control**: Role-based permissions for review management

## Support

- **Documentation**: [Code Review API docs](./docs/api.md)
- **Configuration**: [Setup guides](./docs/setup.md)
- **Discord**: [Community support](https://discord.gg/agentically)
- **GitHub**: [Issues and discussions](https://github.com/agenticallysh/production-agent-templates/issues)

---

**🚀 Ready to automate code reviews?** Follow the [Quick Start Guide](../../docs/quickstart.md) to deploy your code review agent in 7 minutes.