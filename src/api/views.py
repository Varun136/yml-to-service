import yaml
from fastapi import UploadFile, File
from fastapi import APIRouter
from src.langgraph.agent import DeveloperAgent
from src.api.schema import AgentResponse

yml_router = APIRouter()
agent = DeveloperAgent()

@yml_router.post("/upload-yml")
async def uploadYML(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        config_data = yaml.safe_load(contents)
    except yaml.YAMLError as e:
        return {"error": f"Invalid YAML format: {str(e)}"}

    # Example: print out some fields
    project_title = config_data.get("project", {}).get("title")
    service_type = config_data.get("project", {}).get("service")

    response = await agent.run(f"Project Title: {project_title}, Service Type: {service_type}")
    agent_response = AgentResponse(messages=response)

    return {
        "message": "YAML file processed successfully.",
        "ai_response": agent_response,
    }