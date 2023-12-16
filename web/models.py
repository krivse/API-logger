from sqlalchemy import Column, SmallInteger, String, DateTime, UUID, Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Log(Base):
    __tablename__ = 'log'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ip_address = Column(INET)
    http_method = Column(String)
    uri = Column(Text)
    http_status_code = Column(SmallInteger)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
