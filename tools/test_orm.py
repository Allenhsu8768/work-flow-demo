from db_model.db_connect import db_session
from db_model.user import User



email = input("請輸入使用者的電子郵件地址:  ")
password = input("請輸入使用者的密碼:  ")


with db_session() as session:
    # 查詢所有使用者
    user = session.query(User).filter_by(email=email, password=password).first()
    print(user.department.department_name)
    



