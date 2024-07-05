from typing import Dict, Any, List, Union, Optional
from uuid import UUID
from logspend_sdk.core import LogBuilder, LogSpendLogger
import time
import logging

try:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage, ToolMessage, FunctionMessage, ChatMessage
    from langchain_core.prompt_values import PromptValue
except ImportError:
    raise ModuleNotFoundError(
        "Please install langchain: 'pip install langchain'"
    )

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class LogSpendLangChainCallbackHandler(BaseCallbackHandler):
    """LangChain callback handler for LogSpend"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        api_url: Optional[str] = "https://api.logspend.com/llm/v1/log",
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        custom_properties: Optional[Dict[str, Any]] = {},
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.logspend = LogSpendLogger(api_key=api_key, project_id=project_id, api_url=api_url, integration_type="langchain")
        self.identity = {
            "session_id": session_id,
        }
        if user_id is not None:
            self.identity["user_id"] = user_id
        if ip_address is not None:
            self.identity["ip_address"] = ip_address
        self.custom_properties = custom_properties
        self.chains = {}

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> Any:
        """Run when chain starts running."""
        
        try:
            if parent_run_id is None:
                # Retrieve properties passed to the chain
                self.custom_properties.update(inputs)
            elif isinstance(inputs, AIMessage):
                # Extract chain output
                output_data = {
                    "output": self._convert_ai_message_to_dict(inputs),
                    "end_time_ms": int(time.time() * 1000),
                }
                if parent_run_id in self.chains:
                    self.chains[parent_run_id].update(output_data)
                else:
                    self.chains[parent_run_id] = output_data
        except Exception as e:
            logger.error(f"Error occured in LogSpend's langChain handler (on_chain_start): {e}")

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
        ) -> Any:
        """Run when chain ends running."""
        
        try:
            if parent_run_id is None:
                # Signals the end of the main chain
                if run_id not in self.chains or not self.chains[run_id].get("output") or not bool(self.chains[run_id].get("output")):
                    # Attempt to extract the output text if no previous step provided it already
                    output_text = None
                    if isinstance(outputs, dict) and "text" in outputs:
                        output_text = outputs["text"]
                    elif isinstance(outputs, str):
                        output_text = outputs

                    if output_text:
                        current_time_ms = int(time.time() * 1000)
                        if run_id in self.chains:
                            self.chains[run_id].update({
                                "output": {
                                    "choices": [{
                                    "index": 0,
                                    "message": {
                                        "role": "assistant",
                                        "content": output_text,
                                    },
                                    "finish_reason": "",
                                    }],
                                    "http_status_code": 200,
                                },
                                "end_time_ms": current_time_ms,
                            })
                        else:
                            self.chains[run_id] = {
                                "output": {
                                    "choices": [{
                                    "index": 0,
                                    "message": {
                                        "role": "assistant",
                                        "content": output_text,
                                    },
                                    "finish_reason": "",
                                    }],
                                    "http_status_code": 200,
                                },
                                "end_time_ms": current_time_ms,
                            }      
                # Log chains
                self._log_chains()
                
            elif isinstance(outputs, PromptValue):
                # Extract prompt messages for current chain
                input_prompts = outputs.to_messages()

                input_data = self._parse_messages(input_prompts)
                current_time_ms = int(time.time() * 1000)

                if parent_run_id in self.chains:
                    self.chains[parent_run_id].update({
                        "prompts": input_data,
                        "start_time_ms": current_time_ms,
                    })
                else:
                    self.chains[parent_run_id] = {
                        "prompts": input_data,
                        "start_time_ms": current_time_ms,
                    }
        except Exception as e:
            logger.error(f"Error occured in LogSpend's langChain handler (on_chain_end): {e}")

    def on_chain_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any
    ) -> Any:
        """Run when chain errors."""
        try:
            # Extract error status code and error message
            status_code = getattr(error, 'status_code', None)
            error_message = str(error)
            error_output = {
                "choices": [],
                "usage": {},
                "http_status_code": status_code,
                "http_error_message": error_message,
            }

            # Update self.chains with the error output
            chain_id = parent_run_id or run_id
            current_time_ms = int(time.time() * 1000)
            if chain_id in self.chains:
                self.chains[chain_id].update({
                    "output": error_output,
                    "end_time_ms": current_time_ms,
                })
            else:
                self.chains[chain_id] = {
                    "output": error_output,
                    "end_time_ms": current_time_ms,
                }
  
            # Log chains if this is the end of the main chain
            if parent_run_id is None:
                self._log_chains()
        except Exception as e:
            logger.error(f"Error occured in LogSpend's langChain handler (on_chain_error): {e}")
        
    def _convert_ai_message_to_dict(self, ai_message: AIMessage) -> Dict[str, Any]:
        return {
            "id": ai_message.id,
            "model_name": ai_message.response_metadata.get("model_name", ""),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": ai_message.content,
                },
                "finish_reason": ai_message.response_metadata.get("finish_reason", ""),
            }],
            "usage": {
                "prompt_tokens": ai_message.response_metadata.get("token_usage", {}).get("prompt_tokens"),
                "completion_tokens": ai_message.response_metadata.get("token_usage", {}).get("completion_tokens"),
                "total_tokens": ai_message.response_metadata.get("token_usage", {}).get("total_tokens"),
            },
            "http_status_code": 200,  # Assuming a successful response
            "http_error_message": "",
        }
        
    def _convert_message_to_dict(self, message: BaseMessage) -> Dict[str, Any]:
        if isinstance(message, HumanMessage):
            message_dict = {"role": "user", "content": message.content}
        elif isinstance(message, AIMessage):
            message_dict = {"role": "assistant", "content": message.content}
        elif isinstance(message, SystemMessage):
            message_dict = {"role": "system", "content": message.content}
        elif isinstance(message, ToolMessage):
            message_dict = {"role": "tool", "content": message.content}
        elif isinstance(message, FunctionMessage):
            message_dict = {"role": "function", "content": message.content}
        elif isinstance(message, ChatMessage):
            message_dict = {"role": message.role, "content": message.content}
        else:
            raise ValueError(f"Got unknown type {message}")

        return message_dict

    def _parse_messages(self, messages: List[BaseMessage]) -> List[Dict[str, Any]]:
        return [self._convert_message_to_dict(m) for m in messages]
    
    def _log_chains(self):
        # Loop through chains and send logs
        for chain_id, chain_data in self.chains.items():
            input_data = {
                "messages": chain_data.get("prompts", []),
            }

            # Extract model name from output if present
            output_data = chain_data.get("output", {})
            if isinstance(output_data, dict):
                model_name = output_data.get("model_name")
                input_data["model"] = model_name
            
            start_time_ms = chain_data.get("start_time_ms")
            end_time_ms = chain_data.get("end_time_ms")

            builder = LogBuilder(input_data)
            builder.set_identity(self.identity)
            builder.set_custom_properties(self.custom_properties)
            # Handles rare error scenarios where we might be missing either of the timestamps
            builder.set_start_time(start_time_ms or end_time_ms)
            builder.set_end_time(end_time_ms or start_time_ms)
            builder.set_output(output_data)

            self.logspend.send(builder.build())