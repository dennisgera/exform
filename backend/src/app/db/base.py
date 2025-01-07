from typing import Any
from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Generate tablename automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    def __init__(self, *args, **kwargs) -> None:
        kwargs2 = {k: v for k, v in kwargs.items() if hasattr(self.__class__, k)}
        super().__init__(*args, **kwargs2)
    
    