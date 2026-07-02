
import sys
from login import user_login
from terminal import clear_screen
from agents.action_agent import action_table_update_agent, action_leave_work_flow_agent
from menu import show_menu, validate_user_menu, menu_list_permission_map, menu_future_list

def enter_work_flow_system():
    user_data = {}
    while True:
        clear_screen()
        if not user_data:
            user_data = user_login()
            
        show_menu(user_data)
        
        choice = input(f"請輸入欲執行的功能編號 (0 - {len(menu_list_permission_map(user_data))}): ").strip()
        choice_future_obj = [obj for obj in menu_future_list if obj['menu_id'] == choice]
        if choice_future_obj:
            choice_future_obj = choice_future_obj[0]
        menu_permission_check = validate_user_menu(user_data, choice_future_obj["menu_id"]) if choice_future_obj else False
            
        if choice == "1":
            clear_screen()
            action_leave_work_flow_agent(
                user_data=user_data,
                future_work_name=choice_future_obj["menu_name"]
                )
            input("\n[按 Enter 鍵返回主選單]")
            
        elif choice == "2" and menu_permission_check:
            clear_screen()
            action_leave_work_flow_agent(
                user_data=user_data,
                future_work_name=choice_future_obj["menu_name"]
                )
            input("\n[按 Enter 鍵返回主選單]")
            
        elif choice == "3" and menu_permission_check:
            clear_screen()
            action_table_update_agent(
                user_data=user_data,
                future_work_name=choice_future_obj["menu_name"]
                )
            input("\n[按 Enter 鍵返回主選單]")
            
        elif choice == "0":
            print("\n感謝使用本系統，再見！")
            sys.exit()
            
        else:
            print(f"\n❌ { f'{user_data['name']}, ' if user_data.get('name') else ''}輸入錯誤！請輸入 0 到 3 之間的數字。")
            import time
            time.sleep(1.5)