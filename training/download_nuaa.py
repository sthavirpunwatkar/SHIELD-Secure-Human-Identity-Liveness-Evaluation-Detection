import os
import argparse

def download_nuaa(data_dir="data/NUAA"):
    """
    Helper script to download NUAA dataset.
    """
    print("--- NUAA Dataset Setup ---")
    if os.path.exists(data_dir) and len(os.listdir(data_dir)) > 0:
        print(f"Dataset directory {data_dir} already exists and is not empty.")
        return

    print("Please download the NUAA dataset from Kaggle:")
    print("https://www.kaggle.com/datasets/yjxiong/nuaa-imposter-dataset")
    print("\nOr use the Kaggle CLI:")
    print(f"  kaggle datasets download -d yjxiong/nuaa-imposter-dataset -p {data_dir}")
    print(f"  unzip {data_dir}/*.zip -d {data_dir}")
    print("\nThen organize the folders as:")
    print(f"  {data_dir}/train/real/")
    print(f"  {data_dir}/train/spoof/")
    print(f"  {data_dir}/test/real/")
    print(f"  {data_dir}/test/spoof/")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download NUAA dataset")
    parser.add_argument("--data-dir", type=str, default="data/NUAA")
    args = parser.parse_args()
    download_nuaa(args.data_dir)
