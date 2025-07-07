from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import List
from langchain_core.messages import SystemMessage, HumanMessage
from src.api.config import ValidatorModel
from dotenv import load_dotenv
import os
load_dotenv(override=True)


class ValidatorModelResponse(BaseModel):
    invalid: bool = Field(description="Check if the yml given does not passes all the check")
    error_messages: List[str] = Field(description="The errors in the given yml seperated by comma.")

class YMLValidator:
    def __init__(self):
        self._model = ChatOpenAI(
            api_key=os.environ.get("API_KEY"),
            base_url=os.environ.get("BASE_URL"),
            model="gpt-4o"
        ).with_structured_output(ValidatorModelResponse)

    def validate(self, yml):
        valuation_prompt = [SystemMessage(ValidatorModel.system_pompt)]

        valuation_prompt.append(HumanMessage(f"""
            Evaluate the following yml:
            {yml}
        """))
        response = self._model.invoke(valuation_prompt)
        return response

