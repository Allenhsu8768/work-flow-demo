import os
from typing import List, Any
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

from db_model.db_connect import db_session
from db_model.user import User
from db_model.leave import LeaveRequest, LeaveRequestHistory, LeaveType, LeaveRequestDayRecord, LeaveRequestDaysTotal
from tools.tool_permission import check_agent_table_permission, check_agent_confirm_permission

from sqlalchemy import text, update, inspect, func
from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime
from db_model.db_connect import db_session


@tool
def validate_leave_days(
    leave_type: str,
    days: int,
    runtime: ToolRuntime
    ) -> str:
    """
    驗證請假天數是否合法的工具
    args: 
        leave_type: str, 請假類型 -> 可以先去查詢 LeaveType 表, 確認請假類型是否存在
        days: int, 請假天數
    """
    print(f"LLM User requested to validate leave days for leave type: {leave_type} with days: {days}\n")
    user_id = runtime.state.get("user_id", None)
    if days <= 0:
        raise ValueError(f"請假天數 {days} 不能小於等於 0")
    try:
        with db_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            leave_type_id = session.query(LeaveType).filter_by(type=leave_type).first().id
            
            # 查詢使用者申請中的天數
            user_pending_leave_days = session.query(
                    func.sum(LeaveRequestHistory.days)
                ).join(
                    LeaveRequest, 
                    LeaveRequest.id == LeaveRequestHistory.leave_request_id
                ).filter(
                    LeaveRequest.user_id == user_id,
                    LeaveRequest.leave_type_id == leave_type_id,
                    LeaveRequest.status == 'pending',
                    LeaveRequestHistory.status == 'pending',
                    LeaveRequest.start_date <= LeaveRequestHistory.timestamp
                ).scalar() or 0
            
        
            # 查詢使用者的請假類型天數紀錄
            user_leave_days_record = session.query(
                LeaveRequestDayRecord
                ).filter_by(
                    user_id=user_id, 
                    leave_type_id=leave_type_id
                ).first()
            
            # 查詢使用者已請假天數
            user_total_leave_days_record = session.query(
                func.sum(LeaveRequestDaysTotal.days)
                ).filter_by(
                    user_id=user_id, 
                    leave_type_id=leave_type_id
                    ).scalar()
            
            leaved_days = user_total_leave_days_record or 0
            can_leave_days = user_leave_days_record.days - leaved_days - user_pending_leave_days
            validate_days = can_leave_days - days
            
            validate_leave_day_result = f"""
            使用者 {user.name} 的請假類型 [{leave_type}] 
            可請假天數為 {can_leave_days} 天, 
            已請假天數為 {leaved_days} 天, 
            申請中請假天數為 {user_pending_leave_days} 天, 
            本次申請請假天數為 {days} 天, 驗證結果為: {validate_days} 天
            """
            
    except Exception as e:
        raise ValueError(f"驗證請假天數執行失敗: {str(e)}")
    
    return validate_leave_day_result

