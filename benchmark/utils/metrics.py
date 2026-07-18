import time
import psutil
try:
    import torch
except ImportError:
    torch = None

class MetricsCollector:
    def __init__(self):
        self.metrics = {}
        self.start_time = 0

    def start_timer(self):
        self.start_time = time.time()

    def end_timer(self):
        end_time = time.time()
        return (end_time - self.start_time) * 1000  

    def collect_system_metrics(self):
        cpu_util = psutil.cpu_percent()
        mem_info = psutil.virtual_memory()
        gpu_mem = None
        if torch is not None and torch.cuda.is_available():
            gpu_mem = torch.cuda.memory_allocated()
        return {
            "cpu_utilization": cpu_util,
            "memory_usage_mb": mem_info.used / (1024 * 1024),
            "gpu_memory_allocated_bytes": gpu_mem
        }
