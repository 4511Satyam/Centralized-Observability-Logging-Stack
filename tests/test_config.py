from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

def test_prometheus_config():
    data = yaml.safe_load((ROOT / "prometheus/prometheus.yml").read_text())
    assert "scrape_configs" in data
    assert any(x["job_name"] == "text-summarization" for x in data["scrape_configs"])

def test_loki_config():
    data = yaml.safe_load((ROOT / "loki/loki-config.yml").read_text())
    assert data["auth_enabled"] is False
