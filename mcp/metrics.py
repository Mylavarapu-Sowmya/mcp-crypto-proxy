
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

REQUEST_COUNT = Counter('mcp_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('mcp_request_latency_seconds', 'Request latency', ['endpoint'])

def metrics_response():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
