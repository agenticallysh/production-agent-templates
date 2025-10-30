# Document Processing Agent Template

## Overview

Production-ready AI agent system for automated document analysis, extraction, and processing. Built with LangChain for comprehensive document understanding, multi-format support, and intelligent content extraction.

## Quick Deploy

```bash
# Clone and deploy
git clone https://github.com/agenticallysh/production-agent-templates.git
cd production-agent-templates/templates/document-processing
docker-compose up -d

# Your document processing API will be available at: http://localhost:8080
```

## Features

- **📄 Multi-Format Support**: PDF, DOCX, TXT, HTML, Markdown, Excel, PowerPoint
- **🔍 Intelligent Extraction**: Text, tables, images, metadata, structure
- **🧠 Document Understanding**: Summarization, classification, entity extraction
- **📊 Data Structuring**: Convert unstructured documents to structured data
- **🔄 Batch Processing**: Handle multiple documents simultaneously
- **🌐 OCR Integration**: Extract text from scanned documents and images

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Document    │───▶│  Content     │───▶│  Analysis    │───▶│  Output      │
│  Ingestion   │    │  Extraction  │    │  Agent       │    │  Generator   │
│              │    │              │    │              │    │              │
│ • File upload│    │ • Text       │    │ • Summary    │    │ • Structured │
│ • Format det │    │ • Tables     │    │ • Keywords   │    │   JSON       │
│ • Validation │    │ • Images     │    │ • Entities   │    │ • Reports    │
│ • Queue mgmt │    │ • Metadata   │    │ • Category   │    │ • Exports    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Agent Roles

### Document Ingestion Agent
- **Role**: File handling and preprocessing specialist
- **Tools**: File validators, format detectors, conversion libraries
- **Responsibilities**:
  - Multi-format file ingestion
  - Document validation and sanitization
  - Format detection and conversion
  - Queue management for batch processing

### Content Extraction Agent
- **Role**: Text and data extraction expert
- **Tools**: OCR engines, table extractors, image processors
- **Responsibilities**:
  - Text extraction from all formats
  - Table structure recognition and extraction
  - Image and diagram extraction
  - Metadata and document properties extraction

### Analysis Agent
- **Role**: Document understanding and analysis specialist
- **Tools**: NLP models, classification algorithms, entity extractors
- **Responsibilities**:
  - Document summarization and key insights
  - Content classification and categorization
  - Named entity recognition
  - Sentiment analysis and document scoring

### Output Generator Agent
- **Role**: Results formatting and export specialist
- **Tools**: JSON serializers, report generators, export libraries
- **Responsibilities**:
  - Structured data output generation
  - Report creation and formatting
  - Multi-format export handling
  - Results validation and quality assurance

## API Endpoints

### Upload Document for Processing
```bash
curl -X POST http://localhost:8080/api/documents/upload \
  -F "file=@document.pdf" \
  -F "processing_type=comprehensive" \
  -F "extract_tables=true" \
  -F "extract_images=true"
```

### Get Processing Status
```bash
curl http://localhost:8080/api/documents/{doc_id}/status
```

### Get Processed Results
```bash
curl http://localhost:8080/api/documents/{doc_id}/results
```

### Batch Processing
```bash
curl -X POST http://localhost:8080/api/documents/batch \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.docx" \
  -F "files=@doc3.xlsx" \
  -F "processing_type=extraction"
```

## Configuration

### Environment Variables

```bash
# AI Model Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# OCR Configuration
ENABLE_OCR=true
OCR_ENGINE=tesseract
OCR_LANGUAGES=eng,fra,spa,deu

# Processing Settings
MAX_FILE_SIZE=100MB
SUPPORTED_FORMATS=pdf,docx,xlsx,pptx,txt,html,md
EXTRACT_IMAGES=true
EXTRACT_TABLES=true
ENABLE_PREVIEW=true

# Storage Configuration
STORAGE_BACKEND=s3
S3_BUCKET=document-processing-bucket
S3_REGION=us-west-2

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/doc_processing
REDIS_URL=redis://localhost:6379/0
```

### Processing Configuration

