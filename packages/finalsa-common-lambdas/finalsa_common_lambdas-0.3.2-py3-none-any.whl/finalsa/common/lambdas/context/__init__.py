from contextvars import ContextVar
from typing import Optional

correlation_id: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)
aws_request_id: ContextVar[Optional[str]] = ContextVar('aws_request_id', default=None)
