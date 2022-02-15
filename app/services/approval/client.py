from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.future import Engine

from app.services.approval.models import ApprovalEntities


class ApprovalServiceClient:
    """Get information about approval request or entities for copy request."""

    def __init__(self, engine: Engine, metadata: MetaData) -> None:
        self.engine = engine
        self.metadata = metadata

        self.approval_entity = Table(
            'approval_entity',
            self.metadata,
            Column('id', UUID(as_uuid=True), unique=True, primary_key=True, default=uuid4),
            keep_existing=True,
            autoload_with=self.engine,
        )

    def get_approval_entities(self, request_id: str) -> ApprovalEntities:
        """Return all approval entities related to request id."""

        statement = select(self.approval_entity).filter_by(request_id=request_id)
        cursor = self.engine.connect().execute(statement)

        request_approval_entities = ApprovalEntities.from_cursor(cursor)

        return request_approval_entities