```yaml
# app/config/processing_config.yaml
document_types:
  pdf:
    engines: ['pdfplumber', 'pymupdf', 'pdfminer']
    extract_text: true
    extract_tables: true
    extract_images: true
    ocr_fallback: true
    
  docx:
    engines: ['python-docx', 'mammoth']
    preserve_formatting: true
    extract_headers: true
    extract_footnotes: true
    
  xlsx:
    engines: ['openpyxl', 'xlrd']
    all_sheets: true
    detect_tables: true
    preserve_formulas: false

analysis_settings:
  summarization:
    max_length: 500
    min_length: 100
    method: 'extractive'
    
  classification:
    categories: ['contract', 'invoice', 'report', 'presentation', 'other']
    confidence_threshold: 0.8
    
  entity_extraction:
    types: ['PERSON', 'ORG', 'DATE', 'MONEY', 'GPE']
    custom_entities: ['product_name', 'contract_number']
```

## Usage Examples

### Basic Document Processing

```python
import requests

# Upload document
with open('contract.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8080/api/documents/upload',
        files={'file': f},
        data={
            'processing_type': 'comprehensive',
            'extract_tables': True,
            'extract_entities': True
        }
    )

doc_id = response.json()['document_id']

# Check processing status
status = requests.get(f'http://localhost:8080/api/documents/{doc_id}/status')
print(f"Status: {status.json()['status']}")

# Get results when complete
if status.json()['status'] == 'completed':
    results = requests.get(f'http://localhost:8080/api/documents/{doc_id}/results')
    print(f"Summary: {results.json()['summary']}")
    print(f"Entities: {results.json()['entities']}")
```

### Batch Document Processing

```bash
# Process multiple financial documents
curl -X POST http://localhost:8080/api/documents/batch \
  -F "files=@Q1_report.pdf" \
  -F "files=@Q2_report.pdf" \
  -F "files=@Q3_report.pdf" \
  -F "processing_type=financial_analysis" \
  -F "output_format=structured_json"
```

### Custom Processing Pipeline

```bash
# Upload with custom analysis parameters
curl -X POST http://localhost:8080/api/documents/upload \
  -F "file=@research_paper.pdf" \
  -F "processing_type=academic" \
  -F "extract_citations=true" \
  -F "extract_figures=true" \
  -F "summarize_sections=true"
```

## Document Types and Processing

### PDF Documents
- **Text Extraction**: Multi-engine approach for best accuracy
- **Table Extraction**: Detect and preserve table structure
- **Image Extraction**: Extract embedded images and diagrams
- **OCR Fallback**: Process scanned PDFs with OCR
- **Metadata**: Author, creation date, title, keywords

### Microsoft Office Documents
- **DOCX**: Text, formatting, headers, tables, comments
- **XLSX**: All sheets, formulas, charts, pivot tables
- **PPTX**: Slides, speaker notes, embedded objects
- **Formatting Preservation**: Maintain document structure

### Web and Markup Documents
- **HTML**: Clean text extraction, link preservation
- **Markdown**: Structure-aware parsing
- **XML**: Schema-aware extraction
- **Email (EML/MSG)**: Headers, body, attachments

### Specialized Formats
- **Legal Documents**: Contract analysis, clause extraction
- **Financial Reports**: Number extraction, table parsing
- **Academic Papers**: Citation extraction, reference parsing
- **Medical Records**: HIPAA-compliant processing

## Processing Types

### Comprehensive Analysis
```json
{
  "text_extraction": true,
  "table_extraction": true,
  "image_extraction": true,
  "summarization": true,
  "entity_extraction": true,
  "classification": true,
  "sentiment_analysis": true,
  "keyword_extraction": true
}
```

### Quick Extraction
```json
{
  "text_extraction": true,
  "basic_metadata": true,
  "document_type": true,
  "page_count": true
}
```

### Data Extraction Focus
```json
{
  "table_extraction": true,
  "structured_data": true,
  "number_extraction": true,
  "date_extraction": true,
  "contact_extraction": true
}
```

### Content Analysis
```json
{
  "summarization": true,
  "topic_modeling": true,
  "sentiment_analysis": true,
  "readability_score": true,
  "language_detection": true
}
```

## Output Formats

