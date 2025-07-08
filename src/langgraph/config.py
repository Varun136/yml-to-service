import yaml
from src.config.schema import ModelConfig


with open("src/config/langgraph_config.yml", "r") as file:
    langgraph_config = yaml.safe_load(file)

FileSystemAgent = ModelConfig(**langgraph_config.get("file_system_agent"))