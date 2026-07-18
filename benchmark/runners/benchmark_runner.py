import time
import json
import csv
import logging
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark.adapters.minifasnet_adapter import MiniFASNetAdapter
from benchmark.adapters.tscan_adapter import TSCANAdapter
from benchmark.adapters.physnet_adapter import PhysNetAdapter
from benchmark.adapters.shield_fas_adapter import ShieldAntiSpoofAdapter
from benchmark.adapters.shield_rppg_adapter import ShieldRPPGAdapter
from benchmark.utils.metrics import MetricsCollector

logging.basicConfig(filename='benchmark.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BenchmarkRunner:
    def __init__(self):
        self.models = [
            MiniFASNetAdapter(),
            TSCANAdapter(),
            PhysNetAdapter(),
            ShieldAntiSpoofAdapter(),
            ShieldRPPGAdapter()
        ]
        self.metrics_collector = MetricsCollector()
        self.results = []
        self.timings = []
        self.metadata = []

    def run(self, num_samples=15):
        logging.info("Starting Benchmark Runner")
        
        for m in self.models:
            self.metadata.append(m.metadata())
        with open('model_metadata.json', 'w') as f:
            json.dump(self.metadata, f, indent=4)
            
        sys_metrics = self.metrics_collector.collect_system_metrics()
        with open('system_info.json', 'w') as f:
            json.dump(sys_metrics, f, indent=4)

        for model in self.models:
            logging.info(f"Loading model {model.metadata()['name']}")
            try:
                model.load_model()
            except Exception as e:
                logging.error(f"Failed to load {model.metadata()['name']}: {str(e)}")
                continue

            for i in range(num_samples):
                dummy_input = {'image': np.zeros((480, 640, 3), dtype=np.uint8), 'bbox': (100, 100, 200, 200)}
                
                try:
                    self.metrics_collector.start_timer()
                    tensor = model.preprocess(dummy_input)
                    if tensor is None:
                        continue 
                    
                    raw_out = model.infer(tensor)
                    final_out = model.postprocess(raw_out)
                    
                    latency = self.metrics_collector.end_timer()
                    if final_out:
                        final_out['latency_ms'] = latency
                        self.results.append(final_out)
                        self.timings.append({'model': final_out['model'], 'sample': i, 'latency_ms': latency, 'fps': 1000/latency if latency > 0 else 0})
                        
                except Exception as e:
                    logging.error(f"Error running {model.metadata()['name']}: {str(e)}")

        with open('predictions.jsonl', 'w') as f:
            for res in self.results:
                f.write(json.dumps(res) + '\\n')
                
        with open('timings.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['model', 'sample', 'latency_ms', 'fps'])
            writer.writeheader()
            writer.writerows(self.timings)
            
        logging.info("Benchmark complete.")
        print("Benchmark validation run completed successfully.")

if __name__ == "__main__":
    runner = BenchmarkRunner()
    runner.run(num_samples=15)