### Structured JSON
```json
{
  "document_id": "doc_123",
  "metadata": {
    "filename": "contract.pdf",
    "file_size": 2048576,
    "format": "pdf",
    "pages": 15,
    "created_date": "2024-01-15",
    "language": "en"
  },
  "content": {
    "text": "Full extracted text...",
    "summary": "Document summary...",
    "tables": [
      {
        "page": 3,
        "headers": ["Item", "Quantity", "Price"],
        "rows": [["Widget A", "10", "$100"]]
      }
    ],
    "images": [
      {
        "page": 5,
        "description": "Company logo",
        "url": "/api/documents/doc_123/images/img_001.png"
      }
    ]
  },
  "analysis": {
    "classification": "contract",
    "confidence": 0.95,
    "entities": [
      {"text": "John Smith", "type": "PERSON", "start": 45, "end": 55},
      {"text": "Acme Corp", "type": "ORG", "start": 120, "end": 129}
    ],
    "sentiment": "neutral",
    "keywords": ["agreement", "payment", "delivery", "terms"]
  }
}
```

### Excel Export
- Structured data in spreadsheet format
- Separate sheets for text, tables, entities
- Metadata summary sheet
- Charts and visualizations

### PDF Report
- Executive summary
- Detailed analysis results
- Extracted tables and images
- Processing methodology

## Advanced Features

### OCR Processing

```python
# app/processors/ocr_processor.py
from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self, languages=['eng']):
        self.languages = '+'.join(languages)
    
    def extract_text_from_image(self, image_path):
        image = Image.open(image_path)
        
        # Preprocess image for better OCR
        processed_image = self.preprocess_image(image)
        
        # Extract text with confidence scores
        text_data = pytesseract.image_to_data(
            processed_image,
            lang=self.languages,
            output_type=pytesseract.Output.DICT
        )
        
        return self.parse_ocr_results(text_data)
```

### Table Extraction

```python
# app/processors/table_processor.py
import pandas as pd
from tabula import read_pdf

class TableProcessor:
    def extract_tables_from_pdf(self, pdf_path):
        tables = []
        
        # Extract tables using multiple methods
        tabula_tables = read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        for i, table in enumerate(tabula_tables):
            if not table.empty:
                tables.append({
                    'table_id': i,
                    'headers': table.columns.tolist(),
                    'data': table.values.tolist(),
                    'shape': table.shape
                })
        
        return tables
```

### Entity Extraction

```python
# app/processors/entity_processor.py
import spacy
from transformers import pipeline

class EntityProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.ner_pipeline = pipeline("ner", aggregation_strategy="simple")
    
    def extract_entities(self, text):
        # Standard NER with spaCy
        doc = self.nlp(text)
        spacy_entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Advanced NER with transformers
        transformer_entities = self.ner_pipeline(text)
        
        # Combine and deduplicate
        all_entities = self.merge_entity_results(spacy_entities, transformer_entities)
        
        return all_entities
```

## Integration Examples

### File Storage Integration

```python
# app/storage/s3_storage.py
import boto3

class S3Storage:
    def __init__(self, bucket_name, region):
        self.s3 = boto3.client('s3', region_name=region)
        self.bucket = bucket_name
    
    def store_document(self, file_data, document_id):
        key = f"documents/{document_id}/original"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=file_data,
            ServerSideEncryption='AES256'
        )
        return f"s3://{self.bucket}/{key}"
    
    def store_results(self, results, document_id):
        key = f"documents/{document_id}/results.json"
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=json.dumps(results),
            ContentType='application/json',
            ServerSideEncryption='AES256'
        )
```

### Webhook Integration

```python
# app/webhooks/processing_webhooks.py
import requests

class ProcessingWebhooks:
    def __init__(self, webhook_urls):
        self.webhook_urls = webhook_urls
    
    def notify_completion(self, document_id, results):
        payload = {
            'event': 'document.processed',
            'document_id': document_id,
            'status': 'completed',
            'results_url': f'/api/documents/{document_id}/results',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        for url in self.webhook_urls:
            try:
                requests.post(url, json=payload, timeout=10)
            except requests.RequestException as e:
                logger.error(f"Webhook failed for {url}: {e}")
```

## Performance Optimization

### Parallel Processing

