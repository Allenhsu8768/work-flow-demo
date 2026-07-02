from typing import Annotated
from langchain.agents.middleware import AgentState



class UserAgentState(AgentState):
    user_id: Annotated['int', "使用者ID"]
    name: Annotated['str', "使用者名稱"]
    email: Annotated['str', "使用者電子郵件"]
    root_user: Annotated['bool', "使用者是否為系統管理員"]
    department: Annotated['str', "使用者所屬部門"]
    department_manager: Annotated['bool', "使用者是否為部門主管"]


class TableInfoAgentState(UserAgentState):
    table_info: Annotated['list[dict[str, str]]', "資料庫中所有資料表的名稱和描述列表"]
    table_agent_permission: Annotated['list[dict[str, list[str]]]', "資料庫中所有資料表對應的 Agent 權限列表"]
