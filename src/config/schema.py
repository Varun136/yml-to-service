class ModelConfig:
    def __init__(self, system_prompt, model):
        self._system_prompt = system_prompt
        self._model = model
    
    @property
    def system_pompt(self):
        return self._system_prompt
    
    @property
    def model(self):
        return self._model