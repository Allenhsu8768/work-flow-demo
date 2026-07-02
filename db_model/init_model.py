import os
from dotenv import load_dotenv

load_dotenv()

from db_model.db_connect import PostgresSqlConnect
from db_model.base import Base
from db_model.user import User
from db_model.department import Department, DepartmentManager
from db_model.leave import LeaveRequest, LeaveRequestHistory

db_login_config = {
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "database": os.getenv("POSTGRES_DATABASE")
}



if __name__ == "__main__":
    with PostgresSqlConnect(**db_login_config) as db_connect:
        # 建立資料表
        Base.metadata.create_all(db_connect.engine)
        print(f"Database Create Success!")
    