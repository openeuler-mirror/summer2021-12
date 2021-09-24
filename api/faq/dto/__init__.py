from dataclasses import dataclass


class Processable(object):
    """
    用于定义 dto 内容扫描的具体规则（例如敏感信息扫描等）
    """
    def process(self):
        return self


@dataclass
class ErrorBody:
    reason: str
    detail: str

    def __init__(self, reason=None, detail=None) -> None:
        self.reason = reason
        self.detail = detail
