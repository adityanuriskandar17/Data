# ============================================
# PIPELINE MONITORING & ALERTING
# ============================================
# Bahasa Indonesia

import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any
import json

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/log/pipeline_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# METRIK PIPELINE
# ============================================

class PipelineMetrics:
    """Mengumpulkan metrik dari pipeline."""

    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.start_time = None
        self.end_time = None
        self.rows_read = 0
        self.rows_written = 0
        self.errors = 0
        self.warnings = 0

    def start(self):
        self.start_time = time.time()
        logger.info(f"Pipeline '{self.pipeline_name}' dimulai")

    def stop(self):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        logger.info(f"Pipeline '{self.pipeline_name}' selesai dalam {duration:.2f} detik")
        return self.summary()

    def summary(self) -> Dict[str, Any]:
        duration = self.end_time - self.start_time if self.end_time else 0
        return {
            "pipeline": self.pipeline_name,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "duration_seconds": round(duration, 2),
            "rows_read": self.rows_read,
            "rows_written": self.rows_written,
            "errors": self.errors,
            "warnings": self.warnings,
            "throughput": round(self.rows_read / duration, 2) if duration > 0 else 0
        }


# ============================================
# ALERTING
# ============================================

class AlertManager:
    """Mengirim notifikasi jika terjadi masalah."""

    def __init__(self, slack_webhook: str = None, email: str = None):
        self.slack_webhook = slack_webhook
        self.email = email

    def send_slack(self, message: str):
        """Kirim notifikasi ke Slack."""
        if not self.slack_webhook:
            return
        import requests
        payload = {"text": f"[ALERT] {message}"}
        try:
            requests.post(self.slack_webhook, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Gagal kirim Slack: {e}")

    def alert_on_failure(self, pipeline: str, error: str):
        alert_msg = f"Pipeline '{pipeline}' GAGAL!\nError: {error}"
        logger.error(alert_msg)
        self.send_slack(alert_msg)

    def alert_on_slow_pipeline(self, pipeline: str, duration: float, threshold: float):
        if duration > threshold:
            alert_msg = f"Pipeline '{pipeline}' lambat! Durasi: {duration:.2f}s (threshold: {threshold}s)"
            logger.warning(alert_msg)
            self.send_slack(alert_msg)


# ============================================
# SLI / SLO TRACKING
# ============================================

class SLOTracker:
    """Melacak Service Level Indicators (SLI) untuk pipeline."""

    def __init__(self):
        self.total_runs = 0
        self.successful_runs = 0
        self.failed_runs = 0
        self.latencies = []

    def record_run(self, success: bool, latency: float):
        self.total_runs += 1
        if success:
            self.successful_runs += 1
        else:
            self.failed_runs += 1
        self.latencies.append(latency)

    def success_rate(self) -> float:
        """SLO: Persentase pipeline yang sukses."""
        if self.total_runs == 0:
            return 0
        return (self.successful_runs / self.total_runs) * 100

    def p95_latency(self) -> float:
        """SLO: Latency percentile 95."""
        if not self.latencies:
            return 0
        sorted_lat = sorted(self.latencies)
        idx = int(len(sorted_lat) * 0.95)
        return sorted_lat[idx]

    def report(self):
        print(f"""
        === SLO Report ===
        Total Runs: {self.total_runs}
        Success Rate: {self.success_rate():.1f}%
        P95 Latency: {self.p95_latency():.2f}s
        ==================
        """)
