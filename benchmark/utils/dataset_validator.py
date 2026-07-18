import os
import yaml

class DatasetValidator:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['dataset']
        self.dataset_path = self.config['path']

    def validate_siw_structure(self):
        """
        Validates that the SiW dataset is present and strictly adheres to the protocol structure.
        """
        if not os.path.exists(self.dataset_path):
            return False, f"Directory not found: {self.dataset_path}"
            
        required_protocols = ["Protocol_1", "Protocol_2", "Protocol_3"]
        for p in required_protocols:
            p_path = os.path.join(self.dataset_path, p)
            if not os.path.exists(p_path):
                return False, f"Missing required protocol directory: {p_path}"
                
            for split in ["train", "test"]:
                s_path = os.path.join(p_path, split)
                if not os.path.exists(s_path):
                    return False, f"Missing split directory: {s_path}"
                    
        return True, "SiW dataset structure validated."
