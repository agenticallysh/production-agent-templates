# Data Analysis Agent Template

## Overview

Production-ready AI agent for automated data analysis, report generation, and insights extraction. Built with AutoGen for multi-agent collaboration between data processors, analysts, and report generators.

## Quick Deploy

```bash
# Clone and deploy
git clone https://github.com/agenticallysh/production-agent-templates.git
cd production-agent-templates/templates/data-analysis
docker-compose up -d

# Your data analysis API will be available at: http://localhost:8080
```

## Features

- **📊 Automated Analysis**: Upload CSV/Excel files for instant insights
- **📈 Interactive Reports**: Dynamic charts, graphs, and visualizations  
- **🤖 Multi-Agent System**: Specialized agents for processing, analysis, and reporting
- **📋 Export Options**: PDF reports, Excel summaries, JSON data
- **🔄 Batch Processing**: Handle multiple datasets simultaneously
- **📱 Web Interface**: User-friendly dashboard for data uploads and results

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Data Processor │───▶│   Data Analyst  │───▶│ Report Generator│
│                 │    │                 │    │                 │
│ • File parsing  │    │ • Statistical   │    │ • PDF export    │
│ • Data cleaning │    │   analysis      │    │ • Visualizations│
│ • Validation    │    │ • Trend detection│    │ • Summaries     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Agent Roles

### Data Processor Agent
- **Role**: Data ingestion and preprocessing specialist
- **Tools**: Pandas, NumPy, data validation libraries
- **Responsibilities**: 
  - Parse uploaded files (CSV, Excel, JSON)
  - Clean and normalize data
  - Handle missing values and outliers
  - Validate data quality

### Data Analyst Agent  
- **Role**: Statistical analysis and pattern recognition expert
- **Tools**: SciPy, Scikit-learn, statistical libraries
- **Responsibilities**:
  - Perform descriptive statistics
  - Identify trends and correlations
  - Generate insights and recommendations
  - Detect anomalies and outliers

### Report Generator Agent
- **Role**: Visualization and reporting specialist
- **Tools**: Matplotlib, Plotly, ReportLab
- **Responsibilities**:
  - Create charts and visualizations
  - Generate PDF reports
  - Format data summaries
  - Export results in multiple formats

## API Endpoints

### Upload and Analyze Data
```bash
curl -X POST http://localhost:8080/api/analyze \
  -F "file=@data.csv" \
  -F "analysis_type=comprehensive"
```

### Get Analysis Status
```bash
curl http://localhost:8080/api/analysis/{analysis_id}/status
```

### Download Report
```bash
curl http://localhost:8080/api/analysis/{analysis_id}/report \
  -o report.pdf
```

### List Previous Analyses
```bash
curl http://localhost:8080/api/analyses
```

## Configuration

### Environment Variables

```bash
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Analysis Settings
MAX_FILE_SIZE=100MB
SUPPORTED_FORMATS=csv,xlsx,json,parquet
AUTO_ANALYSIS=true
CHART_THEME=plotly_white

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/data_analysis
REDIS_URL=redis://localhost:6379/0

# Security
API_KEY_REQUIRED=true
RATE_LIMIT=100/hour
CORS_ORIGINS=*
```

### Analysis Configuration

```yaml
# app/config/analysis_config.yaml
analysis:
  default_charts:
    - histogram
    - correlation_matrix
    - trend_line
    - scatter_plot
  
  statistical_tests:
    - normality_test
    - correlation_test
    - outlier_detection
  
  export_formats:
    - pdf
    - excel
    - json
    - csv

quality_checks:
  missing_data_threshold: 0.1
  outlier_detection_method: "IQR"
  correlation_threshold: 0.7
```

## Usage Examples

### Basic Data Analysis

```python
import requests

# Upload file for analysis
with open('sales_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:8080/api/analyze',
        files={'file': f},
        data={'analysis_type': 'sales_analysis'}
    )

analysis_id = response.json()['analysis_id']

# Check status
status = requests.get(f'http://localhost:8080/api/analysis/{analysis_id}/status')
print(status.json())

# Download report when complete
if status.json()['status'] == 'completed':
    report = requests.get(f'http://localhost:8080/api/analysis/{analysis_id}/report')
    with open('analysis_report.pdf', 'wb') as f:
        f.write(report.content)
```

### Custom Analysis Pipeline

```bash
# Upload with custom parameters
curl -X POST http://localhost:8080/api/analyze \
  -F "file=@customer_data.csv" \
  -F "analysis_type=customer_segmentation" \
  -F "chart_types=['scatter', 'heatmap', 'box_plot']" \
  -F "export_format=excel"
```

### Batch Processing

