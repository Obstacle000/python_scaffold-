"""统一业务异常体系与错误码定义.

所有业务自定义异常均继承自 `AppError`，由 FastAPI 全局异常处理器统一捕获并返回标准化 JSON。
"""


class AppError(Exception):
    """应用层通用业务异常基类."""

    def __init__(
        self,
        error_code: str = "INTERNAL_SERVER_ERROR",
        message: str = "系统内部异常",
        http_status: int = 500,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.http_status = http_status


class InvalidParamError(AppError):
    """参数校验或格式不合法异常 (HTTP 400)."""

    def __init__(self, message: str = "请求参数不合法") -> None:
        super().__init__("INVALID_PARAM", message, http_status=400)


class UnauthorizedError(AppError):
    """身份认证失败异常 (HTTP 401)."""

    def __init__(self, message: str = "未登录或登录凭证已失效") -> None:
        super().__init__("UNAUTHORIZED", message, http_status=401)


class ForbiddenError(AppError):
    """权限不足拒绝访问异常 (HTTP 403)."""

    def __init__(self, message: str = "无权限执行此操作") -> None:
        super().__init__("FORBIDDEN", message, http_status=403)


class NotFoundError(AppError):
    """目标资源不存在异常 (HTTP 404)."""

    def __init__(self, message: str = "请求的资源未找到") -> None:
        super().__init__("RESOURCE_NOT_FOUND", message, http_status=404)


class ConflictError(AppError):
    """资源冲突或状态互斥异常 (HTTP 409)."""

    def __init__(self, message: str = "资源冲突或当前状态不允许该操作") -> None:
        super().__init__("CONFLICT", message, http_status=409)


class ThirdPartyServiceError(AppError):
    """调用第三方服务/外部接口/大模型 API 异常 (HTTP 502)."""

    def __init__(self, message: str = "外部服务调用失败") -> None:
        super().__init__("THIRD_PARTY_SERVICE_ERROR", message, http_status=502)


class ServiceUnavailableError(AppError):
    """服务不可用或组件连接失败异常 (HTTP 503)."""

    def __init__(self, message: str = "服务暂时不可用") -> None:
        super().__init__("SERVICE_UNAVAILABLE", message, http_status=503)
