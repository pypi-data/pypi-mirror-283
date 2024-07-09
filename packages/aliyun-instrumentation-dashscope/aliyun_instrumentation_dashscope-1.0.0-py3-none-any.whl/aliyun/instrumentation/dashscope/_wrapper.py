from dashscope.api_entities.dashscope_response import DashScopeAPIResponse
from aliyun.instrumentation.dashscope._request_attributes_extractor import RequestAttributesExtractor
from aliyun.instrumentation.dashscope._response_attributes_extractor import  ResponseAttributesExtractor
from aliyun.instrumentation.dashscope._with_span import _WithSpan
from aliyun.semconv.trace import AliyunSpanKindValues
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Tuple,
)
from abc import ABC
from opentelemetry import trace as trace_api
from contextlib import contextmanager
from opentelemetry.util.types import AttributeValue
from opentelemetry.context import _SUPPRESS_INSTRUMENTATION_KEY
from opentelemetry.trace import INVALID_SPAN
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class _WithTracer(ABC):
    def __init__(self, tracer: trace_api.Tracer, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._request_attributes_extractor = RequestAttributesExtractor()
        self._response_attributes_extractor = ResponseAttributesExtractor()
        self._tracer = tracer

    @contextmanager
    def _start_as_current_span(
        self,
        span_name: str,
        attributes: Iterable[Tuple[str, AttributeValue]],
        extra_attributes: Iterable[Tuple[str, AttributeValue]],
    ) -> Iterator[_WithSpan]:
        # Because OTEL has a default limit of 128 attributes, we split our attributes into
        # two tiers, where the addition of "extra_attributes" is deferred until the end
        # and only after the "attributes" are added.
        try:
            span = self._tracer.start_span(name=span_name, attributes=dict(attributes))
        except Exception:
            logger.exception("Failed to start span")
            span = INVALID_SPAN
        with trace_api.use_span(
            span,
            end_on_exit=False,
            record_exception=False,
            set_status_on_exception=False,
        ) as span:
            yield _WithSpan(span=span, extra_attributes=dict(extra_attributes))



class DashscopeRequestWrapper(_WithTracer):

    def _finalize_response(
        self,
        response: Any,
        with_span: _WithSpan,
        cast_to: type,
        request_parameters: Mapping[str, Any],
    ) -> Any:
        logger.debug(f"response: {type(response)}  ------ {response.__reduce__}")
        if isinstance(response, DashScopeAPIResponse):
            logger.debug(f"DashScopeAPIResponse: {dict(response)}")
        resp_attr = self._response_attributes_extractor.extract(dict(response))
        logger.debug(f"resp_attr: {resp_attr}")
        with_span.finish_tracing(
            status=trace_api.Status(status_code=trace_api.StatusCode.OK),
            attributes=dict(resp_attr),
            extra_attributes=dict(resp_attr),
        )
        return response


    def __call__(
        self,
        wrapped: Callable[..., Any],
        instance: Any,
        args: Tuple[type, Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        logger.debug(f"wrapped kwargs: {instance}")
        if instance is  None:
            return wrapped(*args, **kwargs)
        with self._start_as_current_span(
            span_name=AliyunSpanKindValues.LLM.value,
            attributes= self._request_attributes_extractor.extract(kwargs),
            extra_attributes=self._request_attributes_extractor.extract(kwargs),
        ) as with_span:
            try:
                response = wrapped(*args, **kwargs)
            except Exception as exception:
                with_span.record_exception(exception)
                status = trace_api.Status(
                    status_code=trace_api.StatusCode.ERROR,
                    # Follow the format in OTEL SDK for description, see:
                    # https://github.com/open-telemetry/opentelemetry-python/blob/2b9dcfc5d853d1c10176937a6bcaade54cda1a31/opentelemetry-api/src/opentelemetry/trace/__init__.py#L588  # noqa E501
                    description=f"{type(exception).__name__}: {exception}",
                )
                with_span.finish_tracing(status=status)
                raise
            try:
                response = self._finalize_response(
                    response=response,
                    with_span=with_span,
                    cast_to=None,
                    request_parameters=kwargs,
                )
            except Exception:
                logger.warn(f"Failed to finalize response of type {type(response)}, {response.__qualname__}")
                logger.warn(f"[DashscopeRequestWrapper][with_call_wrapper]response err: {response}")

                with_span.finish_tracing()

        return response

class DashscopeResponseWrapper(_WithTracer):

    def __call__(
        self,
        wrapped: Callable[..., Any],
        instance: Any,
        args: Tuple[type, Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        if instance is not None:
            logger.debug(f"[DashscopeResponseWrapper][with_call_wrapper]kwargs: {kwargs}")
            # self._response_attributes_extractor.extract(kwargs)
        with self._start_as_current_span(
            span_name=AliyunSpanKindValues.LLM.value,
            attributes= self._response_attributes_extractor.extract(kwargs),
            extra_attributes=self._response_attributes_extractor.extract(kwargs),
        ) as with_span:
            try:
                response = wrapped(*args, **kwargs)
            except Exception as exception:
                with_span.record_exception(exception)
                status = trace_api.Status(
                    status_code=trace_api.StatusCode.ERROR,
                    # Follow the format in OTEL SDK for description, see:
                    # https://github.com/open-telemetry/opentelemetry-python/blob/2b9dcfc5d853d1c10176937a6bcaade54cda1a31/opentelemetry-api/src/opentelemetry/trace/__init__.py#L588  # noqa E501
                    description=f"{type(exception).__name__}: {exception}",
                )
                with_span.finish_tracing(status=status)
                raise
            try:
                response = self._finalize_response(
                    response=response,
                    with_span=with_span,
                    cast_to=cast_to,
                    request_parameters=request_parameters,
                )
            except Exception:
                logger.exception(f"Failed to finalize response of type {type(response)}")
                with_span.finish_tracing()
        return wrapped(*args, **kwargs)

