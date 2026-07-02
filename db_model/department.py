
from typing import List, TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from user import User
    from leave import LeaveRequest


class Department(Base):
    """
    部門表
        - 儲存部門的基本資訊, 包含部門名稱、部門主管等
        - 部門主管表(DepartmentManager)有一對一的關係, 一個部門只能有一個主管
        - 員工資訊表(User)有一對多的關係, 一個部門可以有多個員工
    """
    __tablename__ = "department"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="部門ID")
    department_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="部門名稱")
    manager_id: Mapped[Optional[int]] = mapped_column(ForeignKey("department_manager.id"), nullable=True, comment="部門主管ID")
    
    # relation fields
    manager: Mapped[Optional["DepartmentManager"]] = relationship("DepartmentManager", back_populates="department")
    users: Mapped[list["User"]] = relationship("User", back_populates="department")

class DepartmentManager(Base):
    """
    部門主管表
        - 儲存部門主管的基本資訊, 包含使用者ID、是否為CEO等
        - 員工資訊表(User)有一對一的關係, 一個部門主管只能對應一個員工
        - 部門表(Department)有一對一的關係, 一個部門只能有一個主管
    """
    __tablename__ = "department_manager"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="部門主管ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, comment="使用者ID")
    is_ceo: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否為CEO")
    
    # relation fields
    user: Mapped["User"] = relationship("User", back_populates="department_manager")
    department: Mapped["Department"] = relationship("Department", back_populates="manager")
    leave_request: Mapped[List["LeaveRequest"]] = relationship("LeaveRequest", back_populates="approver")





export_model_class = {
    Department.__tablename__: Department,
    DepartmentManager.__tablename__: DepartmentManager
}