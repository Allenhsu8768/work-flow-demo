
from typing import List
from langgraph.prebuilt import ToolRuntime
from db_model import model_register
from db_model.db_connect import db_session
from db_model.leave import LeaveRequest
from db_model.user import User


sql_query_dangerous_keywords = [
    "delete", "drop", "alter", "create"
]

def schema_permission(runtime: ToolRuntime):
    state = runtime.state
    root_user = state.get("root_user", False)
    if not root_user:
        raise PermissionError("沒有權限可以查詢表的相關結構資訊，請聯絡系統管理員。")

def select_sql_query_safety(
    table_names: List[str], 
    sql_query: str, 
    runtime: ToolRuntime
):
    cleaned_query = sql_query.strip().lower()
    
    if not cleaned_query.startswith("select") or any(keyword in cleaned_query for keyword in sql_query_dangerous_keywords):
        raise PermissionError("僅允許使用 SELECT 查詢語句。")
    
    if not cleaned_query:
        raise ValueError("SQL 查詢語句不能為空。")

def alter_or_insert_db_permission(
    table_name: str, 
    runtime: ToolRuntime
):
    state = runtime.state
    root_user = state.get("root_user", False)
    department = state.get("department", None)
    if department != "人事部門" and not root_user:
        raise PermissionError(f"沒有權限可以修改或插入資料到表 [{table_name}]，請聯絡系統管理員。")

def check_agent_table_permission(
    runtime: ToolRuntime,
    table_names: str, 
    action_agent_middleware: str
):
    try:
        model_cls = model_register[table_names]
    except KeyError:
        raise PermissionError(f"表 [{table_names}] 不存在，請聯絡系統管理員。")
    
    agent_permission_list = model_cls.agent_table_permission.get(action_agent_middleware, [])
    
    if 'create' not in agent_permission_list or 'update' not in agent_permission_list:
        raise PermissionError(f"沒有權限可以修改或插入資料到表 [{table_names}]，請聯絡系統管理員。")

    return True

def check_agent_confirm_permission(
    leave_request: LeaveRequest,
    approver_id: int,
    runtime: ToolRuntime,
):
    with db_session() as session:
        approver = session.query(User).filter_by(id=approver_id).first()
        leave_request_user = session.query(User).filter_by(id=leave_request.user_id).first()
        if not approver:
            raise ValueError(f"審核人員 ID {approver_id} 不存在")
        if approver.department != leave_request_user.department:
            raise PermissionError(f"請假申請 ID {leave_request.id} 的審核人員 {approver.name} 與申請人 {leave_request_user.name} 不在同一部門，無法審核")