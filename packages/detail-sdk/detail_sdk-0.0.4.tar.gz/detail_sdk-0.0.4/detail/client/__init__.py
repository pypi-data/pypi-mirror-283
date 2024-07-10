import importlib.metadata,importlib.util,os
from pathlib import Path
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.id_generator import RandomIdGenerator
from opentelemetry.trace.span import format_trace_id
from detail.client import logs
from detail.client.logs import get_detail_logger
from detail.client.otel import JsonLSpanExporter,OTLPJsonHttpExporter
output_dir_path=Path(os.environ.get('__DETAIL_OUTPUT_DIR','.'))
PREFLIGHT_CUSTOMER_HEADER='Preflight-Customer-ID'
PREFLIGHT_VERSION_HEADER='Preflight-Version'
PREFLIGHT_CLIENT_LIBRARY_HEADER='Preflight-Library'
PREFLIGHT_SERVICE_START_ID_HEADER='Preflight-Service-Start-Id'
logger=get_detail_logger(__name__)
try:version=importlib.metadata.version('detail')
except Exception:logger.warning("couldn't read package version",exc_info=True);version='unknown'
def instrument(api_key=None):
	F='true';A=api_key;logs.init();G=f"0x{format_trace_id(RandomIdGenerator().generate_trace_id())}";D=os.environ.get('__DETAIL_DEV','').lower()==F;C=os.environ.get('__DETAIL_USE_LOCAL_BACKEND','').lower()==F;B=None;A=A or os.environ.get('DETAIL_API_KEY')
	if A:
		if C:E='http://localhost:4317'
		else:E='https://preflight-backend.onrender.com'
		B=OTLPJsonHttpExporter(endpoint=f"{E}/v1/traces",headers={PREFLIGHT_CUSTOMER_HEADER:A,PREFLIGHT_VERSION_HEADER:version,PREFLIGHT_CLIENT_LIBRARY_HEADER:'python',PREFLIGHT_SERVICE_START_ID_HEADER:G})
	elif not D or C:logger.warning('No Detail API key set. Use instrument(api_key=) or the DETAIL_API_KEY env var to send traces to the Detail backend.')
	if D and not C:B=JsonLSpanExporter(output_dir_path/'spans.jsonl')
	trace.set_tracer_provider(TracerProvider(shutdown_on_exit=True))
	if B:H=BatchSpanProcessor(B);trace.get_tracer_provider().add_span_processor(H)
	for I in load_instrumentor_classes():I().instrument()
instrumentor_defs=[('times.TimeInstrumentor',[]),('times.DatetimeInstrumentor',[]),('random.OSRandomInstrumentor',[]),('random.SystemRandomInstrumentor',[]),('random.RandomInstrumentor',[]),('uuid.UUIDInstrumentor',[]),('http.HttpInstrumentor',[]),('env.EnvInstrumentor',[]),('sqlite3.SQLite3Instrumentor',[]),('redis.RedisInstrumentor',['redis']),('psycopg2.Psycopg2Instrumentor',['psycopg2']),('flask.DetailFlaskInstrumentor',['flask']),('django.DetailDjangoInstrumentor',['django']),('celery.CeleryInstrumentor',['celery'])]
def load_instrumentor_classes():
	A=[]
	for(D,E)in instrumentor_defs:
		F='detail.client.instrumentation.'+D;G,B=F.rsplit('.',1)
		for C in E:
			H=importlib.util.find_spec(C)
			if not H:logger.info('not loading %s due to missing %s',B,C);break
		else:I=importlib.import_module(G);J=getattr(I,B);A.append(J)
	return A
__all__=[str(A)for A in[instrument,JsonLSpanExporter]]