```python
# app/processors/parallel_processor.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelDocumentProcessor:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_batch(self, documents):
        tasks = []
        for doc in documents:
            task = asyncio.create_task(self.process_single_document(doc))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
```

### Caching Strategy

```python
# app/cache/processing_cache.py
import redis
import hashlib

class ProcessingCache:
    def __init__(self, redis_url):
        self.redis = redis.from_url(redis_url)
        self.cache_ttl = 86400  # 24 hours
    
    def get_cached_result(self, file_hash, processing_type):
        cache_key = f"doc:{file_hash}:{processing_type}"
        cached = self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        return None
    
    def cache_result(self, file_hash, processing_type, results):
        cache_key = f"doc:{file_hash}:{processing_type}"
        self.redis.setex(
            cache_key,
            self.cache_ttl,
            json.dumps(results)
        )
```

## Deployment

### Docker Compose (Development)

```yaml
version: '3.8'
services:
  document-processor:
    build: .
    ports:
      - "8080:8080"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://postgres:password@db:5432/doc_processing
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./storage:/app/storage
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: doc_processing
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    
  # OCR service
  tesseract:
    image: tesseractshadow/tesseract4re
    volumes:
      - ./temp:/tmp

volumes:
  postgres_data:
```

### Kubernetes (Production)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: document-processor
spec:
  replicas: 5
  selector:
    matchLabels:
      app: document-processor
  template:
    metadata:
      labels:
        app: document-processor
    spec:
      containers:
      - name: document-processor
        image: agentically/document-processor:latest
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
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
        - name: temp-storage
          mountPath: /tmp
      volumes:
      - name: temp-storage
        emptyDir:
          sizeLimit: 10Gi
```

## Monitoring and Analytics

### Processing Metrics

```python
# app/monitoring/metrics.py
class ProcessingMetrics:
    def track_processing_time(self, document_id, processing_type, duration):
        metrics = {
            'document_id': document_id,
            'processing_type': processing_type,
            'duration_seconds': duration,
            'timestamp': datetime.utcnow()
        }
        self.store_metrics(metrics)
    
    def track_accuracy_metrics(self, document_id, accuracy_scores):
        # Track OCR accuracy, table extraction accuracy, etc.
        pass
```

### Dashboard KPIs
- **Processing Throughput**: Documents per hour
- **Success Rate**: Successful vs failed processing
- **Processing Time**: Average time by document type
- **Accuracy Metrics**: OCR confidence, extraction quality

## Security and Compliance

### Data Protection
- **Encryption**: All documents encrypted at rest and in transit
- **Access Control**: Role-based access to documents and results
- **Audit Logging**: Complete processing audit trail
- **Data Retention**: Configurable retention policies

### GDPR Compliance
- **Data Minimization**: Process only necessary data
- **Right to Deletion**: Complete document and result removal
- **Processing Records**: Detailed processing logs
- **Consent Management**: Track processing consent

## Troubleshooting

### Common Issues

**Large File Processing**
```bash
# Increase memory limits
export PROCESSING_MEMORY_LIMIT=4GB
export CHUNK_SIZE=1MB
```

**OCR Quality Issues**
```bash
# Improve OCR settings
export OCR_DPI=300
export OCR_PSM=6
export IMAGE_PREPROCESSING=true
```

**Table Extraction Failures**
```bash
# Enable multiple extraction engines
export TABLE_ENGINES=tabula,camelot,pdfplumber
export FALLBACK_EXTRACTION=true
```

## Testing

### Unit Tests
```bash
pytest tests/unit/
pytest tests/unit/test_pdf_processor.py
pytest tests/unit/test_ocr_processor.py
```

### Integration Tests
```bash
pytest tests/integration/
pytest tests/integration/test_processing_pipeline.py
```

### Performance Tests
```bash
pytest tests/performance/
pytest tests/performance/test_batch_processing.py
```

## Support

- **Documentation**: [Processing API docs](./docs/api.md)
- **Examples**: [Sample documents](./examples/)
- **Discord**: [Community support](https://discord.gg/agentically)
- **GitHub**: [Issues and discussions](https://github.com/agenticallysh/production-agent-templates/issues)

---

**🚀 Ready to process documents?** Follow the [Quick Start Guide](../../docs/quickstart.md) to deploy your document processing agent in 6 minutes.