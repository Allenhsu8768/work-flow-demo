from typing import List, TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db_model.base import Base


if TYPE_CHECKING:
    from department import Department, DepartmentManager
    from leave import LeaveRequest, LeaveRequestDaysTotal, LeaveRequestDayRecord

class User(Base):
    """
    員工資訊表
    - 儲存員工的基本資訊, 包含姓名、電子郵件、密碼、是否為 root 使用者等
    - 部門表(Department)有多對一的關係, 一個員工只能屬於一個部門
    - 請假申請表(LeaveRequest)有一對多的關係, 一個員工可以有多筆請假申請紀錄
    - 員工年資假天數紀錄表(LeaveRequestDayRecord)有一對多的關係, 一個員工可以有多筆年資假天數紀錄
    - 請假天數統計表(LeaveRequestDaysTotal)有一對多的關係, 一個員工可以有多筆請假天數統計紀錄
    """
    __tablename__ = "users"
    
    # 權限設定
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="使用者ID")
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="使用者名稱")
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="使用者電子郵件")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="使用者密碼")
    root_user: Mapped[bool] = mapped_column(default=False, nullable=False, comment="是否為 root 使用者")
    department_id: Mapped[int] = mapped_column(ForeignKey("department.id"), nullable=False, comment="部門ID")
    
    # relation fields
    department: Mapped["Department"] = relationship("Department", back_populates="users")
    department_manager: Mapped[Optional["DepartmentManager"]] = relationship(
        "DepartmentManager", back_populates="user", uselist=False
    )
    leave_request: Mapped[List["LeaveRequest"]] = relationship("LeaveRequest", back_populates="user")
    leave_request_day_record: Mapped[List["LeaveRequestDayRecord"]] = relationship("LeaveRequestDayRecord", back_populates="user")
    leave_request_days_total: Mapped[List["LeaveRequestDaysTotal"]] = relationship("LeaveRequestDaysTotal", back_populates="user")
    



export_model_class = {
    User.__tablename__: User,
}