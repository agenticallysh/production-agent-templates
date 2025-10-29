#!/usr/bin/env python3
"""
Configuration settings for Customer Support Agent system
Production-ready configuration with environment variable support.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    api_key: str = Field(
        default="demo-api-key-change-in-production",
        description="API key for authentication"
    )
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins"
    )
    
    # OpenAI Configuration
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key for LLM access"
    )
    openai_model: str = Field(
        default="gpt-4",
        description="OpenAI model to use"
    )
    
    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379",
        description="Redis connection URL"
    )
    redis_password: Optional[str] = Field(
        default=None,
        description="Redis password if required"
    )
    
    # Database Configuration (for future use)
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/customer_support",
        description="Database connection URL"
    )
    
    # Application Configuration
    environment: str = Field(
        default="development",
        description="Application environment (development, staging, production)"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    # CrewAI Configuration
    crew_verbose: bool = Field(
        default=True,
        description="Enable verbose logging for CrewAI"
    )
    crew_memory: bool = Field(
        default=True,
        description="Enable memory for CrewAI agents"
    )
    max_iterations: int = Field(
        default=3,
        description="Maximum iterations for agent tasks"
    )
    
    # Performance Configuration
    request_timeout: int = Field(
        default=30,
        description="Request timeout in seconds"
    )
    max_concurrent_requests: int = Field(
        default=100,
        description="Maximum concurrent requests"
    )
    
    # Monitoring Configuration
    enable_metrics: bool = Field(
        default=True,
        description="Enable Prometheus metrics"
    )
    metrics_port: int = Field(
        default=9090,
        description="Metrics server port"
    )
    
    # Security Configuration
    enable_rate_limiting: bool = Field(
        default=True,
        description="Enable rate limiting"
    )
    rate_limit_requests: int = Field(
        default=60,
        description="Requests per minute per IP"
    )
    
    # Escalation Configuration
    escalation_keywords: List[str] = Field(
        default=[
            "manager", "supervisor", "human", "person", 
            "escalate", "complaint", "refund", "cancel"
        ],
        description="Keywords that trigger escalation"
    )
    max_response_time: int = Field(
        default=300,
        description="Maximum response time before escalation (seconds)"
    )
    
    # Business Configuration
    company_name: str = Field(
        default="Acme Corporation",
        description="Company name for responses"
    )
    support_email: str = Field(
        default="support@acme.com",
        description="Support email for escalations"
    )
    business_hours: str = Field(
        default="Monday-Friday 9AM-6PM EST",
        description="Business hours description"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable prefixes
        env_prefix = "CUSTOMER_SUPPORT_"

class ProductionSettings(Settings):
    """Production-specific settings"""
    
    environment: str = "production"
    log_level: str = "WARNING"
    crew_verbose: bool = False
    
    # Production security
    api_key: str = Field(
        ...,
        description="Production API key (required)"
    )
    
    # Production performance
    max_concurrent_requests: int = 500
    request_timeout: int = 60
    
    # Production Redis (managed service)
    redis_url: str = Field(
        ...,
        description="Production Redis URL (required)"
    )

class DevelopmentSettings(Settings):
    """Development-specific settings"""
    
    environment: str = "development"
    log_level: str = "DEBUG"
    crew_verbose: bool = True
    
    # Development-friendly defaults
    api_key: str = "dev-api-key"
    redis_url: str = "redis://localhost:6379"

def get_settings() -> Settings:
    """Get settings based on environment"""
    
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "development":
        return DevelopmentSettings()
    else:
        return Settings()

# Global settings instance
settings = get_settings()