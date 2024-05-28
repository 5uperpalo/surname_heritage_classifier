from typing import Any, Union
from pathlib import Path
from datetime import datetime

import dill
from prometheus_api_client import PrometheusConnect


def get_kepler_pod_stats(
    to_timestamp: float,
    from_timestamp: float,
    prometheus_url: str = "http://prometheus-kube-prometheus-prometheus.monitoring:9090",
    container_namespace: str = "jupyterhub",
    pod_name: str = "jupyter-5uperpalo",
) -> dict:
    """Function to query Kepler power consumption data of specific pod in Kubernetes.

    # https://sustainable-computing.io/design/kepler-energy-sources/
    # https://github.com/sustainable-computing-io/kepler/blob/1c397ff00b72b5cb1585d0de2cd495c73d88f07a/grafana-dashboards/Kepler-Exporter.json#L299
    # https://prometheus.io/docs/prometheus/latest/querying/basics/#time-durations
    # [metric for metric in prom.all_metrics() if "kepler" in metric]

    Args:
        to_timestamp (list): 'to' timestamp
        from_timestamp (list): 'from' timestamp
        prometheus_url (str): Prometheus service url
        container_namespace (str): Kubernetes pod namespace name
        pod_name (str): Kubernetes namespace name
    Returns:
        metrics (dict): Kepler metrics of the power consumption of pod in Kubernetes
    """
    prom = PrometheusConnect(url=prometheus_url, disable_ssl=True)

    pod_name = f"'{pod_name}'"
    container_namespace = f"'{container_namespace}'"

    time_range_sec = str(int(to_timestamp - from_timestamp))
    container_sum_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"
    container_core_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_core_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"
    container_uncore_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_uncore_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"
    container_pkg_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_package_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"
    container_dram_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_dram_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"
    container_other_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_other_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"
    container_gpu_query = f"sum by (pod_name, container_namespace) (irate(kepler_container_gpu_joules_total{{container_namespace={container_namespace}, pod_name={pod_name}}}[{time_range_sec}s] @ {str(to_timestamp)}))"

    sum_data = prom.custom_query(query=container_sum_query)
    core_data = prom.custom_query(query=container_core_query)
    uncore_data = prom.custom_query(query=container_uncore_query)
    pkg_data = prom.custom_query(query=container_pkg_query)
    dram_data = prom.custom_query(query=container_dram_query)
    other_data = prom.custom_query(query=container_other_query)
    gpu_data = prom.custom_query(query=container_gpu_query)

    metrics = {
        "from": datetime.fromtimestamp(from_timestamp).strftime("%m/%d/%Y, %H:%M:%S"),
        "to": datetime.fromtimestamp(to_timestamp).strftime("%m/%d/%Y, %H:%M:%S"),
        "sum": float(sum_data[0]["value"][1]),
        "core": float(core_data[0]["value"][1]),
        "uncore": float(uncore_data[0]["value"][1]),
        "pkg": float(pkg_data[0]["value"][1]),
        "dram": float(dram_data[0]["value"][1]),
        "other": float(other_data[0]["value"][1]),
        "gpu": float(gpu_data[0]["value"][1]),
    }
    return metrics


def intsec(list1: list, list2: list) -> list:
    """Simple intesection of two lists.
    Args:
        list1 (list): list1
        list2 (list): list2
    Returns:
        list (list): intersection of lists
    """
    return list(set.intersection(set(list1), set(list2)))


def dill_load(file_loc: Union[str, Path]) -> Any:
    """Helper function to open/close dill file,
    otherwise the python outputs warning that the file remains opened

    Args:
        file_loc (str): location of the file
    Returns:
        content (dict): content of dill file, usually dictionary
    """
    with open(file_loc, "rb") as f:
        content = dill.load(f)
    return content


def dill_dump(file_loc: Union[str, Path], content: object):
    """Helper function to open/close dill file and dump content into it,
    otherwise the python outputs warning that the file remains opened

    Args:
        file_loc (str): location of the file
        content (object): data that will be saved to dill, usually dictionary
    """
    with open(file_loc, "wb") as f:
        dill.dump(content, f)
