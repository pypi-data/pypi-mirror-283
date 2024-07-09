import logging
from importlib import import_module
from typing import Any, Collection

import dashscope
from aliyun.instrumentation.dashscope.package import _instruments
from aliyun.instrumentation.dashscope.version import __version__
from aliyun.instrumentation.dashscope._wrapper import DashscopeRequestWrapper, DashscopeResponseWrapper
from opentelemetry import trace as trace_api
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor  # type: ignore
from wrapt import wrap_function_wrapper



logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
_MODULE = "dashscope.client.base_api"
__all__ = ["AliyunDashScopeInstrumentor"]
class AliyunDashScopeInstrumentor(BaseInstrumentor):  # type: ignore
    """
    An instrumentor for openai
    """

    __slots__ = (
        "_original_call",
    )

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments

    def _instrument(self, **kwargs: Any) -> None:
        if not (tracer_provider := kwargs.get("tracer_provider")):
            tracer_provider = trace_api.get_tracer_provider()
        tracer = trace_api.get_tracer(__name__, __version__, tracer_provider)
        wrap_function_wrapper(
            module=_MODULE,
            name="BaseApi.call",
            wrapper=DashscopeRequestWrapper(tracer=tracer),
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        pass
