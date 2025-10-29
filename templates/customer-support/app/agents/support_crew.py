#!/usr/bin/env python3
"""
Customer Support CrewAI Implementation
Multi-agent system for intelligent customer support with escalation workflows.

Agents:
- Support Agent: Primary customer interaction
- Manager Agent: Escalation and complex issue handling  
- Quality Agent: Response quality assurance and improvement
"""

import os
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain.tools import tool
import json

logger = logging.getLogger(__name__)

class KnowledgeBaseTool(BaseTool):
    """Tool for searching company knowledge base"""
    
    name: str = "knowledge_base_search"
    description: str = "Search the company knowledge base for relevant information"
    
    def _run(self, query: str) -> str:
        """Search knowledge base (mock implementation)"""
        # In production, this would connect to your actual knowledge base
        knowledge_responses = {
            "return policy": "Our return policy allows returns within 30 days of purchase with original receipt.",
            "shipping": "Standard shipping takes 3-5 business days. Express shipping is 1-2 business days.",
            "refund": "Refunds are processed within 5-7 business days to the original payment method.",
            "warranty": "All products come with a 1-year manufacturer warranty covering defects.",
            "account": "You can reset your password by clicking 'Forgot Password' on the login page.",
            "billing": "Billing questions can be resolved by checking your account dashboard or contacting billing support.",
            "technical": "For technical issues, try restarting the application or clearing your browser cache.",
            "pricing": "Current pricing information is available on our pricing page. Enterprise discounts are available."
        }
        
        # Simple keyword matching (in production, use vector search)
        for keyword, response in knowledge_responses.items():
            if keyword.lower() in query.lower():
                return response
        
        return "I couldn't find specific information about that in our knowledge base. Let me escalate this to a specialist."

class EscalationTool(BaseTool):
    """Tool for escalating issues to human agents"""
    
    name: str = "escalate_to_human"
    description: str = "Escalate complex issues to human agents"
    
    def _run(self, reason: str, customer_info: str = "", urgency: str = "normal") -> str:
        """Escalate to human agent"""
        escalation_id = f"ESC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # In production, this would create a ticket in your support system
        logger.info(f"Escalation created: {escalation_id} - Reason: {reason}")
        
        return f"I've escalated your issue (ID: {escalation_id}) to our specialist team. A human agent will contact you within 15 minutes for {urgency} priority issues."

