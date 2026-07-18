class BaseRunner:
    def __init__(self, logger):
        self.logger = logger
        
    def run(self, dataset_path):
        """
        Executes the benchmark on the given dataset path.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement run(dataset_path)")
