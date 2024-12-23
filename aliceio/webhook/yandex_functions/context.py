from typing import Optional, Protocol


class RuntimeContext(Protocol):
    function_name: str
    function_version: str
    function_folder_id: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    request_id: str
    log_group_name: str
    log_stream_name: str
    deadline_ms: int
    token: Optional[str]
    aws_request_id: str

    def get_remaining_time_in_millis(self) -> int: ...
