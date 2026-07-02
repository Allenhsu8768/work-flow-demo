from typing import (
    Sequence,
    Callable,
    Any,
)
from langgraph.cache.base import BaseCache
from langgraph.store.base import BaseStore
from langgraph.stream._mux import TransformerFactory
from langgraph.types import Checkpointer
from langchain_core.language_models import BaseChatModel
from langchain.agents import create_agent
from langchain.agents.middleware.types import (
    AgentMiddleware,
    AgentState,
    ContextT,
    ResponseT,
    StateT_co,
)

from langchain.agents.structured_output import (
    ResponseFormat,
)

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage, trim_messages
from langchain_core.tools import BaseTool
from langchain.agents.middleware.types import (AgentMiddleware,AgentState,)


from llm_model.count_token import count_tokens

class CommonAgent(object):
    def __init__(
        self, 
        model: str | BaseChatModel,
        tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] | None = None,
        system_prompt: str | SystemMessage | None = None,
        middleware: Sequence[AgentMiddleware[StateT_co, ContextT]] = (),
        response_format: ResponseFormat[ResponseT] | type[ResponseT] | None = None,
        state_schema: type[AgentState[ResponseT]] | None = None,
        context_schema: type[ContextT] | None = None,
        checkpointer: Checkpointer | None = None,
        store: BaseStore | None = None,
        interrupt_before: list[str] | None = None,
        interrupt_after: list[str] | None = None,
        debug: bool = False,
        name: str | None = None,
        cache: BaseCache[Any] | None = None,
        transformers: Sequence[TransformerFactory] | None = None, 
        ):
        
        self.model = model
        self.tools = tools
        self.system_prompt = system_prompt
        self.middleware = middleware
        self.response_format = response_format
        self.state_schema = state_schema
        self.context_schema = context_schema
        self.checkpointer = checkpointer
        self.store = store
        self.interrupt_before = interrupt_before
        self.interrupt_after = interrupt_after
        self.debug = debug
        self.name = name
        self.cache = cache
        self.transformers = transformers

    def new_agent(self):
        agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
            middleware=self.middleware,
            response_format=self.response_format,
            state_schema=self.state_schema,
            context_schema=self.context_schema,
            checkpointer=self.checkpointer,
            store=self.store,
            interrupt_before=self.interrupt_before,
            interrupt_after=self.interrupt_after,
            debug=self.debug,
            name=self.name,
            cache=self.cache,
            transformers=self.transformers
        )
        return agent
