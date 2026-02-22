from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)        # REQUIRED
    description = Column(Text, nullable=True)    # OPTIONAL

    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    category_id = Column(Integer, ForeignKey("categories.id"))

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category")