#!/usr/bin/env python3
"""
Production Customer Support Agent System
Built with CrewAI for multi-agent coordination and FastAPI for REST API.

This is a production-ready template that includes:
- Multi-agent customer support with CrewAI
- REST API with authentication
- Real-time chat capabilities
- Monitoring and observability
- Docker deployment ready
"""

import os
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
import redis.asyncio as redis

from agents.support_crew import CustomerSupportCrew
from config.settings import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = Settings()

# Redis connection for session management
redis_client: Optional[redis.Redis] = None

class ChatMessage(BaseModel):
    """Chat message model"""
    message: str = Field(..., description="User message")
    session_id: str = Field(..., description="Chat session ID")
    customer_info: Optional[Dict[str, Any]] = Field(None, description="Customer context")

class ChatResponse(BaseModel):
    """Chat response model"""
    response: str = Field(..., description="Agent response")
    session_id: str = Field(..., description="Chat session ID")
    agent_used: str = Field(..., description="Which agent handled the request")
    confidence: float = Field(..., description="Response confidence score")
    escalated: bool = Field(False, description="Whether this was escalated to human")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    uptime: str

class ConnectionManager:
    """WebSocket connection manager for real-time chat"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected for session: {session_id}")
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected for session: {session_id}")
    
    async def send_message(self, session_id: str, message: dict):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)

# Global connection manager
manager = ConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global redis_client
    
    # Startup
    logger.info("🚀 Starting Customer Support Agent System")
    
    # Initialize Redis connection
    try:
        redis_client = redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        logger.info("✅ Redis connection established")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        redis_client = None
    
    # Initialize CrewAI agents
    try:
        support_crew = CustomerSupportCrew()
        app.state.support_crew = support_crew
        logger.info("✅ Customer support crew initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize support crew: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Customer Support Agent System")
    if redis_client:
        await redis_client.close()

# Initialize FastAPI app
app = FastAPI(
    title="Customer Support Agent API",
    description="Production-ready customer support with AI agents",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token (simplified for demo)"""
    if credentials.credentials != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return credentials.credentials

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        uptime="System operational"
    )

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_agent(
    chat_request: ChatMessage,
    token: str = Depends(verify_token)
):
    """
    Chat with customer support agents
    
    This endpoint processes customer messages through the CrewAI support crew
    and returns intelligent responses with escalation logic.
    """
    try:
        # Get the support crew from app state
        support_crew = app.state.support_crew
        
        # Process the message through CrewAI
        result = await support_crew.process_customer_request(
            message=chat_request.message,
            session_id=chat_request.session_id,
            customer_info=chat_request.customer_info or {}
        )
        
        # Store conversation in Redis if available
        if redis_client:
            await store_conversation(
                chat_request.session_id,
                chat_request.message,
                result["response"]
            )
        
        # Send real-time update via WebSocket
        await manager.send_message(chat_request.session_id, {
            "type": "agent_response",
            "response": result["response"],
            "agent": result["agent_used"]
        })
        
        return ChatResponse(
            response=result["response"],
            session_id=chat_request.session_id,
            agent_used=result["agent_used"],
            confidence=result["confidence"],
            escalated=result["escalated"]
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time chat
    
    Enables real-time bidirectional communication for chat interface
    """
    await manager.connect(websocket, session_id)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            # Process through support crew
            support_crew = app.state.support_crew
            result = await support_crew.process_customer_request(
                message=data["message"],
                session_id=session_id,
                customer_info=data.get("customer_info", {})
            )
            
            # Send response back
            await manager.send_message(session_id, {
                "type": "agent_response",
                "response": result["response"],
                "agent": result["agent_used"],
                "escalated": result["escalated"],
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(session_id)

@app.get("/api/v1/conversations/{session_id}")
async def get_conversation_history(
    session_id: str,
    token: str = Depends(verify_token)
):
    """Get conversation history for a session"""
    if not redis_client:
        raise HTTPException(status_code=503, detail="Session storage not available")
    
    try:
        history = await redis_client.lrange(f"conversation:{session_id}", 0, -1)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        logger.error(f"Error retrieving conversation: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve conversation")

@app.get("/api/v1/analytics/dashboard")
async def get_analytics_dashboard(token: str = Depends(verify_token)):
    """Get analytics dashboard data"""
    try:
        # In production, this would query your analytics database
        # For demo, return sample data
        return {
            "total_conversations": 1247,
            "avg_response_time": 1.2,
            "satisfaction_score": 4.7,
            "escalation_rate": 0.08,
            "active_sessions": len(manager.active_connections),
            "agents_status": {
                "support_agent": "active",
                "escalation_agent": "active",
                "manager_agent": "active"
            }
        }
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail="Analytics unavailable")

async def store_conversation(session_id: str, user_message: str, agent_response: str):
    """Store conversation in Redis"""
    if redis_client:
        try:
            conversation_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "user": user_message,
                "agent": agent_response
            }
            await redis_client.lpush(
                f"conversation:{session_id}",
                str(conversation_entry)
            )
            # Expire after 24 hours
            await redis_client.expire(f"conversation:{session_id}", 86400)
        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development",
        log_level="info"
    )