```bash
# Process multiple files
curl -X POST http://localhost:8080/api/batch-analyze \
  -F "files=@Q1_sales.csv" \
  -F "files=@Q2_sales.csv" \
  -F "files=@Q3_sales.csv" \
  -F "analysis_type=quarterly_comparison"
```

## Supported Analysis Types

### Sales Analysis
- Revenue trends and forecasting
- Customer segmentation
- Product performance analysis
- Seasonal pattern detection

### Financial Analysis  
- Cash flow analysis
- Profitability metrics
- Budget variance analysis
- Financial ratio calculations

### Marketing Analysis
- Campaign performance metrics
- Customer acquisition analysis
- ROI calculations
- A/B test analysis

### Operations Analysis
- Efficiency metrics
- Resource utilization
- Quality control analysis
- Process optimization

## Customization

### Adding Custom Analysis Types

```python
# app/analyzers/custom_analyzer.py
from app.agents import DataAnalyzer

class CustomAnalyzer(DataAnalyzer):
    def __init__(self):
        super().__init__()
        self.analysis_type = "custom_analysis"
    
    def analyze(self, data):
        # Your custom analysis logic
        insights = self.perform_custom_analysis(data)
        visualizations = self.create_custom_charts(data)
        
        return {
            'insights': insights,
            'visualizations': visualizations,
            'recommendations': self.generate_recommendations(insights)
        }
```

### Custom Visualization Templates

```python
# app/visualizations/custom_charts.py
import plotly.graph_objects as go

def create_custom_dashboard(data):
    fig = go.Figure()
    
    # Add your custom visualization logic
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['value'],
        mode='lines+markers'
    ))
    
    return fig
```

## Deployment

### Docker Compose (Development)

```yaml
version: '3.8'
services:
  data-analysis:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/data_analysis
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: data_analysis
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Kubernetes (Production)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-analysis-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-analysis-agent
  template:
    metadata:
      labels:
        app: data-analysis-agent
    spec:
      containers:
      - name: data-analysis
        image: agentically/data-analysis:latest
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
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

## Monitoring and Observability

### Metrics Dashboard

Access Grafana dashboard at `http://localhost:3000` with metrics:

- **Analysis Performance**: Processing time, success rate
- **Resource Usage**: CPU, memory, disk utilization  
- **API Metrics**: Request rate, response time, error rate
- **Data Quality**: Missing data %, outlier detection rate

### Health Checks

```bash
# Application health
curl http://localhost:8080/health

# Agent status
curl http://localhost:8080/api/agents/status

# Database connectivity
curl http://localhost:8080/api/health/database
```

### Logging

Structured logs available for:
- Data processing pipeline
- Analysis execution
- Error tracking
- Performance monitoring

## Testing

### Run Tests

```bash
# Unit tests
pytest tests/unit/

# Integration tests  
pytest tests/integration/

# End-to-end tests
pytest tests/e2e/

# Performance tests
pytest tests/performance/
```

### Sample Test Data

```bash
# Generate test datasets
python scripts/generate_test_data.py --type sales --records 10000
python scripts/generate_test_data.py --type financial --records 5000
```

## Troubleshooting

### Common Issues

**Large File Processing**
```bash
# Increase memory limits
export PYTHON_MEMORY_LIMIT=4GB
export PANDAS_CHUNK_SIZE=10000
```

**Analysis Timeout**
```bash
# Adjust timeout settings
export ANALYSIS_TIMEOUT=300
export AGENT_MAX_ITERATIONS=20
```

**Memory Issues**
```bash
# Enable streaming processing
export ENABLE_STREAMING=true
export CHUNK_PROCESSING=true
```

## Performance Optimization

### For Large Datasets

```python
# app/config/performance.py
PERFORMANCE_CONFIG = {
    'chunk_size': 10000,
    'parallel_processing': True,
    'memory_optimization': True,
    'cache_intermediate_results': True
}
```

### Scaling Configuration

```yaml
# docker-compose.prod.yml
services:
  data-analysis:
    deploy:
      replicas: 5
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
      restart_policy:
        condition: on-failure
```

## Security

- **Data Encryption**: All uploaded files encrypted at rest
- **API Authentication**: JWT tokens required for all endpoints
- **Access Control**: Role-based permissions for different analysis types
- **Audit Logging**: Complete audit trail of all data access

## Support

- **Documentation**: [Full API docs](./docs/api.md)
- **Examples**: [Sample notebooks](./examples/)
- **Discord**: [Community support](https://discord.gg/agentically)
- **GitHub**: [Issues and discussions](https://github.com/agenticallysh/production-agent-templates/issues)

---

**🚀 Ready to deploy?** Follow the [Quick Start Guide](../../docs/quickstart.md) to get your data analysis agent running in 5 minutes.