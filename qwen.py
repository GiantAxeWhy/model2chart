import random
from http import HTTPStatus
import dashscope
from langchain.llms.base import LLM
from abc import ABC
from typing import Any, List, Mapping, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun

class Qwen(LLM, ABC):
    max_token: int = 10000
    temperature: float = 0.01
    top_p = 0.9
    history_len: int = 3

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "Qwen"

    @property
    def _history_len(self) -> int:
        return self.history_len

    def set_history_len(self, history_len: int = 10) -> None:
        self.history_len = history_len

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
    ) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        print('messages',messages)
        response = dashscope.Generation.call(
            'qwen2-7b-instruct',
            messages=messages,
            seed=random.randint(1, 10000),
            result_format='message',
        )
        if response.status_code == HTTPStatus.OK:
            print('response',response)
            return response
        else:

            return 'Request failed with status code {}: {}'.format(
                response.status_code, response.text)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "max_token": self.max_token,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "history_len": self.history_len
        }
