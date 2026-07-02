
from typing import List, TYPE_CHECKING
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from department import DepartmentManager
    from user import User


class LeaveRequest(Base):
    """
    請假申請表
        - 儲存請假申請的基本資訊, 包含申請人、請假類型、開始日期、結束日期、請假原因、審核狀態等
        - 員工資訊表(User)有多對一的關係, 一個請假申請只能對應一個員工
        - 請假類別表(LeaveType)有多對一的關係, 一個請假申請只能對應一個請假類型
        - 部門主管表(DepartmentManager)有多對一的關係, 一個請假申請只能對應一個審核人
        - 請假申請歷史紀錄表(LeaveRequestHistory)有一對多的關係, 一個請假申請可以有多筆歷史紀錄
    """
    
    __tablename__ = "leave_request"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view', 'update', 'create'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="請假申請ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="使用者ID")
    user: Mapped["User"] = relationship("User", back_populates="leave_request")
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_type.id"), nullable=False, comment="請假類型ID")
    leave_type: Mapped["LeaveType"] = relationship("LeaveType", back_populates="leave_request")
    start_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, comment="請假開始日期")
    end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False, comment="請假結束日期")
    reason: Mapped[str] = mapped_column(String(255), nullable=False, comment="請假原因")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="待審核", comment="請假狀態")
    reject_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="拒絕原因")
    approver_id: Mapped[Optional[int]] = mapped_column(ForeignKey("department_manager.id"), nullable=True, comment="已審核人員ID")
    approver: Mapped[Optional["DepartmentManager"]] = relationship("DepartmentManager", back_populates="leave_request")
    leave_request_history: Mapped[List["LeaveRequestHistory"]] = relationship("LeaveRequestHistory", back_populates="leave_request")

class LeaveRequestHistory(Base):
    """
    請假申請歷史紀錄表
        - 儲存請假申請的歷史紀錄, 包含請假申請ID、時間戳記、狀態、原因等
        - 請假申請表(LeaveRequest)可以紀錄只能對應一個請假申請
    """
    
    __tablename__ = "leave_request_history"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view', 'update', 'create'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="請假申請歷史紀錄ID")
    leave_request_id: Mapped[int] = mapped_column(ForeignKey("leave_request.id"), nullable=False, comment="請假申請ID")
    leave_request: Mapped["LeaveRequest"] = relationship("LeaveRequest", back_populates="leave_request_history")
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False, comment="時間戳記")
    status: Mapped[str] = mapped_column(String(50), nullable=False, comment="請假狀態")
    reason: Mapped[str] = mapped_column(String(255), nullable=True, comment="請假原因")
    days: Mapped[Optional[int]] = mapped_column(nullable=False, comment="請假天數")

class LeaveType(Base):
    """
    請假類別表
        - 儲存請假類別的基本資訊, 包含類別名稱、描述等
        - 請假申請表(LeaveRequest)有一對多的關係, 一個請假類別可以有多個請假申請
        - 員工年資假天數紀錄表(LeaveRequestDayRecord)有一對多的關係, 一個請假類別可以有多個年資假天數紀錄
        - 員工已請假天數紀錄表(LeaveRequestDaysTotal)有一對多的關係, 一個請假類別可以有多個已請假天數紀錄
    """
    
    __tablename__ = "leave_type"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="請假類別ID")
    type: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, comment="請假類別名稱")
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="請假類別描述")
    leave_request: Mapped[List["LeaveRequest"]] = relationship("LeaveRequest", back_populates="leave_type")
    leave_request_day_record: Mapped[List["LeaveRequestDayRecord"]] = relationship("LeaveRequestDayRecord", back_populates="leave_type")
    leave_request_days_total: Mapped[List["LeaveRequestDaysTotal"]] = relationship("LeaveRequestDaysTotal", back_populates="leave_type")

class LeaveRequestDayRecord(Base):
    """
    員工年資假天數紀錄表
        - 儲存員工的年資假天數紀錄, 包含請假類別ID、使用者ID、天數等
        - 請假類別表(LeaveType)有多對一的關係, 一個年資假天數紀錄只能對應一個請假類別
        - 員工資訊表(User)有多對一的關係, 一個年資假天數紀錄只能對應一個員工
    """
    
    __tablename__ = "leave_request_day_record"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="年資假天數紀錄ID")
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_type.id"), nullable=False, comment="請假類型ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="使用者ID")
    days: Mapped[int] = mapped_column(nullable=False, default=0, comment="年資假天數")
    
    # relation fields
    leave_type: Mapped["LeaveType"] = relationship("LeaveType", back_populates="leave_request_day_record")
    user: Mapped["User"] = relationship("User", back_populates="leave_request_day_record")
    
    
class LeaveRequestDaysTotal(Base):
    """
    員工已請假天數紀錄表
        - 儲存員工的已請假天數紀錄, 包含使用者ID、請假類別ID、天數等
        - 員工資訊表(User)有多對一的關係, 一個已請假天數紀錄只能對應一個員工
        - 請假類別表(LeaveType)有多對一的關係, 一個已請假天數紀錄只能對應一個請假類別
    """
    
    __tablename__ = "leave_request_days_total"
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="已請假天數紀錄ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, comment="使用者ID")
    
    
    user: Mapped["User"] = relationship("User", back_populates="leave_request_days_total")
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_type.id"), nullable=False, comment="請假類型ID")
    days: Mapped[int] = mapped_column(nullable=False, default=0, comment="已請假天數")
    
    # relation fields
    leave_type: Mapped["LeaveType"] = relationship("LeaveType", back_populates="leave_request_days_total")


export_model_class = {
    LeaveRequest.__tablename__: LeaveRequest,
    LeaveRequestHistory.__tablename__: LeaveRequestHistory,
    LeaveType.__tablename__: LeaveType,
    LeaveRequestDayRecord.__tablename__: LeaveRequestDayRecord,
    LeaveRequestDaysTotal.__tablename__: LeaveRequestDaysTotal,
}

