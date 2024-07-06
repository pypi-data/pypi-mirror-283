from logging import raiseExceptions
from tkinter import SE
from uuid import uuid4
import uuid
import therix
from therix.core.pipeline_component import PipelineComponent
from .constants import (
    DataSourceMaster,
    EmbeddingModelMaster,
    PipelineTypeMaster,
)  # Import your constants
from ..services.pipeline_service import PipelineService  # Import your service
from ..entities.models import ConfigType  # Import your ConfigType enum
from ..services.pipeline_service import PipelineService  # Import your service
from langchain.globals import set_llm_cache
from therix.core.response import ModelResponse
from sqlalchemy import create_engine
from therix.core.cache import TherixCache
from therix.db.session import SQLALCHEMY_DATABASE_URL
import os
import json
import warnings

warnings.simplefilter('always', DeprecationWarning)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Pipeline:
    def __init__(self, name, pipeline_ids=None, status="PUBLISHED"):
        if self.__class__.__name__ != 'Agent':
            warning_message = "\033[93mThe 'Pipeline' class is deprecated and will be removed in a future release. Please use the 'Agent' class instead.\033[0m"
            warnings.warn(
                warning_message,
                DeprecationWarning,
                stacklevel=2
            )
        self.pipeline_data = {"name": name, "status": status}
        self.components = []
        self.type = None
        self.pipeline_ids = pipeline_ids
        self.added_configs = set()
        self.therix_api_key = os.getenv("THERIX_API_KEY")
        if self.therix_api_key is None or self.therix_api_key == "":
            print(
                "\033[93m🚨THERIX_API_KEY is not set. You are going to use therix-SDK services without authentication.\033[0m"
            )
            self.pipeline_service = PipelineService()

        else:
            self.pipeline_service = PipelineService(therix_api_key=self.therix_api_key)

    @classmethod
    def from_id(cls, pipeline_id):
        pipeline = cls.__new__(cls)
        pipeline.__init__(None)
        pipeline.load(pipeline_id)
        return pipeline
    
    @classmethod
    def merge(cls, pipeline_ids):
        if not pipeline_ids:
            raise ValueError("No pipeline IDs provided for merging")

        merged_pipeline = cls.__new__(cls)

        merged_pipeline.__init__(None, pipeline_ids)

        for pid in pipeline_ids:
            pipeline = cls.from_id(pid)
            merged_pipeline.components.extend(pipeline.components)

        return merged_pipeline


    def validate_configuration(self, component):
        if not isinstance(component, PipelineComponent):
            raise ValueError("component must be an instance of PipelineComponent")
        config_key = component.type.value
        if config_key in self.added_configs:
            if not config_key == ConfigType.INPUT_SOURCE.value:
                raise ValueError(
                    f"Configuration '{component.type.value}' is added multiple times."
                )
        self.added_configs.add(config_key)

    def set_primary(self, pipeline_id):
        self.pipeline_data = self.pipeline_service.get_pipeline(pipeline_id)
        self.id = self.pipeline_data.id
        self.name = self.pipeline_data.name
        return self.pipeline_data

    def add(self, component):
        if not isinstance(component, PipelineComponent):
            raise ValueError("component must be an instance of PipelineComponent")

        component_type_to_pipeline_type = {
            ConfigType.EMBEDDING_MODEL.value: PipelineTypeMaster.RAG.value,
            ConfigType.SUMMARIZER.value: PipelineTypeMaster.SUMMARIZER.value,
            # Add future component types here
        }

        # Check if the component type is in the dictionary and if the pipeline type is not set
        if (
            component.type.value in component_type_to_pipeline_type
            and self.type is None
        ):
            self.type = component_type_to_pipeline_type[component.type.value]
        elif component.type.value not in component_type_to_pipeline_type:
            pass
        else:
            raise Exception(f"Cannot add {component.type.value}.")

        self.validate_configuration(component)

        self.components.append(component)
        return self  # Enable method chaining

    def add_data_source(self, name, config):
        data_source = PipelineComponent(ConfigType.INPUT_SOURCE, name, config)
        return self.add(data_source)

    def add_embedding_model(self, name, config):
        embedding_model = PipelineComponent(ConfigType.EMBEDDING_MODEL, name, config)
        return self.add(embedding_model)

    def add_inference_model(self, name, config):
        inference_model = PipelineComponent(ConfigType.INFERENCE_MODEL, name, config)
        return self.add(inference_model)

    def add_output_source(self, name, config):
        output_source = PipelineComponent(ConfigType.OUTPUT_SOURCE, name, config)
        return self.add(output_source)

    def save(self):
        configurations_data = [
            {
                "config_type": component.type.value,
                "name": component.name,
                "config": component.config,
            }
            for component in self.components
        ]

        if self.type is None:
            for config in configurations_data:
                if config["config_type"] == ConfigType.INFERENCE_MODEL.value:
                    self.type = PipelineTypeMaster.DEFAULT.value
                    break

        self.pipeline_data["type"] = self.type

        self.pipeline_data = self.pipeline_service.create_pipeline_with_configurations(
            self.pipeline_data, configurations_data
        )

        self.id = self.pipeline_data.id
        self.name = self.pipeline_data.name
        return self.pipeline_data

    def get_db_url(self):
        db_url = self.pipeline_service.get_db_url()
        return db_url

    def get_prompt_by_name(self, prompt_name):
        return self.pipeline_service.get_prompt_by_name(prompt_name)

    def get_trace_api(self):
        trace_api = self.pipeline_service.get_trace_creds()
        return trace_api

    def update_configuration(self, pipeline_id, component):
        if not isinstance(component, PipelineComponent):
            raise ValueError("component must be an instance of PipelineComponent")

        config_data = {
            "config_type": component.type.value,
            "name": component.name,
            "config": component.config,
        }

        return self.pipeline_service.update_pipeine_configuration(
            pipeline_id=pipeline_id, component=config_data
        )

    def publish(self):
        return self.pipeline_service.publish_pipeline(self.pipeline_data)

    def load(self, pipeline_id):
        self.pipeline_data = self.pipeline_service.get_pipeline(pipeline_id)
        self.id = self.pipeline_data.id
        self.name = self.pipeline_data.name
        self.type = self.pipeline_data.type
        return self.pipeline_data

    def preprocess_data(self):
        return self.pipeline_service.preprocess_data(self.pipeline_data.id)

    def get_configurations(self, pipeline_id):
        therix_cache = TherixCache(engine)
        inference_model = self.pipeline_service.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )
        add_cache = self.pipeline_service.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.CACHE_CONFIG
        )
        pipeline_trace_config = (
            self.pipeline_service.get_pipeline_configurations_by_type(
                pipeline_id, ConfigType.TRACE_DETAILS
            )
        )
        saved_system_prompt = self.pipeline_service.get_pipeline_configurations_by_type(
            pipeline_id, ConfigType.SYSTEM_PROMPT
        )
        if(self.therix_api_key):
            pipeline_type = self.pipeline_service.get_pipeline(pipeline_id).type
        else:
            pipeline_type = self.pipeline_service.get_pipeline(pipeline_id).type.value
            
        return (
            therix_cache,
            inference_model,
            add_cache,
            pipeline_trace_config,
            saved_system_prompt,
            pipeline_type,
        )

    def async_invoke(
        self,
        question=None,
        session_id=None,
        keyword_search_params=None,
        dynamic_system_prompt=None,
        output_parser=None,
    ):
        # Check if required parameters are provided
        if question is None and keyword_search_params is None:
            return "Please provide the required parameters to invoke the pipeline"

        # Initialize session_id if not provided
        if session_id is None:
            session_id = str(uuid.uuid4())

        (
            therix_cache,
            inference_model,
            add_cache,
            pipeline_trace_config,
            saved_system_prompt,
            pipeline_type,
        ) = self.get_configurations(self.pipeline_data.id)
        # Determine system prompt to use
        pipeline_system_prompt = (
            {"system_prompt": dynamic_system_prompt}
            if dynamic_system_prompt
            else (saved_system_prompt[0].config if saved_system_prompt else None)
        )
        trace_details = (
            pipeline_trace_config[0].config if pipeline_trace_config else None
        )

        # Handle RAG pipeline type
        if pipeline_type == PipelineTypeMaster.RAG.value:
            if add_cache:
                cached_response = therix_cache.lookup(
                    question, inference_model.name, self.pipeline_data.id
                )
                if cached_response:
                    return ModelResponse(
                        cached_response.response, session_id
                    ).create_response()

            if keyword_search_params and question is None:
                if (
                    isinstance(self.pipeline_ids, list)
                    and len(self.pipeline_ids) > 0
                    and isinstance(self.pipeline_data.id, uuid.UUID)
                ):
                    self.pipeline_ids.append(str(self.pipeline_data.id))
                    keyword_search_params["pipeline_ids"] = self.pipeline_ids
                    # keyword_search_params['pipeline_id'] = self.pipeline_data.id
                    keyword_search_params["trace_details"] = trace_details
                    answer = self.pipeline_service.async_search_keywords(
                        keyword_search_params
                    )

                elif isinstance(self.pipeline_ids, list) and len(self.pipeline_ids) > 0:
                    keyword_search_params["pipeline_ids"] = self.pipeline_ids
                    # keyword_search_params['pipeline_id'] = self.pipeline_data.id
                    keyword_search_params["trace_details"] = trace_details
                    keyword_search_params["trace_api"] = self.get_trace_api() or None
                    answer = self.pipeline_service.async_search_keywords(
                        keyword_search_params
                    )
            else:
                output_parser_arg = (
                    {"output_parser": output_parser}
                    if output_parser is not None
                    else {}
                )

                if (
                    isinstance(self.pipeline_ids, list)
                    and len(self.pipeline_ids) > 0
                    and isinstance(self.pipeline_data.id, uuid.UUID)
                ):
                    self.pipeline_ids.append(str(self.pipeline_data.id))
                    if pipeline_system_prompt:
                        answer = self.pipeline_service.async_invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session_id,
                            trace_details,
                            pipeline_system_prompt,
                            trace_api=self.get_trace_api() or None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                    else:
                        answer = self.pipeline_service.async_invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session_id,
                            trace_details,
                            trace_api=self.get_trace_api() or None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                elif isinstance(self.pipeline_ids, list) and len(self.pipeline_ids) > 0:
                    pipeline_data_id = self.pipeline_ids[-1]
                    if pipeline_system_prompt:
                        answer = self.pipeline_service.async_invoke_pipeline(
                            pipeline_data_id,
                            question,
                            session_id,
                            trace_details,
                            pipeline_system_prompt,
                            trace_api=self.get_trace_api() or None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                    else:
                        answer = self.pipeline_service.async_invoke_pipeline(
                            pipeline_data_id,
                            question,
                            session_id,
                            trace_details,
                            trace_api=self.get_trace_api() or None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                else:
                    if pipeline_system_prompt:
                        answer = self.pipeline_service.async_invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session_id,
                            trace_details,
                            pipeline_system_prompt,
                            trace_api=self.get_trace_api() or None,
                            **output_parser_arg,
                        )
                    else:
                        answer = self.pipeline_service.async_invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session_id,
                            trace_details,
                            **output_parser_arg,
                            trace_api=self.get_trace_api() or None,
                        )

            if add_cache:
                therix_cache.update(
                    question, inference_model.name, answer, self.pipeline_data.id
                )

        # Handle Summarizer pipeline type
        elif pipeline_type == PipelineTypeMaster.SUMMARIZER.value:
            answer = (
                self.pipeline_service.async_invoke_summarizer_pipeline(
                    self.pipeline_data.id,
                    text=question,
                    trace_details=trace_details,
                    system_prompt=pipeline_system_prompt,
                )
                if pipeline_system_prompt
                else self.pipeline_service.async_invoke_summarizer_pipeline(
                    self.pipeline_data.id, text=question, trace_details=trace_details
                )
            )

        # Handle Default pipeline type
        elif pipeline_type == PipelineTypeMaster.DEFAULT.value:
            if pipeline_system_prompt:
                answer = self.pipeline_service.async_invoke_default_pipeline(
                    self.pipeline_data.id,
                    session_id,
                    question=question,
                    trace_details=trace_details,
                    system_prompt=pipeline_system_prompt,
                    trace_api=self.get_trace_api(),
                )
            else:
                answer = self.pipeline_service.async_invoke_default_pipeline(
                    self.pipeline_data.id,
                    session_id,
                    question=question,
                    trace_details=trace_details,
                    trace_api=self.get_trace_api(),
                )

        return ModelResponse(answer, session_id).create_response()

    def invoke(
        self,
        question=None,
        session_id=None,
        keyword_search_params=None,
        dynamic_system_prompt=None,
        output_parser=None,
    ):  
        if isinstance(self.pipeline_data, dict) and 'id' not in self.pipeline_data:
            if(self.pipeline_ids is not None):
                self.set_primary(self.pipeline_ids[-1])
        
        # Check if required parameters are provided
        if question is None and keyword_search_params is None:
            return "Please provide the required parameters to invoke the pipeline"

        # Initialize session_id if not provided
        if session_id is None:
            session = {"session_id": str(uuid.uuid4()), "source": "AUTO-GENERATED"}
        else:
            session = {"session_id": session_id, "source": "USER"}
        (
            therix_cache,
            inference_model,
            add_cache,
            pipeline_trace_config,
            saved_system_prompt,
            pipeline_type,
        ) = self.get_configurations(self.pipeline_data.id)
        
        # Determine system prompt to use
        if(self.therix_api_key):
            pipeline_system_prompt = {"system_prompt": dynamic_system_prompt} if dynamic_system_prompt else (self.pipeline_service.get_prompt_by_name(saved_system_prompt[0].config.get('system_prompt')) if saved_system_prompt else None)
        else:
            pipeline_system_prompt = (
            {"system_prompt": dynamic_system_prompt}
            if dynamic_system_prompt
            else (saved_system_prompt[0].config if saved_system_prompt else None)
        )
        trace_details = (
            pipeline_trace_config[0].config if pipeline_trace_config else None
        )
        
        
        trace_details = (
            pipeline_trace_config[0].config if pipeline_trace_config else None
        )

        # Handle RAG pipeline type
        if pipeline_type == PipelineTypeMaster.RAG.value:
            if add_cache:
                cached_response = therix_cache.lookup(
                    question, inference_model.name, self.pipeline_data.id
                )
                if cached_response:
                    return ModelResponse(
                        cached_response.response, session.get("session_id")
                    ).create_response()

            if keyword_search_params and question is None:
                if (
                    isinstance(self.pipeline_ids, list)
                    and len(self.pipeline_ids) > 0
                ):
                    # self.pipeline_ids.append(str(self.pipeline_data.id))
                    keyword_search_params['active_pipeline_id'] = str(self.pipeline_data.id)
                    keyword_search_params["pipeline_ids"] = self.pipeline_ids
                    keyword_search_params["trace_details"] = trace_details
                    keyword_search_params['session'] = session
                    keyword_search_params["trace_api"] = self.get_trace_api() if self.therix_api_key else None
                    answer = self.pipeline_service.search_keywords(
                        keyword_search_params
                    )
                else:
                    keyword_search_params["pipeline_id"] = self.pipeline_data.id
                    keyword_search_params["trace_details"] = trace_details
                    keyword_search_params['session'] = session
                    keyword_search_params["trace_api"] = self.get_trace_api() if self.therix_api_key else None
                    answer = self.pipeline_service.search_keywords(
                        keyword_search_params
                    )
            else:
                output_parser_arg = (
                    {"output_parser": output_parser}
                    if output_parser is not None
                    else {}
                )

                if (
                    isinstance(self.pipeline_ids, list)
                    and len(self.pipeline_ids) > 0
                    and isinstance(self.pipeline_data.id, uuid.UUID)
                ):
                    self.pipeline_ids.append(str(self.pipeline_data.id))
                    if pipeline_system_prompt:
                        answer = self.pipeline_service.invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session,
                            trace_details,
                            pipeline_system_prompt,
                            db_url= self.get_db_url() if self.therix_api_key else None,
                            trace_api=self.get_trace_api() if self.therix_api_key else None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                    else:
                        answer = self.pipeline_service.invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session,
                            trace_details,
                            db_url= self.get_db_url() if self.therix_api_key else None,
                            trace_api=self.get_trace_api() if self.therix_api_key else None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                elif isinstance(self.pipeline_ids, list) and len(self.pipeline_ids) > 0:
                    pipeline_data_id = self.pipeline_ids[-1]
                    if pipeline_system_prompt:
                        answer = self.pipeline_service.invoke_pipeline(
                            pipeline_data_id,
                            question,
                            session,
                            trace_details,
                            pipeline_system_prompt,
                            db_url= self.get_db_url() if self.therix_api_key else None,
                            trace_api=self.get_trace_api() if self.therix_api_key else None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                    else:
                        answer = self.pipeline_service.invoke_pipeline(
                            pipeline_data_id,
                            question,
                            session,
                            trace_details,
                            db_url= self.get_db_url() if self.therix_api_key else None,
                            trace_api=self.get_trace_api() if self.therix_api_key else None,
                            pipeline_ids=self.pipeline_ids,
                            **output_parser_arg,
                        )
                else:
                    if pipeline_system_prompt:
                        answer = self.pipeline_service.invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session,
                            trace_details,
                            pipeline_system_prompt,
                            db_url= self.get_db_url() if self.therix_api_key else None,
                            trace_api=self.get_trace_api() if self.therix_api_key else None,
                            **output_parser_arg,
                        )
                    else:
                        answer = self.pipeline_service.invoke_pipeline(
                            self.pipeline_data.id,
                            question,
                            session,
                            trace_details,
                            **output_parser_arg,
                            db_url= self.get_db_url() if self.therix_api_key else None,
                            trace_api=self.get_trace_api() if self.therix_api_key else None,
                        )

            if add_cache:
                therix_cache.update(
                    question, inference_model.name, answer, self.pipeline_data.id
                )

        # Handle Summarizer pipeline type
        elif pipeline_type == PipelineTypeMaster.SUMMARIZER.value:
            answer = (
                self.pipeline_service.invoke_summarizer_pipeline(
                    pipeline_id=self.pipeline_data.id,
                    text=question,
                    trace_details=trace_details,
                    trace_api=self.get_trace_api() if self.therix_api_key else None,
                    system_prompt=pipeline_system_prompt,
                    session = session
                )
                if pipeline_system_prompt
                else self.pipeline_service.invoke_summarizer_pipeline(
                    self.pipeline_data.id, text=question, trace_details=trace_details, session=session, trace_api=self.get_trace_api() if self.therix_api_key else None
                )
            )

        # Handle Default pipeline type
        elif pipeline_type == PipelineTypeMaster.DEFAULT.value:
            if pipeline_system_prompt:
                answer = self.pipeline_service.invoke_default_pipeline(
                    self.pipeline_data.id,
                    session,
                    question=question,
                    trace_details=trace_details,
                    system_prompt=pipeline_system_prompt,
                    trace_api=self.get_trace_api() if self.therix_api_key else None,
                    db_url=self.get_db_url() if self.therix_api_key else None,
                )
            else:
                answer = self.pipeline_service.invoke_default_pipeline(
                    self.pipeline_data.id,
                    session,
                    question=question,
                    trace_details=trace_details,
                    trace_api=self.get_trace_api() if self.therix_api_key else None ,
                    db_url=self.get_db_url() if self.therix_api_key else None,
                )

        return ModelResponse(answer, session.get("session_id")).create_response()
