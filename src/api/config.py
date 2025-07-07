import yaml
from pydantic import BaseModel

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

with open("src/config/api_config.yml", "r") as file:
    api_config = yaml.safe_load(file)


ValidatorModel = ModelConfig(**api_config.get("yml_validator"))