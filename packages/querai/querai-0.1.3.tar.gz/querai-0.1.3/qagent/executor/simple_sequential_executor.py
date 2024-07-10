from typing import Type

from qagent.executor.base_executor import QueryPlanExecutorBase
from qagent.llms import BaseLLM, OpenAILM
from qagent.query import to_query_plan_for_one


class SimpleSingularExecutor(QueryPlanExecutorBase):
    def __init__(
        self,
        prompt: str,
        response_type: str,
        choices: list = None,
        object_constructor: Type = None,
        llm: BaseLLM = None
    ):
        super().__init__(
            plan=to_query_plan_for_one(
                text=prompt,
                response_type=response_type,
                choices=choices,
                object_constructor=object_constructor
            ),
            llm=llm or OpenAILM()
        )
