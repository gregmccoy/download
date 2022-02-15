from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.engine import CursorResult


class EntityType(str, Enum):
    FOLDER = 'folder'
    FILE = 'file'


class ReviewStatus(str, Enum):
    DENIED = 'denied'
    PENDING = 'pending'
    APPROVED = 'approved'


class CopyStatus(str, Enum):
    PENDING = 'pending'
    COPIED = 'copied'


class ApprovalEntity(BaseModel):
    """Model to represent one approval entity."""

    id: UUID
    request_id: Optional[UUID]
    entity_geid: Optional[str]
    entity_type: Optional[EntityType]
    review_status: Optional[ReviewStatus]
    parent_geid: Optional[str]
    copy_status: Optional[CopyStatus]
    name: str

    class Config:
        orm_mode = True


class ApprovalEntities(dict):
    """Store multiple approval entities from one request using entity geid as a key."""

    @classmethod
    def from_cursor(cls, result: CursorResult) -> 'ApprovalEntities':
        """Load approval entities from sqlalchemy cursor result."""

        instance = cls()
        for entity in result:
            approval_entity = ApprovalEntity.from_orm(entity)
            instance[approval_entity.entity_geid] = approval_entity

        return instance
