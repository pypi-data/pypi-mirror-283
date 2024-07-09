
from therix.core.data_sources import PDFDataSource
from therix.core.embedding_models import BedrockTitanEmbedding

from therix.core.output_parser import OutputParserWrapper
from therix.core.agent import Agent

from therix.core.system_prompt_config import SystemPromptConfig
from therix.core.agent import Agent
from therix.core.data_sources import PDFDataSource
from therix.core.embedding_models import BedrockTitanEmbedding
from therix.core.inference_models import GroqMixtral87bInferenceModel


GROQ_API_KEY=''

sys_prompt = """Answer the question based only on the following context and reply with your capabilities if something is out of context.
        Context: 
        {context}

        Question: {question}
        """



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
answer = agent.invoke("What kind of experiments are performed in the study?")

print(answer)