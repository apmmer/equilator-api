"""
File to declare SQL models
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from openapi.core.db.main import Base
from openapi.core.db.models_mixins import DBBaseMixin


class DesignationModel(Base, DBBaseMixin):
    __tablename__ = "designations"
    __table_args__ = {"schema": "public"}

    id = Column(
        String(500),
        primary_key=True
    )
    range_definition = Column(
        String(5000),
        unique=True,
        nullable=False
    )
    range_length = Column(
        Integer,
        nullable=False
    )

    def __repr__(self):
        return self.custom_representation(
            id=self.id,
            range_definition=self.range_definition,
            range_length=self.range_length
        )


class WeightedRangeModel(Base, DBBaseMixin):
    __tablename__ = "ranges"
    __table_args__ = {"schema": "public"}

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False
    )
    name = Column(
        String(500),
        unique=True,
        nullable=False
    )
    hash = Column(
        String(1000),
        nullable=False
    )
    definition = Column(
        JSONB,
        nullable=False
    )

    def __repr__(self):
        return self.custom_representation(
            name=self.name, hash=self.hash, definition=self.definition
        )
