from logging import config
import trace
from therix.core import pipeline
from therix.utils.summarizer import summarizer, async_summarizer
from ..db.session import SessionLocal
from ..entities.models import ConfigType, Pipeline, PipelineConfiguration
import json
import os
import urllib
from therix.services.web_crawling import crawl_website
from therix.utils.pii_filter import pii_filter
from ..db.session import SessionLocal
from therix.utils.rag import (
    chat,
    create_embeddings,
    get_embedding_model,
    get_vectorstore,
    get_loader,
    async_chat,
)
from langchain_openai import AzureOpenAIEmbeddings
from therix.utils.keyword_search import async_keyword_search, keyword_search
from therix.services.api_service import ApiService
from types import SimpleNamespace
from therix.utils.default_chat import async_invoke_default_chat, invoke_default_chat
from langchain.retrievers.merger_retriever import MergerRetriever


class PipelineService:
    def __init__(self, therix_api_key=None):
        self.db_session = SessionLocal()
        self.therix_api_key = therix_api_key
        if(self.therix_api_key is not None):
            self.api_service = ApiService(therix_api_key)

    def create_pipeline_with_configurations(self, pipeline_data, configurations_data):

        if self.therix_api_key is not None:
            for config_data in configurations_data:
                if config_data["config_type"] == "INFERENCE_MODEL":
                    config = config_data.get("config", {})
                    if "temperature" not in config:
                        config["temperature"] = 0.5
                    config_data["config"] = config

            payload = {
                "name": pipeline_data.get("name", None),
                "status": pipeline_data.get("status", None),
                "type": pipeline_data.get("type", None),
                "agent_configurations": configurations_data
            }            

            response_data = self.api_service.post("agent/", payload)
            return DictToObject(response_data['data'])
        else:
            new_pipeline = Pipeline(**pipeline_data)
            self.db_session.add(new_pipeline)
            self.db_session.flush()  # Flush to assign an ID to the new_pipeline

            for config_data in configurations_data:
                config_data["pipeline_id"] = new_pipeline.id
                new_config = PipelineConfiguration(**config_data)
                if new_config.config_type == "INFERENCE_MODEL":
                    if "temperature" not in new_config.config:
                        new_config.config["temperature"] = 0.5
                self.db_session.add(new_config)

            self.db_session.commit()
            return new_pipeline


    def update_pipeine_configuration(self, pipeline_id, component):

        agent_configuration_id= self.get_pipeline_configurations_by_type(pipeline_id, component['config_type'])
        self.api_service.patch( f"agent-config/{agent_configuration_id[0].id}", component)


    def get_db_url(self):
        database_url = self.api_service.get(f"agent/db-url")  
        return database_url['data']
    

    def get_trace_creds(self):
        trace_creds = self.api_service.get(f"trace-keys")
        return trace_creds['data']
    

    def get_prompt_by_name(self, prompt_name):
        response_data = self.api_service.get(endpoint=f"prompts/active",params={"prompt_name": prompt_name})
        return {"system_prompt":response_data['data']['prompt']}



    def publish_pipeline(self, pipeline_data):
        pipeline = self.db_session.query(Pipeline).filter_by(id = pipeline_data.get("id")).first()
        pipeline.status = "PUBLISHED"
        self.db_session.commit()
        return pipeline

    def get_pipeline(self, pipeline_id):

        if self.therix_api_key is not None:
            response_data = self.api_service.get(f"agent/{pipeline_id}")
            return DictToObject(response_data['data'])
        else:
            return self.db_session.query(Pipeline).filter_by(id=pipeline_id).first()

    def get_pipeline_configuration(self, pipeline_id):

        if self.therix_api_key is not None:
            response_data = self.api_service.get(f"agent/{pipeline_id}")
            return DictToObject(response_data['data'])
        else:
            return (
            self.db_session.query(PipelineConfiguration)
            .filter_by(pipeline_id=pipeline_id)
            .all()
        )

    def get_pipeline_configurations_by_type(self, pipeline_id, config_type):



        if self.therix_api_key is not None:
            params = {"agent_id": pipeline_id, "config_type": config_type if isinstance(config_type, str) else config_type.value}
            response_data = self.api_service.get("agent-config/", params=params)

            data = response_data.get('data', [])
            if not data:
                return None

            first_index_data = data[0]
            if isinstance(first_index_data, list) and first_index_data:
                return [DictToObject(item) for item in first_index_data]
            else:
                return None
        else:
            ("ELSE Mein aa raha hai")
            return (
            self.db_session.query(PipelineConfiguration)
            .filter_by(pipeline_id=pipeline_id, config_type=config_type)
            .all()
        )
    

    def preprocess_data(self, pipeline_id):
        data_sources = self.get_pipeline_configurations_by_type(
            pipeline_id, "INPUT_SOURCE"
        )
        output_file = None
        if  hasattr(data_sources[0].config, "website"):
            website_url = data_sources[0].config["website"]
            web_content = crawl_website(website_url)
            domain_name = urllib.parse.urlparse(website_url).netloc
            output_file = f"{domain_name}_data.json"
            with open(output_file, "w") as f:
                json.dump(web_content, f, indent=4)
            data_sources.config["files"] = [output_file]
        if "website" in data_sources[0].config:
            os.remove(output_file)
        embedding_model = self.get_pipeline_configurations_by_type(
            pipeline_id, "EMBEDDING_MODEL"
        )
        if self.therix_api_key is not None:
            return create_embeddings(data_sources, embedding_model[0], str(pipeline_id), self.get_db_url())
        else:
            return create_embeddings(data_sources, embedding_model[0], str(pipeline_id))


    async def async_invoke_pipeline(
            self, 
            pipeline_id, 
            question, 
            session, 
            trace_details=None, 
            system_prompt=None, 
            db_url=None, 
            trace_api=None, 
            pipeline_ids = None,
            output_parser=None
        ):
        embedding_model = self.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.EMBEDDING_MODEL
        )

        if(pipeline_ids):
            combined_retrievers = []
            for individual_pipeline_id in pipeline_ids:
                embedding_model = self.get_pipeline_configurations_by_type(
                    individual_pipeline_id, "EMBEDDING_MODEL"
                )
                store = get_vectorstore(embedding_model[0], str(individual_pipeline_id), self.get_db_url())
                combined_retrievers.append(store.as_retriever())
            retriever = MergerRetriever(retrievers=combined_retrievers)

        else:
            store = get_vectorstore(embedding_model[0], str(pipeline_id), self.get_db_url())
            retriever = store.as_retriever()
            
        inference_model = self.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )

        pii_filter_config = self.get_pipeline_configurations_by_type(pipeline_id, ConfigType.PII_FILTER)
        if pii_filter_config is not None and len(pii_filter_config) != 0:
            pii_filter_config = pii_filter_config[0]
        else:
            pii_filter_config = None

        result = await async_chat(
            question,
            retriever,
            inference_model[0],
            embedding_model,
            session,
            pipeline_id,
            trace_api=trace_api,
            trace_details=trace_details,
            pii_filter_config=pii_filter_config,
            system_prompt=system_prompt,
            output_parser=output_parser,
            db_url=db_url
        )

        if pii_filter_config:
            pii_filter_config = pii_filter_config.config
            entities = pii_filter_config['entities']
            return pii_filter(result, entities)
        else:
            return result

    def invoke_pipeline(
        self, 
        pipeline_id, 
        question, 
        session, 
        trace_details=None, 
        system_prompt=None, 
        db_url=None, 
        trace_api=None, 
        pipeline_ids = None, 
        output_parser = None):
        
        embedding_model = self.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.EMBEDDING_MODEL
        )
        if(pipeline_ids):
            combined_retrievers = []
            for individual_pipeline_id in pipeline_ids:
                embedding_model = self.get_pipeline_configurations_by_type(
                    individual_pipeline_id, "EMBEDDING_MODEL"
                )
                if self.therix_api_key is not None:
                    store = get_vectorstore(embedding_model[0], str(individual_pipeline_id), self.get_db_url())
                else:
                    store = get_vectorstore(embedding_model[0], str(individual_pipeline_id))    
                combined_retrievers.append(store.as_retriever())
            retriever = MergerRetriever(retrievers=combined_retrievers)

        else:
            if self.therix_api_key is not None:
                store = get_vectorstore(embedding_model[0], str(pipeline_id), self.get_db_url())
            else:
                 store = get_vectorstore(embedding_model[0], str(pipeline_id))   
            retriever = store.as_retriever()
            
        inference_model = self.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )

        pii_filter_config = self.get_pipeline_configurations_by_type(pipeline_id, ConfigType.PII_FILTER)
        if pii_filter_config is not None and len(pii_filter_config) != 0:
            pii_filter_config = pii_filter_config[0]
        else:
            pii_filter_config = None

        result = chat(
            question,
            retriever,
            inference_model[0],
            embedding_model,
            session,
            pipeline_id,
            trace_api=trace_api,
            trace_details=trace_details,
            pii_filter_config=pii_filter_config,
            system_prompt=system_prompt,
            db_url=db_url,
            output_parser=output_parser
        )

        if pii_filter_config:
            pii_filter_config = pii_filter_config.config
            entities = pii_filter_config['entities']
            return pii_filter(result, entities)
        else:
            return result
    
    async def async_invoke_summarizer_pipeline(
            self, 
            pipeline_id, 
            text, 
            session,
            trace_details = None, 
            trace_api=None,
            system_prompt=None
        ):
        inference_model = self.get_pipeline_configurations_by_type(pipeline_id, ConfigType.INFERENCE_MODEL)
        summarizer_config = self.get_pipeline_configurations_by_type(pipeline_id, ConfigType.SUMMARIZER)[0].config
        return await async_summarizer(summarizer_config,inference_model[0],text, trace_details, system_prompt,trace_api=trace_api,session_id=session.get('session_id'))

    def invoke_summarizer_pipeline(
            self, 
            pipeline_id, 
            text, 
            session,
            trace_details = None,
            trace_api=None, 
            system_prompt=None):
    
        inference_model = self.get_pipeline_configurations_by_type(pipeline_id, ConfigType.INFERENCE_MODEL)
        summarizer_config = self.get_pipeline_configurations_by_type(pipeline_id, ConfigType.SUMMARIZER)[0].config
        return summarizer(summarizer_config,inference_model[0],text, trace_details, pipeline_id, system_prompt,trace_api=trace_api,session_id=session.get('session_id'))
    
    
    def async_invoke_default_pipeline(
            self, 
            pipeline_id, 
            session, 
            question, 
            trace_details=None, 
            system_prompt=None, 

            trace_api=None):
        inference_model = self.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )
        return async_invoke_default_chat(inference_model_details=inference_model[0], session=session, pipeline_id=pipeline_id, question=question, trace_details=trace_details, system_prompt=system_prompt, trace_api = trace_api, db_url = self.get_db_url() if self.therix_api_key else None)
    
    
    def invoke_default_pipeline(self, pipeline_id, session,question, trace_details=None, system_prompt=None, trace_api = None, db_url = None):
        inference_model = self.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )
        return invoke_default_chat(inference_model_details=inference_model[0], session=session, pipeline_id=pipeline_id, question=question, trace_details=trace_details, system_prompt=system_prompt, trace_api = trace_api, db_url = self.get_db_url() if self.therix_api_key else None)
    

    async def async_search_keywords(self, keyword_search_params):
        if (
            not keyword_search_params.get("prompt")
            or not keyword_search_params.get("keywords")
            or not keyword_search_params.get("output_parser")
        ):
            return "Request is missing required parameters, please provide all the parameters, i.e. pipeline_id, config_id, prompt, keywords, output_parser"

        if "pipeline_ids" in keyword_search_params and len(
            keyword_search_params.get("pipeline_ids")
        ):
            combined_retrievers = []
            inference_model = self.get_pipeline_configurations_by_type(
                keyword_search_params.get("pipeline_ids")[
                    len(keyword_search_params.get("pipeline_ids")) - 1
                ],
                ConfigType.INFERENCE_MODEL,
            )
            for pipeline_id in keyword_search_params.get("pipeline_ids"):
                embedding_model = self.get_pipeline_configurations_by_type(
                    pipeline_id, ConfigType.EMBEDDING_MODEL
                )
                if self.therix_api_key is not None:
                    store = get_vectorstore(embedding_model[0], str(pipeline_id), self.get_db_url())
                else:
                    store = get_vectorstore(embedding_model[0], str(pipeline_id))   
                combined_retrievers.append(store.as_retriever())
            retriever = MergerRetriever(retrievers=combined_retrievers)
        else:
            inference_model = self.get_pipeline_configurations_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.INFERENCE_MODEL
            )
            embedding_model = self.get_pipeline_configurations_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.EMBEDDING_MODEL
            )
            if self.therix_api_key is not None:
                store = get_vectorstore(
                    embedding_model[0], str(keyword_search_params.get("pipeline_id")), self.get_db_url()
                )
            else:
                store = get_vectorstore(
                embedding_model[0], str(keyword_search_params.get("pipeline_id")))
            retriever = store.as_retriever()

        keyword_search_dict = {
            "retriever": retriever,
            "keywords": keyword_search_params.get("keywords"),
            "output_parser": keyword_search_params.get("output_parser"),
            "prompt": keyword_search_params.get("prompt"),
            "trace_details": keyword_search_params.get("trace_details"),
            "trace_api_key": keyword_search_params.get("trace_api"),
            "inference_model": inference_model[0],
        }
        return await async_keyword_search(keyword_search_dict)

    def search_keywords(self, keyword_search_params):
        if (
            not keyword_search_params.get("prompt")
            or not keyword_search_params.get("keywords")
            or not keyword_search_params.get("output_parser")
        ):
            return "Request is missing required parameters, please provide all the parameters, i.e. pipeline_id, prompt, keywords, output_parser"
        
        if "pipeline_ids" in keyword_search_params and len(
            keyword_search_params.get("pipeline_ids")):
            combined_retrievers = []
            inference_model = self.get_pipeline_configurations_by_type(
                keyword_search_params.get("active_pipeline_id"),
                ConfigType.INFERENCE_MODEL,
            )
            for pipeline_id in keyword_search_params.get("pipeline_ids"):
                embedding_model = self.get_pipeline_configurations_by_type(
                    pipeline_id, ConfigType.EMBEDDING_MODEL
                )
                if self.therix_api_key is not None:
                    store = get_vectorstore(embedding_model[0], str(pipeline_id), self.get_db_url())
                else:
                    store = get_vectorstore(embedding_model[0], str(pipeline_id))   
                combined_retrievers.append(store.as_retriever())
            retriever = MergerRetriever(retrievers=combined_retrievers)   
            
        else:
            inference_model = self.get_pipeline_configurations_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.INFERENCE_MODEL
            )
            embedding_model = self.get_pipeline_configurations_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.EMBEDDING_MODEL
            )
            if self.therix_api_key is not None:
                store = get_vectorstore(
                    embedding_model[0], str(keyword_search_params.get("pipeline_id")), self.get_db_url()
                )
            else:
                 store = get_vectorstore(
                embedding_model[0], str(keyword_search_params.get("pipeline_id"))
                )   
            retriever = store.as_retriever()
            
        if("active_pipeline_id" in keyword_search_params):
            active_pipeline_id = keyword_search_params.get("active_pipeline_id")
        elif("pipeline_ids" in keyword_search_params and "active_pipeline_id" not in keyword_search_params):
            active_pipeline_id = keyword_search_params.get("pipeline_ids")[-1]
        else:
            active_pipeline_id = keyword_search_params.get("pipeline_id")

        keyword_search_dict = {
            "retriever": retriever,
            "pipeline_id": active_pipeline_id,
            "keywords": keyword_search_params.get("keywords"),
            "output_parser": keyword_search_params.get("output_parser"),
            "prompt": keyword_search_params.get("prompt"),
            "trace_details": keyword_search_params.get("trace_details"),
            "trace_api": keyword_search_params.get("trace_api"),
            "inference_model": inference_model[0],
            "session" : keyword_search_params.get("session"),
        }
        
        return keyword_search(keyword_search_dict)


    def __del__(self):
        self.db_session.close()



class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)