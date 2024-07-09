from aliyun.instrumentation.llama_index.internal._callback import \
    OpenInferenceTraceCallbackHandler as _OpenInferenceTraceCallbackHandler
from opentelemetry import trace


class AliyunCallbackHandler(_OpenInferenceTraceCallbackHandler):

    def __init__(self, tracer: trace.Tracer) -> None:
        super().__init__(tracer=tracer)
