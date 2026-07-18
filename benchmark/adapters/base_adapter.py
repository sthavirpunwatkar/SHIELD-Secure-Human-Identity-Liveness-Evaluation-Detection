import abc

class BenchmarkModel(abc.ABC):
    @abc.abstractmethod
    def load_model(self):
        pass

    @abc.abstractmethod
    def preprocess(self, input_data):
        pass

    @abc.abstractmethod
    def infer(self, tensor):
        pass

    @abc.abstractmethod
    def postprocess(self, output):
        pass

    @abc.abstractmethod
    def metadata(self):
        pass
