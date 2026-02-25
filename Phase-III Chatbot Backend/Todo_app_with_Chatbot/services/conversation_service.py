"""Conversation service for managing chat history."""
from sqlmodel import Session, select
from typing import List, Optional
from conversation_models.conversation import Conversation, Message
from datetime import datetime
import uuid


class ConversationService:
    """Service for managing conversations and messages."""
    
    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """Create a new conversation session.
        
        Args:
            session: Database session
            user_id: Authenticated user ID
            
        Returns:
            New conversation object
        """
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation
    
    @staticmethod
    def get_conversation(
        session: Session, 
        conversation_id: str, 
        user_id: str
    ) -> Optional[Conversation]:
        """Get conversation by ID with user ownership validation.
        
        Args:
            session: Database session
            conversation_id: Conversation UUID
            user_id: Authenticated user ID for ownership check
            
        Returns:
            Conversation if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id,
            Conversation.user_id == user_id
        )
        result = session.exec(statement)
        return result.first()
    
    @staticmethod
    def save_message(
        session: Session,
        conversation_id: str,
        role: str,
        content: str
    ) -> Message:
        """Save a message to conversation history.
        
        Args:
            session: Database session
            conversation_id: Conversation UUID
            role: Message role ('user' or 'assistant')
            content: Message content
            
        Returns:
            Saved message object
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    
    @staticmethod
    def load_history(
        session: Session,
        conversation_id: str,
        user_id: str,
        limit: int = 50
    ) -> List[Message]:
        """Load conversation history with user ownership validation.
        
        Args:
            session: Database session
            conversation_id: Conversation UUID
            user_id: Authenticated user ID for ownership check
            limit: Maximum messages to retrieve
            
        Returns:
            List of messages ordered by timestamp
        """
        # First verify conversation ownership
        conversation = ConversationService.get_conversation(
            session, conversation_id, user_id
        )
        if not conversation:
            return []
        
        # Load messages
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.asc())
            .limit(limit)
        )
        result = session.exec(statement)
        return result.all()
    
    @staticmethod
    def update_conversation_timestamp(
        session: Session,
        conversation_id: str
    ) -> None:
        """Update conversation's updated_at timestamp.
        
        Args:
            session: Database session
            conversation_id: Conversation UUID
        """
        statement = select(Conversation).where(
            Conversation.conversation_id == conversation_id
        )
        conversation = session.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
