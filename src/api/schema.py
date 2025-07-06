from pydantic import BaseModel, Field
from typing import List

class AgentResponse(BaseModel):

    messages: str = Field(description="The response message from the agent.")