class CustomerSupportCrew:
    """CrewAI-based customer support system"""
    
    def __init__(self):
        """Initialize the customer support crew"""
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize tools
        self.knowledge_tool = KnowledgeBaseTool()
        self.escalation_tool = EscalationTool()
        
        # Create agents
        self.support_agent = self._create_support_agent()
        self.manager_agent = self._create_manager_agent()
        self.quality_agent = self._create_quality_agent()
        
        # Create crew
        self.crew = self._create_crew()
        
        logger.info("✅ Customer support crew initialized")
    
    def _create_support_agent(self) -> Agent:
        """Create the primary support agent"""
        return Agent(
            role="Customer Support Specialist",
            goal="Provide helpful, accurate, and empathetic customer support",
            backstory="""You are an experienced customer support specialist with excellent 
            communication skills. You're patient, understanding, and always try to resolve 
            issues on the first contact. You have access to the company knowledge base and 
            can escalate complex issues when needed.""",
            tools=[self.knowledge_tool, self.escalation_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_iter=3,
            memory=True
        )
    
    def _create_manager_agent(self) -> Agent:
        """Create the manager agent for escalations"""
        return Agent(
            role="Support Manager",
            goal="Handle escalated issues and ensure customer satisfaction",
            backstory="""You are a senior support manager with extensive experience in 
            resolving complex customer issues. You have the authority to make decisions 
            about refunds, discounts, and policy exceptions. You work closely with other 
            departments to resolve issues quickly.""",
            tools=[self.knowledge_tool, self.escalation_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=2,
            memory=True
        )
    
    def _create_quality_agent(self) -> Agent:
        """Create the quality assurance agent"""
        return Agent(
            role="Quality Assurance Specialist",
            goal="Ensure response quality and customer satisfaction",
            backstory="""You are a quality assurance specialist who reviews customer 
            interactions to ensure they meet our high standards. You focus on accuracy, 
            empathy, and solution effectiveness. You provide feedback to improve our 
            support processes.""",
            tools=[],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=1,
            memory=True
        )
    
    def _create_crew(self) -> Crew:
        """Create the support crew"""
        return Crew(
            agents=[self.support_agent, self.manager_agent, self.quality_agent],
            process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True,
            memory=True
        )
    
    async def process_customer_request(
        self, 
        message: str, 
        session_id: str,
        customer_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Process a customer request through the support crew
        
        Args:
            message: Customer message
            session_id: Unique session identifier
            customer_info: Customer context information
            
        Returns:
            Dict with response, agent_used, confidence, escalated status
        """
        try:
            # Analyze message for urgency and complexity
            urgency, complexity = self._analyze_message(message)
            
            # Determine which agent should handle this
            primary_agent = self._route_to_agent(urgency, complexity)
            
            # Create task for the selected agent
            task = Task(
                description=f"""
                Handle this customer request with empathy and accuracy:
                
                Customer Message: "{message}"
                Session ID: {session_id}
                Customer Info: {json.dumps(customer_info or {}, indent=2)}
                Urgency: {urgency}
                Complexity: {complexity}
                
                Instructions:
                1. Understand the customer's issue clearly
                2. Search the knowledge base for relevant information
                3. Provide a helpful, accurate response
                4. If you cannot resolve the issue, escalate appropriately
                5. Be empathetic and professional
                6. Keep the response concise but complete
                
                Response should be direct and helpful.
                """,
                agent=primary_agent,
                expected_output="A helpful customer support response that addresses the customer's concern"
            )
            
            # Execute the task
            result = await asyncio.to_thread(self.crew.kickoff, tasks=[task])
            
            # Extract the response
            response_text = str(result)
            
            # Determine if escalation occurred
            escalated = "escalat" in response_text.lower() or "specialist" in response_text.lower()
            
            # Calculate confidence based on response quality
            confidence = self._calculate_confidence(response_text, message)
            
            return {
                "response": response_text,
                "agent_used": primary_agent.role,
                "confidence": confidence,
                "escalated": escalated,
                "session_id": session_id,
                "urgency": urgency,
                "complexity": complexity
            }
            
        except Exception as e:
            logger.error(f"Error processing customer request: {e}")
            
            # Fallback response
            return {
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again in a moment, or I can connect you with a human agent if this is urgent.",
                "agent_used": "Fallback Handler",
                "confidence": 0.1,
                "escalated": True,
                "session_id": session_id,
                "urgency": "normal",
                "complexity": "high"
            }
    
    def _analyze_message(self, message: str) -> tuple[str, str]:
        """Analyze message for urgency and complexity"""
        
        # Urgency keywords
        urgent_keywords = ["urgent", "emergency", "asap", "immediately", "broken", "down", "not working", "critical"]
        high_keywords = ["problem", "issue", "error", "help", "wrong", "failed"]
        
        # Complexity indicators
        complex_keywords = ["refund", "billing", "account", "technical", "integration", "api", "database"]
        simple_keywords = ["question", "how to", "information", "status", "when", "where"]
        
        message_lower = message.lower()
        
        # Determine urgency
        if any(keyword in message_lower for keyword in urgent_keywords):
            urgency = "urgent"
        elif any(keyword in message_lower for keyword in high_keywords):
            urgency = "high"
        else:
            urgency = "normal"
        
        # Determine complexity
        if any(keyword in message_lower for keyword in complex_keywords):
            complexity = "high"
        elif any(keyword in message_lower for keyword in simple_keywords):
            complexity = "low"
        else:
            complexity = "medium"
        
        return urgency, complexity
    
    def _route_to_agent(self, urgency: str, complexity: str) -> Agent:
        """Route to appropriate agent based on urgency and complexity"""
        
        if urgency == "urgent" or complexity == "high":
            return self.manager_agent
        else:
            return self.support_agent
    
    def _calculate_confidence(self, response: str, original_message: str) -> float:
        """Calculate confidence score for the response"""
        
        # Simple confidence calculation based on response characteristics
        confidence = 0.5  # Base confidence
        
        # Increase confidence for longer, detailed responses
        if len(response) > 100:
            confidence += 0.2
        
        # Increase confidence if response contains specific information
        if any(word in response.lower() for word in ["policy", "process", "contact", "resolve"]):
            confidence += 0.2
        
        # Decrease confidence for escalations
        if "escalat" in response.lower() or "specialist" in response.lower():
            confidence -= 0.3
        
        # Ensure confidence is between 0 and 1
        return max(0.1, min(1.0, confidence))
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all agents"""
        return {
            "support_agent": "active",
            "manager_agent": "active", 
            "quality_agent": "active",
            "crew_status": "operational"
        }
    
    async def get_analytics(self) -> Dict[str, Any]:
        """Get crew analytics"""
        return {
            "total_requests_processed": getattr(self, '_total_requests', 0),
            "average_response_time": 1.2,
            "escalation_rate": 0.08,
            "customer_satisfaction": 4.7,
            "agents_active": 3
        }