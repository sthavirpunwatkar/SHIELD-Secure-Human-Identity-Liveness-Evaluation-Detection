import os
import cv2
import numpy as np
from data.data_wrangler import DataWrangler
from evaluation.benchmark import BenchmarkEngine
from evaluation.report_generator import ReportGenerator

def main():
    print("--- SHIELD End-to-End Roadmap Demo (Sprints 4 & 5) ---")
    
    # 1. Create a mock raw dataset for demonstration
    raw_dir = "data/raw_mock"
    os.makedirs(f"{raw_dir}/live", exist_ok=True)
    os.makedirs(f"{raw_dir}/spoof", exist_ok=True)
    
    def create_dummy_img(path, text, color=(255, 255, 255)):
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(img, text, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
        # Add some noise for quality gate pass
        noise = np.random.normal(0, 10, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
        cv2.imwrite(path, img)

    print("Step 1: Creating Mock Raw Data...")
    for i in range(5):
        create_dummy_img(f"{raw_dir}/live/subject_{i}.jpg", "LIVE", (0, 255, 0))
        create_dummy_img(f"{raw_dir}/spoof/attack_{i}.jpg", "SPOOF", (0, 0, 255))
    
    # 2. Sprint 4: Data Wrangling
    print("\nStep 2: Sprint 4 - Data Wrangling...")
    wrangler = DataWrangler(output_base="data/processed_demo")
    wrangler.process_dataset(raw_dir, "mock_dataset", {"live": "live", "spoof": "spoof"}, is_video=False, strict=False)
    wrangler.save_manifest()
    
    # 3. Sprint 5: Evaluation
    print("\nStep 3: Sprint 5 - Benchmarking...")
    bench = BenchmarkEngine(manifest_path="data/processed_demo/manifest.json")
    stats, results = bench.run_benchmark()
    
    if stats:
        print(f"Benchmark Results: Accuracy {stats['accuracy']*100:.1f}%, ACER {stats['acer']*100:.1f}%")
        
        # 4. Reporting
        print("\nStep 4: Generating Report...")
        ReportGenerator.generate(stats, output_path="reports/demo_benchmark_report.md")
    
    print("\n--- Roadmap Demo Complete ---")

if __name__ == "__main__":
    main()
