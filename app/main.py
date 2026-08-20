import logging
import time
import psutil

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

from app.logging_config import configure_logging
from app.metrics import REQUESTS, LATENCY, INPUT_TOKENS, OUTPUT_TOKENS, CPU_PERCENT, MEMORY_MB
from app.model import load_model, summarize_text

configure_logging()
logger = logging.getLogger("text-summarization")

app = FastAPI(
    title="Text Summarization Observability API",
    version="1.0.0",
    description="A student MLOps project using T5-small with Prometheus, Grafana and Loki.",
)

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to summarize")
    num_beams: int = Field(4, ge=1, le=8)
    length_penalty: float = Field(1.0, ge=0.1, le=3.0)

class SummarizeResponse(BaseModel):
    summary: str
    latency_sec: float
    input_tokens: int
    output_tokens: int
    model: str

@app.on_event("startup")
def startup():
    load_model()
    logger.info("Model loaded", extra={"event": "startup"})

@app.get("/")
def root():
    return {"service": "text-summarization", "docs": "/docs", "metrics": "/metrics"}

@app.get("/health")
def health():
    return {"status": "healthy", "model": "t5-small"}

@app.get("/metrics")
def metrics():
    process = psutil.Process()
    CPU_PERCENT.set(process.cpu_percent(interval=0.05))
    MEMORY_MB.set(process.memory_info().rss / 1024 / 1024)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    if not request.text.strip():
        REQUESTS.labels(status="error").inc()
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    start = time.perf_counter()
    try:
        summary, input_tokens, output_tokens = summarize_text(
            request.text,
            num_beams=request.num_beams,
            length_penalty=request.length_penalty,
        )
        latency = time.perf_counter() - start
        INPUT_TOKENS.observe(input_tokens)
        OUTPUT_TOKENS.observe(output_tokens)
        LATENCY.observe(latency)
        REQUESTS.labels(status="success").inc()

        process = psutil.Process()
        CPU_PERCENT.set(process.cpu_percent(interval=0.05))
        MEMORY_MB.set(process.memory_info().rss / 1024 / 1024)

        logger.info(
            "Summarization completed",
            extra={
                "event": "prediction",
                "latency_ms": round(latency * 1000, 2),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            },
        )

        return SummarizeResponse(
            summary=summary,
            latency_sec=round(latency, 4),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model="t5-small",
        )
    except Exception as exc:
        REQUESTS.labels(status="error").inc()
        logger.exception("Summarization failed", extra={"event": "prediction_error"})
        raise HTTPException(status_code=500, detail=str(exc))
