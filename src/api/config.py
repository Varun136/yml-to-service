import yaml
from src.config.schema import ModelConfig

with open("src/config/api_config.yml", "r") as file:
    api_config = yaml.safe_load(file)


ValidatorModel = ModelConfig(**api_config.get("yml_validator"))