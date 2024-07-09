import os 
from therix.services import api_service
from therix.services.api_service import ApiService


class Prompt:
    @classmethod
    def get_prompt(cls,prompt_name):
        api_service = ApiService(therix_api_key=os.getenv("THERIX_API_KEY"))
        if os.getenv("THERIX_API_KEY") is not None:
            response_data = api_service.get(endpoint=f"prompts/active",params={"prompt_name": prompt_name})
            return response_data['data']['prompt']
        else:
            raise EnvironmentError("THERIX_API_KEY is not set")