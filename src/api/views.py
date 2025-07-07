import yaml
from fastapi import UploadFile, File, Form
from fastapi import APIRouter
from src.langgraph.agent import DeveloperAgent
from src.api.schema import AgentResponse
from fastapi.exceptions import HTTPException
from src.api.validator import YMLValidator

yml_router = APIRouter()
agent = DeveloperAgent()
validator = YMLValidator()

@yml_router.post("/upload-yml")
async def uploadYML(
    file: UploadFile = File(None), 
    yaml_content: str = Form(None)
    ):
    
    if not file and not yaml_content:
        return HTTPException(400, "NO_YAML")
    
    if file:
        contents = await file.read()
    else:
        contents = yaml_content.encode()
    
    try:
        config_data = yaml.safe_load(contents)
    except yaml.YAMLError as e:
        return {"error": f"Invalid YAML format: {str(e)}"}
    
    validated_data = validator.validate(config_data)
    if validated_data.invalid:
        return HTTPException(400, validated_data.error_messages)

    response = await agent.run(validated_data)
    agent_response = AgentResponse(messages=response)

    return {
        "message": "YAML file processed successfully.",
        "ai_response": agent_response,
    }