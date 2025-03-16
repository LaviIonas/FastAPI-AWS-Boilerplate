from database import Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

# User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
    # Relationships
    # papers = relationship("UserPaper", back_populates="user")

# # Research Paper model
# class Paper(Base):
#     __tablename__ = "papers"

#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String, nullable=False)
#     authors = Column(String, nullable=False)
#     abstract = Column(Text)
#     url = Column(String)
#     doi = Column(String, unique=True)
#     publication_date = Column(TIMESTAMP(timezone=True))
#     journal = Column(String)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
#     # Relationships
#     users = relationship("UserPaper", back_populates="paper")
#     llm_outputs = relationship("LLMOutput", back_populates="paper")

# # Junction table for many-to-many relationship between users and papers
# class UserPaper(Base):
#     __tablename__ = "user_papers"

#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
#     paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), primary_key=True)
#     notes = Column(Text)
#     saved_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
#     # Relationships
#     user = relationship("User", back_populates="papers")
#     paper = relationship("Paper", back_populates="users")

# # LLM outputs associated with papers
# class LLMOutput(Base):
#     __tablename__ = "llm_outputs"
    
#     id = Column(Integer, primary_key=True, nullable=False)
#     paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
#     output_type = Column(String, nullable=False)  # e.g., "summary", "critique", "key_points"
#     content = Column(Text, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    
#     # Relationships
#     paper = relationship("Paper", back_populates="llm_outputs")