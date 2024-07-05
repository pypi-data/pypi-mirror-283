# type: ignore

import json
from typing import Union, Optional, Awaitable

try:
    from langchain.prompts import StringPromptTemplate
except ImportError as err:
    raise ImportError("langchain is not installed") from err

from .. import Airprompt, AsyncAirprompt
from .._types import NOT_GIVEN, Literal


class AirpromptTemplate(StringPromptTemplate):
    prompt_id: str
    client: Optional[Airprompt]
    asyncClient: Optional[AsyncAirprompt]
    environment: Optional[str]
    version: Optional[Union[int, Literal["latest"]]]
    json_input_variables: Optional[bool]

    def __init_subclass__(
        cls,
        prompt_id: str,
        client: Optional[Airprompt],
        asyncClient: Optional[AsyncAirprompt],
        environment: Optional[str],
        version: Optional[Union[int, Literal["latest"]]],
        json_input_variables: Optional[bool],
        **kwargs,
    ):
        if not client and not asyncClient:
            raise ValueError("Either client or asyncClient must be provided")
        cls.client = client
        cls.asyncClient = asyncClient

        cls.prompt_id = prompt_id
        cls.environment = environment
        cls.version = version
        cls.json_input_variables = json_input_variables

        super().__init_subclass__(**kwargs)

    def __init__(self, **kwargs):
        json_input_variables = kwargs.get("json_input_variables")

        input_variables = kwargs.pop("input_variables", None)
        if json_input_variables:
            input_variables = ["vars"]

        super().__init__(
            input_variables=input_variables,
            **kwargs,
        )

    def _make_input_variables(self, **kwargs):
        return json.loads(kwargs["vars"]) if self.json_input_variables else kwargs

    def format(self, **kwargs) -> str:
        if not self.client:
            raise ValueError("client is not provided")

        data = self._make_input_variables(**kwargs)
        prompt = self.client.prompts.get(
            self.prompt_id,
            environment=self.environment or NOT_GIVEN,
            version=self.version or NOT_GIVEN,
        ).text
        return prompt.format(**data)

    async def aformat(self, **kwargs) -> Awaitable[str]:
        if not self.asyncClient:
            raise ValueError("asyncClient is not provided")

        data = self._make_input_variables(**kwargs)
        prompt = await self.asyncClient.prompts.get(
            self.prompt_id,
            environment=self.environment or NOT_GIVEN,
            version=self.version or NOT_GIVEN,
        )
        return prompt.text.format(**data)
