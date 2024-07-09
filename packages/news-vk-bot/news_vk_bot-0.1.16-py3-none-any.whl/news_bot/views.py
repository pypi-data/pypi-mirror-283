import requests
from django.http import HttpResponse
from prometheus_client import (CONTENT_TYPE_LATEST, CollectorRegistry,
                               generate_latest)
from prometheus_client.core import Metric
from prometheus_client.parser import text_string_to_metric_families

from monitoring.constants import METRICS_ADDRESS


class CustomCollector:
    def collect(self):
        bot_metrics = fetch_bot_metrics()
        for family in text_string_to_metric_families(bot_metrics):
            for sample in family.samples:
                metric_family = Metric(family.name, family.documentation, family.type)
                metric_family.add_sample(sample.name, sample.labels, sample.value)
                yield metric_family


def fetch_bot_metrics():
    response = requests.get(METRICS_ADDRESS)
    return response.text


def get_metrics_from_bot(request):
    registry = CollectorRegistry()
    registry.register(CustomCollector())

    merged_metrics = generate_latest(registry)
    return HttpResponse(merged_metrics, content_type=CONTENT_TYPE_LATEST)