@tool
def apply_leave_work(
    table_name: str,
    insert_data_list: list[dict[str, Any]],
    days: int,
    runtime: ToolRuntime
    ) -> str:
    """
    提交請假申請的工具
        args:
            table_name: str, 資料庫表名
            insert_data: list[dict[str, Any]]
                - 可以一次申請多筆假別資料
                - 參數欄位請確認與資料表 leave_request 欄位一致，每個 dict 代表一筆資料，key 為欄位名稱，value 為欄位值
                - status 欄位請勿自行填寫，系統會自動填寫為 "待審核"
                - start_date 與 end_date 欄位請在起始加上 08:00:00, 結束加上 17:00:00, 例如: "2023-01-01 08:00:00", "2023-01-02 17:00:00"
            days: int, 請假天數, 用於紀錄請假申請歷史紀錄表
    """
    print(f"LLM User requested to apply leave work for table: {table_name}\n with data: {insert_data_list}\n")
    
    try:
        check_agent_table_permission(
            runtime=runtime, 
            table_names=table_name,
            action_agent_middleware='LeaveWorkFlowMiddleware',
        )
        
    except PermissionError as e:
        raise PermissionError(f"沒有新增此表的權限: {str(e)}")
    
    # 建立 請假申請紀錄
    try:
        with db_session() as session:
            for leave_insert_data in insert_data_list:
                context_use_id = runtime.state.get("user_id", None)
                # 檢查使用者是否存在
                apply_user_id = session.query(User).filter_by(id=leave_insert_data['user_id']).first()
                if not apply_user_id:
                    raise ValueError(f"使用者 ID {leave_insert_data['user_id']} 不存在")
                
                if context_use_id != apply_user_id.id:
                    raise ValueError(f"沒有權限申請其他使用者: {apply_user_id.name} 請假申請，請確認申請人是否正確")
            
            
                start_date = leave_insert_data['start_date']
                end_date = leave_insert_data['end_date']
                if start_date < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
                    raise ValueError(f"請假開始日期 {start_date} 不能小於今天日期 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                if end_date < start_date:
                    raise ValueError(f"請假結束日期 {end_date} 不能小於請假開始日期 {start_date}")
                
                
                # 新增請假申請
                new_leave_request = LeaveRequest(**leave_insert_data)
                session.add(new_leave_request)
                session.flush()
                
                # 建立請假單歷史紀錄
                new_leave_request_history = LeaveRequestHistory(
                    leave_request_id=new_leave_request.id,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=new_leave_request.status,
                    reason=new_leave_request.reason,
                    days=days
                )
                
                session.add(new_leave_request_history)
                session.flush()
            
    except Exception as e:
        raise ValueError(f"提交請假申請執行失敗: {str(e)}")
    
    return "請假申請已提交，等待審核"


@tool
def update_apply_leave_work(
    table_name: str,
    update_data_list: list[dict[str, Any]],
    days: int,
    runtime: ToolRuntime
    ) -> str:
    """
    更新請假申請的工具
        args:
            table_name: str, 資料庫表名
            update_data_list: list[dict[str, Any]]
                - 可以一次更新多筆假別資料
                - 參數欄位請確認與資料表 leave_request 欄位一致，每個 dict 代表一筆資料，key 為欄位名稱，value 為欄位值
                - status 重新提交的狀態為 "待審核", 取消的狀態為 "已取消"
                - start_date 與 end_date 欄位請在起始加上 08:00:00, 結束加上 17:00:00, 例如: "2023-01-01 08:00:00", "2023-01-02 17:00:00"
                - days: int, 請假天數, 用於紀錄請假申請歷史紀錄表
    """
    print(f"LLM User requested to update apply leave work for table: {table_name}\n with data: {update_data_list}\n")
    try:
        check_agent_table_permission(
            runtime=runtime, 
            table_names=table_name,
            action_agent_middleware='LeaveWorkFlowMiddleware',
        )
        
    except PermissionError as e:
        raise PermissionError(f"沒有新增此表的權限: {str(e)}")
    
    # 建立 請假申請紀錄
    try:
        with db_session() as session:
            for leave_update_data in update_data_list:
                context_use_id = runtime.state.get("user_id", None)
                # 檢查使用者是否存在
                apply_user_id = session.query(User).filter_by(id=leave_update_data['user_id']).first()
                if not apply_user_id:
                    raise ValueError(f"使用者 ID {leave_update_data['user_id']} 不存在")
                
                if context_use_id != apply_user_id.id:
                    raise ValueError(f"沒有權限申請其他使用者: {apply_user_id.name} 修改請假紀錄，請確認申請人是否正確")
            
            
                start_date = leave_update_data['start_date']
                end_date = leave_update_data['end_date']
                if start_date < datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
                    raise ValueError(f"請假開始日期 {start_date} 不能小於今天日期 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                if end_date < start_date:
                    raise ValueError(f"請假結束日期 {end_date} 不能小於請假開始日期 {start_date}")
                
                # 更新請假申請
                leave_request_id = leave_update_data['id']
                process_update_data = {k: v for k, v in leave_update_data.items() if k != 'id' and hasattr(LeaveRequest, k)}
                leave_request = session.query(LeaveRequest).filter_by(id=leave_request_id).first()
                if not leave_request:
                    raise ValueError(f"請假申請 ID {leave_request_id} 不存在")
                
                for filed_name, value in process_update_data.items():
                    setattr(leave_request, filed_name, value)
                session.flush()
                
                # 建立請假單歷史紀錄
                new_leave_request_history = LeaveRequestHistory(
                    leave_request_id=leave_request.id,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=leave_request.status,
                    reason=leave_request.reason,
                    days=days
                )
                
                session.add(new_leave_request_history)
                session.flush()
            
    except Exception as e:
        raise ValueError(f"提交請假申請執行失敗: {str(e)}")
    
    return "請假申請已提交，等待審核"


@tool
def manager_confirm_leave_work(
    table_name: str,
    leave_request_list: List[dict[str, Any]],
    runtime: ToolRuntime
    ) -> str:
    """
    批准請假申請的工具
    args:
        table_name: str, 資料庫表名
        leave_request_list: List[dict[str, Any]], 審核請假申請資料列表, 每個 dict 代表一筆請假申請資料, key 為欄位名稱, value 為欄位值
            - example: 
                1. 通過 -> [{id: 1, status: "審核通過", approver_id: 2}]
                2. 拒絕 -> [{id: 1, status: "審核拒絕", approver_id: 2, reject_reason: "理由"}]
                3. 多筆 -> [{id: 1, status: "審核通過", approver_id: 2}, {id: 2, status: "審核拒絕", approver_id: 2, reject_reason: "理由"}]
                4. approver_id -> 部門主管的使用者 ID, 需要與請假申請人的部門一致, 否則無法審核
            - Hint: 部門主管審核請假紀錄時，僅能審核自己部門的請假紀錄，不能審核其他部門的請假紀錄。
    """
    print(f"LLM User requested to manager confirm leave work for table: {table_name}\n with data: {leave_request_list}\n")
    try:
        check_agent_table_permission(
            runtime=runtime, 
            table_names=table_name,
            action_agent_middleware='LeaveWorkFlowMiddleware',
        )
        
    except PermissionError as e:
        raise PermissionError(f"沒有新增此表的權限: {str(e)}")
    
    try:
        with db_session() as session:
            request_user_id = runtime.state.get("user_id", None)
            request_user = session.query(User).filter_by(id=request_user_id).first()
            
            if not request_user.department_manager:
                raise PermissionError(f"使用者 {request_user.name} 不是部門主管，無法審核請假申請")
            
            for leave_request_obj in leave_request_list:
                leave_request_id = leave_request_obj['id']
                leave_request = session.query(LeaveRequest).filter_by(id=leave_request_id).first()
                if not leave_request:
                    raise ValueError(f"請假申請 ID {leave_request_id} 不存在")
                
                # reject_reason 欄位只有在拒絕時才會有值
                reject_reason = leave_request_obj.get('reject_reason', None)
                if leave_request.status == "審核拒絕" and not reject_reason:
                    raise ValueError(f"請假申請 ID {leave_request_id} 被拒絕，請提供拒絕理由")
                
                # 確認部門主管審核
                check_agent_confirm_permission(
                    leave_request=leave_request,
                    approver_id=leave_request_obj['approver_id'],
                    runtime=runtime
                )
                
                # 更新請假申請狀態
                leave_request.status = leave_request_obj['status']
                leave_request.approver_id = leave_request_obj['approver_id']
                session.flush()
                
                # 建立請假單歷史紀錄
                last_leave_request_history = session.query(LeaveRequestHistory).filter_by(
                    leave_request_id=leave_request.id
                    ).order_by(
                        LeaveRequestHistory.timestamp.desc()
                        ).first()
                    
                new_leave_request_history = LeaveRequestHistory(
                    leave_request_id=leave_request.id,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    status=leave_request.status,
                    reason=leave_request.reason,
                    days=last_leave_request_history.days
                )
                
                session.add(new_leave_request_history)
                session.flush()
                
                # 新增累加請假天數紀錄
                if leave_request.status == "審核通過":
                    leave_request_days_total = session.query(LeaveRequestDaysTotal).filter_by(
                        user_id=leave_request.user_id, 
                        leave_type_id=leave_request.leave_type_id
                    ).first()
                    
                    if not leave_request_days_total:
                        leave_request_days_total = LeaveRequestDaysTotal(
                            user_id=leave_request.user_id,
                            leave_type_id=leave_request.leave_type_id,
                            days=last_leave_request_history.days
                        )
                        session.add(leave_request_days_total)
                    else:
                        leave_request_days_total.days += last_leave_request_history.days
                    session.flush()
        
    except Exception as e:
        raise ValueError(f"批准請假申請執行失敗: {str(e)}")
    
    return "請假申請已審核完成"
