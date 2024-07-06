from typing import List
from pydantic import BaseModel, Field
from therix.core.data_sources import PDFDataSource
from therix.core.embedding_models import (
    BedrockTitanEmbedding,
    OpenAITextAdaEmbeddingModel,
)
from therix.core.inference_models import (
    Anthropic_Claude_Opus,
    OpenAIGPT4TurboPreviewInferenceModel,
    OpenAIGPT4OInferenceModel
)
from therix.core.inference_models import (
    OpenAIGPT4TurboPreviewInferenceModel,GroqLlama370b
)
from therix.core.embedding_models import (
    OpenAITextAdaEmbeddingModel,
)
from therix.core.inference_models import (
    BedrockLiteG1
)
from therix.core.output_parser import OutputParserWrapper
from therix.core.agent import Agent
import sys

from therix.core.system_prompt_config import SystemPromptConfig
from therix.core.trace import Trace

GROQ_API_KEY=''

# sys_prompt = """Answer the question based only on the following context and reply with your capabilities if something is out of context.
#         Context: 
#         {context}

#         Question: {question}
#         """



agent = Agent(name="Robin Agent")
(
        agent.add(PDFDataSource(config={"files": ["../../test-data/rat.pdf"]}))
        .add(BedrockTitanEmbedding(config={"bedrock_aws_access_key_id" : "",
                                "bedrock_aws_secret_access_key" : "",
                                "bedrock_aws_session_token" : "",
                                "bedrock_region_name" : "us-east-1"}))
        .add(GroqLlama370b(config={"groq_api_key": GROQ_API_KEY}))
        .save()
    )

agent.preprocess_data()
print(agent.id)
ans = agent.invoke("What is ablation study")
print(ans)