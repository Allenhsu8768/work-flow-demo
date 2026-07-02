from typing import Any
import time
from datetime import datetime
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessageChunk


from agents.agent_class import LeaveWorkFlowAgent, UpdateOrCreateTableInfoAgent
from llm_model.ollama_model import ollama_gpt_model_20b
from tools.db_tools import (
    all_model_class_schema,
    table_name_map_schema,
    select_from_db, 
    insert_into_db, 
    update_db, 
)

from tools.leave_work_flow_tools import (
    validate_leave_days,
    apply_leave_work,
    update_apply_leave_work,
    manager_confirm_leave_work
)

from agents.middleware.agent_middleware import leave_work_flow_dynamic_system_prompt, update_table_info_dynamic_system_prompt, \
    LeaveWorkFlowMiddleware, UpdateTableInfoMiddleware
from format.schema_format import UserAgentState, TableInfoAgentState


from db_model.db_connect import db_session
from db_model.user import User
from terminal import TerminalSpinner
from terminal import terminal_display_panel

checkpoint_saver = InMemorySaver()
table_info_update_instance = UpdateOrCreateTableInfoAgent(
    model=ollama_gpt_model_20b,
    tools=[
        all_model_class_schema, 
        table_name_map_schema,
        select_from_db,
        insert_into_db,
        update_db
    ],
    middleware=[
        update_table_info_dynamic_system_prompt,
        UpdateTableInfoMiddleware(),
    ],
    state_schema=TableInfoAgentState,
    checkpointer=checkpoint_saver
)


leave_work_flow_instance = LeaveWorkFlowAgent(
    model=ollama_gpt_model_20b,
    tools=[
        table_name_map_schema,
        all_model_class_schema,
        select_from_db,
        apply_leave_work,
        update_apply_leave_work,
        validate_leave_days,
        manager_confirm_leave_work
    ],
    middleware=[
        leave_work_flow_dynamic_system_prompt,
        LeaveWorkFlowMiddleware(),
    ],
    state_schema=TableInfoAgentState,
    checkpointer=checkpoint_saver
)

table_info_update_agent = table_info_update_instance.new_agent()
leave_work_flow_agent = leave_work_flow_instance.new_agent()


def create_memory_key(user_data: dict[str, Any]) -> str:
    user_id = user_data['id']
    user_name = user_data['name']
    datetime_now = datetime.now().strftime("%Y-%m-%d")
    memory_key = f"{user_id}_{user_name}_{datetime_now}"
    return memory_key

def terminal_spinner(
    agent_name: str,
    message: str,
    hint_message: str
    ):
    def decorator(func):
        def wrapper(*args, **kwargs):
            loading_spinner = TerminalSpinner(message=message)
            user_data = kwargs.get('user_data', {})
            future_work_name = kwargs.get('future_work_name', '')
            memory_key = create_memory_key(user_data)
            
            func_add_kwargs = {
                "memory_key": memory_key,
                "future_work_name": future_work_name,
                "loading_spinner": loading_spinner,
            }
            
            kwargs.update(func_add_kwargs)
            
            terminal_display_panel(future_work_name, hint_message, agent_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@terminal_spinner(
    agent_name="Table Update Agent",
    message="Table Update Agent 思考中...", 
    hint_message="我是資料庫後台智能助手, 請問有什麼可以幫助您的嗎 ?"
    )
def action_table_update_agent(
    user_data: dict[str, Any],
    future_work_name: str,
    memory_key: str,
    loading_spinner: TerminalSpinner
    ) -> None:
    while True:
        user_prompt = input("請輸入您想要執行的操作 (輸入 'exit' 離開):  ")
        if user_prompt.lower() == "exit":
            print(f"已退出 - {future_work_name}")
            break
        
        loading_spinner.start()
        response = table_info_update_agent.stream(
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                ],
                "user_id": user_data['id'],
            },
            config={
                "configurable" : {
                    "thread_id": memory_key,
                }
            },
            stream_mode="messages"
        )
        
        for chuck, _ in response:
            if isinstance(chuck, AIMessageChunk):
                if chuck.content:
                    loading_spinner.stop()
                    print(chuck.content, end='', flush=True)
        print('\n')
        
@terminal_spinner(
    agent_name="Leave Work Flow Agent",
    message="Leave Work Flow Agent 思考中...",
    hint_message="我是資料庫後台智能助手, 請問有什麼可以幫助您的嗎 ?"
    )
def action_leave_work_flow_agent(
    user_data: dict[str, Any],
    future_work_name: str,
    memory_key: str,
    loading_spinner: TerminalSpinner
    ) -> None:
    while True:
        user_prompt = input("請輸入您想要執行的操作 (輸入 'exit' 離開):  ")
        if user_prompt.lower() == "exit":
            print(f"已退出 - {future_work_name}")
            break
        
        loading_spinner.start()
        response = table_info_update_agent.stream(
            input={
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt
                    },
                ],
                "user_id": user_data['id'],
            },
            config={
                "configurable" : {
                    "thread_id": memory_key,
                }
            },
            stream_mode="messages"
        )
        
        for chuck, _ in response:
            if isinstance(chuck, AIMessageChunk):
                if chuck.content:
                    loading_spinner.stop()
                    print(chuck.content, end='', flush=True)
        print('\n')