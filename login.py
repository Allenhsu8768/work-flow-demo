from db_model.user import User
from db_model.db_connect import db_session
from terminal import clear_screen
import getpass

def user_login():
    """使用者登入驗證"""
    user_info = {}
    while not user_info:
        clear_screen()
        print("=== 登入帳號 ===")
        email = input("請輸入電子信箱: ")
        password = getpass.getpass("請輸入密碼: ")
        print(f"\n系統提示：正在驗證 {email} 的身分...")
        with db_session() as session:
            try:
                import time
                time.sleep(2)
                user = session.query(User).filter_by(email=email, password=password).first()
                if user:
                    user_info = user.__dict__.copy()
                    user_info.update(
                        {
                            'department_name': user.department.department_name if user.department else '',
                            'department_manager': True if user.department and user.department.manager.user_id == user.id else False
                            }
                        )
                else:
                    print("❌ 登入失敗，請檢查電子信箱或密碼是否正確, 會自動跳轉重新輸入。")
                    import time
                    time.sleep(1.5)
                    continue
                
            except Exception as e:
                print(f"❌ 發生錯誤: {str(e)}")
            
            else:
                print(f"✅ 登入成功，歡迎 {user_info['name']}, 隸屬於 {user_info['department_name']}！")
                input("\n[按 Enter 鍵返回主選單]")
    return user_info