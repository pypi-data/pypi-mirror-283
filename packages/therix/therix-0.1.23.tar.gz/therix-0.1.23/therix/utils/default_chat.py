from enum import Enum
import json
from therix.core.chat_history.base_chat_history import TherixChatMessageHistory
from therix.core.constants import InferenceModelMaster
from therix.db.session import SQLALCHEMY_DATABASE_URL
from therix.utils.rag import get_inference_model
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langfuse.callback import CallbackHandler
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages.chat import ChatMessage


async def async_invoke_default_chat(inference_model_details, session, pipeline_id, question, trace_details=None, system_prompt=None, trace_api = None):
    chain_callbacks = []
    session_id = session.get('session_id')
    if trace_details is not None:
            langfuse_handler = CallbackHandler(
                secret_key=trace_details['secret_key'],
                public_key=trace_details['public_key'],
                host=trace_details["host"],
                trace_name=pipeline_id,
                session_id=session_id
            )
    else :
        if trace_api is not None:
            langfuse_handler = CallbackHandler(
                secret_key=trace_api['secret_key'],
                public_key=trace_api['public_key'],
                host=trace_api["host"],
                trace_name=pipeline_id,
                session_id=session_id
            )  
        else:      
            langfuse_handler= None
    chain_callbacks.append(langfuse_handler)       
    history = TherixChatMessageHistory(
    str(session_id),
    str(pipeline_id),
    SQLALCHEMY_DATABASE_URL,
    table_name="chat_history",
    )
    message_history = history.get_message_history(str(session_id))
    chat_history=[]
    for message in message_history:
        chat_history.append(
            ChatMessage(role=message["message_role"], content=message["message"])
        )
    
    inference_model_name = inference_model_details.name
    inference_model_config = inference_model_details.config
    model = get_inference_model(inference_model_name, inference_model_config)

    if system_prompt is not None:
        system_prompt = system_prompt['system_prompt']
    else:
        system_prompt = "You are a helpful chatbot, you can use your own brain to provide answer to questions by users. The question is: {question}"

    ANSWER_PROMPT = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human",
                 "{question}")
            ]
        )

    chain = ANSWER_PROMPT | model 

    if(trace_details is not None or trace_api is not None):
        result = chain.invoke({"question": question, "chat_history": chat_history},config={"callbacks": [langfuse_handler]})
    
    else:
        result = chain.invoke({"question": question, "chat_history": chat_history})
        

    if inference_model_details.name == InferenceModelMaster.BEDROCK_TEXT_EXPRES_V1 or inference_model_details.name == InferenceModelMaster.BEDROCK_TEXT_LITE_G1 : 
        response = f'{result}'
    else :
        response = json.loads(result.json())["content"]
    
    history.add_message("user",question,pipeline_id,session_id)
    history.add_message("system",response,pipeline_id,session_id)
    return response


def invoke_default_chat(inference_model_details, session, pipeline_id, question, trace_details=None, system_prompt=None, trace_api = None, db_url = None):
    chain_callbacks = []
    session_id = session.get('session_id')
    if trace_details is not None:
            therix_trace_handler = CallbackHandler(
                secret_key=trace_details['secret_key'],
                public_key=trace_details['public_key'],
                host=trace_details["host"],
                trace_name=str(pipeline_id),
                session_id=str(session_id)
            )
    else :
        if trace_api is not None:
            therix_trace_handler = CallbackHandler(
                secret_key=trace_api['secret_key'],
                public_key=trace_api['public_key'],
                host="https://analytics.dev.therix.ai",
                trace_name=pipeline_id,
                session_id=session_id
            )  
        else:      
            therix_trace_handler= None
    chain_callbacks.append(therix_trace_handler)       
    history = TherixChatMessageHistory(
    str(session_id),
    str(pipeline_id),
    db_url or SQLALCHEMY_DATABASE_URL,
    table_name="chat_history",
    )
    message_history = history.get_message_history(str(session_id))
    chat_history=[]
    for message in message_history:
        chat_history.append(
            ChatMessage(role=message["message_role"], content=message["message"])
        )
    
    inference_model_name = inference_model_details.name
    inference_model_config = inference_model_details.config
    model = get_inference_model(inference_model_name, inference_model_config)

    if system_prompt is not None:
        system_prompt = system_prompt['system_prompt']
    else:
        system_prompt = "You are a helpful chatbot, you can use your own brain to provide answer to questions by users. The question is: {question}"

    ANSWER_PROMPT = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human",
                 "{question}")
            ]
        )

    chain = ANSWER_PROMPT | model 

    if(trace_details is not None or trace_api is not None):
        result = chain.invoke({"question": question, "chat_history": chat_history},config={"callbacks": [therix_trace_handler]})
    
    else:
        result = chain.invoke({"question": question, "chat_history": chat_history})
        

    if inference_model_details.name == InferenceModelMaster.BEDROCK_TEXT_EXPRES_V1 or inference_model_details.name == InferenceModelMaster.BEDROCK_TEXT_LITE_G1 : 
        response = f'{result}'
    else :
        response = json.loads(result.json())["content"]
    
    history.add_message("user",question,pipeline_id,session_id)
    history.add_message("system",response,pipeline_id,session_id)
    return response