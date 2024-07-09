import logging
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterable,
    Iterator,
    Mapping,
    Dict,
    Tuple,
)

import dashscope
from opentelemetry.util.types import AttributeValue
from aliyun.semconv.trace import SpanAttributes, EmbeddingAttributes,AliyunSpanKindValues


class ResponseKey:
    REQUEST_ID = "request_id"

    STATUS_CODE = "status_code"

    OUTPUT = "output"
    '''
    output key
    '''
    FINISH_REASON = "finish_reason"

    TEXT = "text"

    USAGE = "usage"
    '''
    usage key
    '''
    TOTAL_TOKENS = "total_tokens"

    OUTPUT_TOKENS = "output_tokens"

    INPUT_TOKENS = "input_tokens"

    CHOICES = "choices"
    '''
    choices keys 
    '''
    MESSAGE = "message"
    '''
    message keys
    '''
    MESSAGE_ROLE = "role"

    MESSAGE_CONTENT = "content"

    TEXT = "text"

    EMBEDDINGS = "embeddings"

    EMBEDDING = "embedding"


SPEC_KEY_MAP = {
    ResponseKey.REQUEST_ID: "request_id",
    ResponseKey.STATUS_CODE: "status_code",
    ResponseKey.FINISH_REASON: SpanAttributes.GEN_AI_RESPONSE_FINISH_REASON,
    ResponseKey.TOTAL_TOKENS: SpanAttributes.GEN_AI_USAGE_TOTAL_TOKENS,
    ResponseKey.OUTPUT_TOKENS: SpanAttributes.GEN_AI_USAGE_COMPLETION_TOKENS,
    ResponseKey.INPUT_TOKENS: SpanAttributes.GEN_AI_USAGE_PROMPT_TOKENS,
    ResponseKey.TEXT: SpanAttributes.OUTPUT_VALUE,
    ResponseKey.EMBEDDINGS: SpanAttributes.EMBEDDING_EMBEDDINGS
}

RESPONSE_KEY_LIST = [ResponseKey.REQUEST_ID, ResponseKey.STATUS_CODE, ResponseKey.OUTPUT, ResponseKey.USAGE]
OUTPUT_KEY_LIST = [ResponseKey.TEXT, ResponseKey.FINISH_REASON, ResponseKey.EMBEDDINGS]
USAGE_KEY_LIST = [ResponseKey.TOTAL_TOKENS, ResponseKey.OUTPUT_TOKENS, ResponseKey.INPUT_TOKENS]
MESSAGE_KEY_LIST = [ResponseKey.MESSAGE_ROLE, ResponseKey.MESSAGE_CONTENT]


class ResponseAttributesExtractor:

    def _is_stream(self, resp_type: type):
        pass

    def _serialize_json(self,obj: Any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)

    def extract(self, response: Dict[str, Any]) -> Iterable[Tuple[str, AttributeValue]]:
        logging.debug(f"***************** response key: {response},type: {type(response)}")
        for response_key in RESPONSE_KEY_LIST:
            if response_key in response:
                resp_val = response[response_key]
                logging.debug(f"{response_key}: {resp_val}")
                if resp_val is not None and response_key in SPEC_KEY_MAP:
                    yield SPEC_KEY_MAP[response_key], resp_val
                if response_key == ResponseKey.OUTPUT:
                    output = response[response_key]
                    yield SpanAttributes.OUTPUT_VALUE, f"{output}"
                    logging.debug(f"output: {output},output type: {type(output)}")
                    for output_key in OUTPUT_KEY_LIST:
                        output_val = response[response_key]
                        if output_key in output_val and output_key in SPEC_KEY_MAP:
                            output_value = response[response_key][output_key]
                            logging.debug(f"{response_key}: {output_value}")
                            yield SPEC_KEY_MAP[output_key], output_value
                        if output_key == ResponseKey.EMBEDDINGS and output_key in output_val:
                            embeddings = output_val[output_key]
                            for idx in range(len(embeddings)):
                                embedding = embeddings[idx]
                                yield f"{SpanAttributes.EMBEDDING_EMBEDDINGS}.{idx}.{EmbeddingAttributes.EMBEDDING_VECTOR_SIZE}", len(
                                    embedding)
                    if ResponseKey.TEXT in output and ResponseKey.CHOICES not in output:
                        yield f"{SpanAttributes.GEN_AI_COMPLETION}.{0}.{ResponseKey.MESSAGE_CONTENT}", output[
                            ResponseKey.TEXT]
                    if ResponseKey.CHOICES in output:
                        choices = output[ResponseKey.CHOICES]
                        for idx in range(len(choices)):
                            choice = choices[idx]
                            if ResponseKey.MESSAGE in choice:
                                message = choice[ResponseKey.MESSAGE]
                                for message_key in MESSAGE_KEY_LIST:
                                    if message_key in message:
                                        yield f"{SpanAttributes.GEN_AI_COMPLETION}.{idx}.message.{message_key}", \
                                        message[message_key]
                if response_key == ResponseKey.USAGE:
                    for usage_key in USAGE_KEY_LIST:
                        if usage_key in response[response_key] and usage_key in SPEC_KEY_MAP:
                            usage_value = response[response_key][usage_key]
                            logging.debug(f"{usage_key}: {usage_value}")
                            yield SPEC_KEY_MAP[usage_key], usage_value

        # return None
