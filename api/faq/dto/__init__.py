from dataclasses import dataclass


@dataclass
class ErrorBody:
    reason: str
    detail: str

    def __init__(self, reason=None, detail=None) -> None:
        self.reason = reason
        self.detail = detail
