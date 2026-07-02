
from typing import Callable


# Langchain imports
from langchain.agents.middleware import  dynamic_prompt, ModelRequest, ToolCallRequest, AgentMiddleware
from langgraph.runtime import Runtime
from langchain_core.messages import ToolMessage


from db_model import model_register
from db_model.user import User
from db_model.db_connect import db_session
from prompt.systemprompt import LeaveWorkFlowSystemPrompt, UpdateTableInfoSystemPrompt
from format.schema_format import UserAgentState

@dynamic_prompt
def leave_work_flow_dynamic_system_prompt(request: ModelRequest) -> str:
    """
        根據 state 動態生成 system prompt 的 middleware 
    """
    work_system_prompt = LeaveWorkFlowSystemPrompt(request)
    return work_system_prompt.get_system_prompt()


@dynamic_prompt
def update_table_info_dynamic_system_prompt(request: ModelRequest) -> str:
    """
        根據 state 動態生成 system prompt 的 middleware
    """
    update_table_info_dynamic_system_prompt = UpdateTableInfoSystemPrompt(request)
    return update_table_info_dynamic_system_prompt.get_system_prompt()


class CommonMiddleware(AgentMiddleware):
    """
        繼承 AgentMiddleware 在週期寫入邏輯的
    """
    def before_agent(self, state: UserAgentState, runtime: Runtime) -> dict | None:
        """
        在 agent 執行前的週期，可以在這裡加入一些邏輯
        初始化使用者的資料, 及資料表資料
        """
        # 生成資料表資訊
        table_info_obj_list = [
            { 
                model_class.__tablename__: model_class.__doc__
            } for _, model_class in model_register.items()
        ]
        
        table_agent_permission_list = [
            {
                model_class.__tablename__: model_class.agent_table_permission[self.__class__.__name__]
            } for _, model_class in model_register.items()
        ]
        
        # 初始化
        with db_session() as session:
            user = session.query(User).filter_by(id=state['user_id']).first()
            
            if not user:
                raise ValueError(f"找不到使用者，請檢查使用者ID是否正確。")
            
            user_info = {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "root_user": user.root_user,
                "department": user.department.department_name,
                "department_manager": True if user.department_manager else None
            }
        
        return {
            **user_info,
            'table_info': table_info_obj_list,
            'table_agent_permission': table_agent_permission_list
        }

    def wrap_tool_call(
        self, 
        request: ToolCallRequest, 
        handler: Callable[[ToolCallRequest], ToolMessage]
        ) -> ToolMessage:
        """
            在 agent 執行工具呼叫的週期，可以在這裡加入一些邏輯
            當 Tool 呼叫失敗時，可以捕獲異常並返回一個格式統一的錯誤訊息
        """
        try:
            return handler(request)
        except Exception as e:
            error_msg = f"工具調用失敗: {str(e)}"
            print(error_msg)
            return ToolMessage(
                content=error_msg,
                tool_call_id=request.tool_call['id'],
                name=request.tool_call['name']
            )

class LeaveWorkFlowMiddleware(CommonMiddleware):
    """
        繼承 AgentMiddleware 在週期寫入邏輯的
    """
    pass

class UpdateTableInfoMiddleware(CommonMiddleware):
    """
        繼承 AgentMiddleware 在週期寫入邏輯的
    """
    pass