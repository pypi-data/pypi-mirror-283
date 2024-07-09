import logging
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Tuple,
)
from urllib.request import Request

from opentelemetry.util.types import AttributeValue
from aliyun.semconv.trace import SpanAttributes, AliyunSpanKindValues, EmbeddingAttributes

'''
REQUEST KEY
'''


class RequestKey:
    '''
    model
    '''
    MODEL = "model"

    TASK_GROUP = "task_group"

    TASK = "task"

    FUNCTION = "function"

    TEMPERATURE = "temperature"

    TOP_P = "top_p"

    TOP_K = "top_k"

    INPUT = "input"

    '''
    input value
    '''
    PROMPT = "prompt"
    '''
    message
    '''
    MESSAGES = "messages"

    TEXTS = "texts"


class MessageKey:
    ROLE = "role"

    CONTENT = "content"


REQUEST_KEY_LIST = [
    RequestKey.MODEL,
    RequestKey.TASK_GROUP,
    RequestKey.TASK,
    RequestKey.FUNCTION,
    RequestKey.TEMPERATURE,
    RequestKey.TOP_P,
    # RequestKey.TOP_K,
    RequestKey.INPUT,
    RequestKey.PROMPT,
]

MESSAGE_KEY_LIST = [
    MessageKey.ROLE,
    MessageKey.CONTENT,
]

SPEC_MAP = {
    RequestKey.MODEL: SpanAttributes.GEN_AI_MODEL_NAME,
    RequestKey.TASK_GROUP: "task_group",
    RequestKey.TASK: "task",
    RequestKey.FUNCTION: SpanAttributes.GEN_AI_REQUEST_TOOL_CALLS,
    RequestKey.TEMPERATURE: SpanAttributes.GEN_AI_REQUEST_TEMPERATURE,
    RequestKey.TOP_P: SpanAttributes.GEN_AI_REQUEST_TOP_P,
    RequestKey.INPUT: SpanAttributes.INPUT_VALUE,
    RequestKey.PROMPT: SpanAttributes.GEN_AI_PROMPT,
}


class RequestAttributesExtractor(object):

    def _get_span_kind(self, cast_to: type) -> str:
        return (
            AliyunSpanKindValues.EMBEDDING.value
            if cast_to is self._openai.types.CreateEmbeddingResponse
            else AliyunSpanKindValues.LLM.value
        )

    def _is_embedded_request(self, request: Mapping[str, Any]) -> bool:
        if RequestKey.FUNCTION in request:
            function_name = request[RequestKey.FUNCTION]
            logging.debug(f"------Function: {function_name}")
            if "embedding" in function_name:
                return True
            return False

    def extract(self, request: Mapping[str, Any]) -> Iterable[Tuple[str, AttributeValue]]:
        logging.debug(f"Extracting: {request}")
        for request_key in SPEC_MAP:
            if request_key in request:
                logging.debug(f"{request_key}: {request[request_key]}")
                request_value = request[request_key]
                if request_key == RequestKey.MODEL and self._is_embedded_request(request):
                    yield SpanAttributes.EMBEDDING_MODEL_NAME, request[RequestKey.MODEL]
                if request_value is not None:
                    yield SPEC_MAP[request_key], request[request_key]
                if request_key == RequestKey.INPUT:
                    yield SpanAttributes.INPUT_VALUE, f"{request[RequestKey.INPUT]}"
                    if RequestKey.PROMPT in request[request_key]:
                        prompt_val = request[request_key][RequestKey.PROMPT]
                        logging.debug(f"{RequestKey.PROMPT}: {prompt_val}")
                        yield SPEC_MAP[request_key], prompt_val
                    if RequestKey.MESSAGES in request[request_key]:
                        logging.debug(f"------Messagesddd: {request[request_key][RequestKey.MESSAGES]}")
                        messages = request[request_key][RequestKey.MESSAGES]
                        for idx in range(len(messages)):
                            meesage = messages[idx]
                            logging.debug(f"message info : {idx},{meesage}")
                            yield f"{SpanAttributes.GEN_AI_PROMPT}.{idx}.message.{MessageKey.ROLE}", meesage[
                                MessageKey.ROLE]
                            yield f"{SpanAttributes.GEN_AI_PROMPT}.{idx}.message.{MessageKey.CONTENT}", meesage[
                                MessageKey.CONTENT]

                    if RequestKey.TEXTS in request[request_key] and self._is_embedded_request(request):
                        texts = request[request_key][RequestKey.TEXTS]
                        for idx in range(len(texts)):
                            text = texts[idx]
                            logging.debug(f"text info : {idx},{text}")
                            yield f"{SpanAttributes.EMBEDDING_EMBEDDINGS}.{idx}.{EmbeddingAttributes.EMBEDDING_TEXT}", text

                if self._is_embedded_request(request):
                    yield SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.EMBEDDING.value
                else:
                    yield SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.LLM.value

        # return None
