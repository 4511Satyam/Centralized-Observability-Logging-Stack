# Centralized Observability & Logging Stack for a Text Summarization Model

## Project 15 - MLOps

This project takes one text-summarization model from the provided reference repository and builds an independent MLOps observability stack around it.

**Model:** `t5-small`  
**Dataset:** No new dataset used for Project 15. The model is adopted from the provided text-summarization project.  
**Main tools:** Hugging Face Transformers, FastAPI, Prometheus, Grafana, Loki, Promtail, Docker, GitHub Actions, Render and psutil.

## Objective

The goal is to monitor a deployed ML inference service from one place. The system collects application metrics with Prometheus, system metrics with psutil, structured JSON logs through Loki, and visualizes metrics and logs in Grafana.

## Architecture

```text
Client
  |
  v
FastAPI + T5-small
  |---- /metrics ----> Prometheus ----\\
  |                                    \\
  |---- JSON logs ----> Loki ----------> Grafana
  |
  +---- psutil CPU/RAM metrics --------/

Docker Compose runs the complete local stack.
GitHub Actions validates configuration and tests.
Render can deploy the FastAPI service.
```

## Features

- Text summarization with `t5-small`
- `/health` endpoint
- `/summarize` endpoint
- Prometheus `/metrics` endpoint
- Request count and error metrics
- Latency histogram
- Input/output token metrics
- CPU and memory monitoring with psutil
- Structured JSON logging
- Loki log aggregation
- Grafana overview dashboard
- Grafana model-performance dashboard
- Docker Compose orchestration
- GitHub Actions CI
- Render deployment configuration

## Local setup

### Option 1: Docker Compose

```bash
docker compose up --build
```

Open:

- API: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Loki: http://localhost:3100

Grafana login:

```text
username: admin
password: admin
```

The first model startup downloads `t5-small`, so the first run may take longer.

### Example API request

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Artificial intelligence is increasingly used in healthcare, education and business. Machine learning systems can process large amounts of information and help organizations automate repetitive tasks while supporting human decision making."}'
```

## Prometheus metrics

Important metrics include:

- `summarization_requests_total`
- `summarization_request_latency_seconds`
- `summarization_input_tokens`
- `summarization_output_tokens`
- `summarization_cpu_percent`
- `summarization_memory_mb`

Example PromQL:

```promql
rate(summarization_requests_total[5m])
```

```promql
rate(summarization_request_latency_seconds_sum[5m])
/
rate(summarization_request_latency_seconds_count[5m])
```

```promql
histogram_quantile(
  0.95,
  sum(rate(summarization_request_latency_seconds_bucket[5m])) by (le)
)
```

## Grafana

Two dashboards are provisioned automatically:

1. **Text Summarization - Overview**
   - total requests
   - error rate
   - average latency
   - memory
   - request rate
   - CPU
   - memory over time

2. **Text Summarization - Model Performance**
   - average input tokens
   - average output tokens
   - p95 latency

## Structured logging and Loki

Application events are written as JSON, for example:

```json
{
  "timestamp": "2026-08-20T08:30:00+00:00",
  "level": "INFO",
  "service": "text-summarization",
  "message": "Summarization completed",
  "event": "prediction",
  "latency_ms": 5200,
  "input_tokens": 100,
  "output_tokens": 30
}
```

Loki is included in the Docker Compose stack and Grafana is configured with a Loki data source.

## GitHub Actions

The CI workflow:

1. Checks out the repository.
2. Installs validation dependencies.
3. Validates Prometheus/Loki/Promtail/Grafana YAML.
4. Runs `docker compose config -q`.
5. Runs pytest.

## Project contribution

The provided GitHub repository is used only as the reference source for the selected summarization model. This repository is a separate implementation focused on Project 15 observability and logging.

## Reproducibility

```bash
git clone <YOUR_REPOSITORY_URL>
cd Centralized-Observability-Logging-Stack
docker compose up --build
```

Then generate several `/summarize` requests and refresh the Grafana dashboards.

## Report screenshots to collect

Before submitting the report, capture:

1. Successful `/summarize` response
2. Prometheus targets page showing the summarization service UP
3. Prometheus graph for request rate
4. Grafana Overview dashboard
5. Grafana Model Performance dashboard
6. Grafana Loki logs
7. GitHub Actions successful run
8. Docker Compose running containers

## Limitations

This is a student-scale observability project. The model is CPU-based and the first startup downloads the Hugging Face model. Loki/Promtail are included for demonstration and local reproducibility; production deployments would normally use persistent storage, authentication, TLS and more robust log shipping.

## Author

Satyam
