from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        nullable=False, 
        server_default=func.now()
        )
    update_time: Mapped[datetime] = mapped_column(
        nullable=False, 
        server_default=func.now(), 
        onupdate=func.now())
    
    agent_table_permission = {
        'LeaveWorkFlowMiddleware': ['view'],
        'UpdateTableInfoMiddleware': ['view', 'update', 'create', 'delete'],
    }
    
    @classmethod
    def get_class_name(cls):
        return cls.__name__
    
    @classmethod
    def get_model_schema(cls) -> str:
        """
        回傳資料庫模型的結構化資訊用於模型了解資料結構
        """
        columns = inspect(cls).columns
        relationships = inspect(cls).relationships
        
        # table description
        output_list = [f"\n============= Model Class Name: {cls.get_class_name()} =========="]
        output_list.append(f"  Table Name: {cls.__tablename__}")
        
        # column and relationship information
        for idx, column in enumerate(columns):
            output_list.append(f"  Column Field: {idx + 1}: {column.key}, Type: {column.type}, Nullable: {column.nullable}, Primary Key: {column.primary_key}, Comment: {column.comment}")

        for idx, relationship in enumerate(relationships):
            output_list.append(f"  Relationship Field: {idx + 1}: {relationship.key}, Direction: {relationship.direction}, Target: {relationship.target}")
        
        return output_list