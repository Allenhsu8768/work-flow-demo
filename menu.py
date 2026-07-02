import sys
from login import user_login
from datetime import datetime
from terminal import clear_screen
from agents.action_agent import action_table_update_agent, action_leave_work_flow_agent
from typing import Any


menu_future_list = [
    {
            "menu_id": "1",
            "menu_name": "📝 申請修改請假作業",
        },
        {
            "menu_id": "2",
            "menu_name": "⚖️ 請假審核作業",
        },
        {
            "menu_id": "3",
            "menu_name": "➕ 新增資訊 (員工/部門)作業",
        },
    ]

def validate_user_menu(user_data: dict[str, Any], choice: str) -> bool:
    """驗證使用者選擇的功能是否符合權限"""
    department_name = user_data.get('department_name', '')
    department_manager = user_data.get('department_manager', False)
    
    match choice:
        case "2":
            return department_manager
        case "3":
            return department_name in ['人事部門', '後台管理部門']
        case _:
            return True

def menu_list_permission_map(user_data: dict[str, Any]) -> dict[str, bool]:
    """建立功能選單與權限對應的字典"""
    return [f"{index}. {future['menu_name']}" 
            for index, future in enumerate(menu_future_list, start=1) if validate_user_menu(user_data, future["menu_id"])
            ]




def show_menu(user_data: dict[str, Any]) -> None:
    """印出主選單頁面"""
    menu_list = menu_list_permission_map(user_data)
    print("=" * 40)
    print(f"{'員工請假管理系統':^30}")
    print("=" * 40)
    for menu in menu_list:
        print(menu)
    print(f"0. ❌ 退出系統")
    print("=" * 40)