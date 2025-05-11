from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Request latency')