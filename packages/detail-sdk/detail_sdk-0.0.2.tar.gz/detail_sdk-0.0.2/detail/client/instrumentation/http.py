import json
from typing import Collection
import vcr
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import get_tracer
from vcr.cassette import Cassette
from vcr.persisters.filesystem import CassetteNotFoundError
from vcr.record_mode import RecordMode
from vcr.serializers import compat
from wrapt import wrap_function_wrapper
from detail.client.instrumentation import NS
from detail.client.logs import get_detail_logger
from detail.client.serialization import DetailEncoder
logger=get_detail_logger(__name__)
def before_record_cb(request):
	A=request
	if A.host.endswith('ingest.sentry.io'):logger.info('ignoring sentry http request');return
	return A
detail_vcr=vcr.VCR(before_record_request=before_record_cb)
def append_wrapper(wrapped,instance,args,kwargs):
	C=wrapped(*args,**kwargs);A,D=instance.data[-1];E=compat.convert_to_unicode(A._to_dict());F=compat.convert_to_unicode(D)
	with get_tracer('http').start_as_current_span(f"{A.method} {A.uri}")as B:B.set_attribute(f"{NS}.library",'external-http');B.set_attribute('external-http.request',json.dumps(E,cls=DetailEncoder));B.set_attribute('external-http.response',json.dumps(F,cls=DetailEncoder))
	return C
class NoopPersister:
	def load_cassette(A,cassette_path,serializer):raise CassetteNotFoundError()
	def save_cassette(A,cassette_path,cassette_dict,serializer):0
class HttpInstrumentor(BaseInstrumentor):
	cassette_manager=None
	def instrumentation_dependencies(A):return[]
	def _instrument(A,**B):detail_vcr.register_persister(NoopPersister());wrap_function_wrapper(Cassette,'append',append_wrapper);A.start_capturing_http()
	def _uninstrument(A,**B):0
	@classmethod
	def start_capturing_http(A):
		if A.cassette_manager:A.stop_capturing_http()
		A.cassette_manager=detail_vcr.use_cassette('<detail span cassette>',record_mode=RecordMode.ALL);A.cassette_manager.__enter__()
	@classmethod
	def stop_capturing_http(A):A.cassette_manager.__exit__();A.cassette_manager=None