from prometheus_client import Counter, Histogram, Gauge

REQUESTS = Counter(
    "summarization_requests_total",
    "Total summarization API requests",
    ["status"],
)

LATENCY = Histogram(
    "summarization_request_latency_seconds",
    "Summarization request latency in seconds",
    buckets=(0.5, 1, 2, 3, 5, 10, 20, 30, 60),
)

INPUT_TOKENS = Histogram(
    "summarization_input_tokens",
    "Number of input tokens",
    buckets=(10, 50, 100, 250, 500, 750, 1000, 1500, 2000),
)

OUTPUT_TOKENS = Histogram(
    "summarization_output_tokens",
    "Number of output tokens",
    buckets=(5, 10, 20, 30, 50, 75, 100, 150, 200),
)

CPU_PERCENT = Gauge("summarization_cpu_percent", "Current process CPU percentage")
MEMORY_MB = Gauge("summarization_memory_mb", "Current process RSS memory in MB")
