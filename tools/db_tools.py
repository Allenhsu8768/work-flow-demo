import os
from typing import List, Any
from dotenv import load_dotenv

load_dotenv()

from db_model.db_connect import db_session
from db_model import model_register
from tools.tool_permission import select_sql_query_safety, alter_or_insert_db_permission

from sqlalchemy import text, update, inspect


from langchain_core.tools import tool
from langgraph.prebuilt import ToolRuntime


@tool
def all_model_class_schema(runtime: ToolRuntime) -> str:
    """
    回傳所有資料庫模型的結構化資訊
        - 根據用戶的需求, 需要做出的動作前若不知道表結構可以透過此工具查詢對應的表結構資訊, 以利後續工具的使用
    """
    print('LLM User requested all model class schema information.\n')
    out_put_string_list = []
    for _, model_class in model_register.items():
        out_put_string_list.extend(model_class.get_model_schema())
            
    return '\n'.join(out_put_string_list)


@tool
def table_name_map_schema(table_name: str, runtime: ToolRuntime) -> str:
    """
    如果已經確定要查指定的表名, 請傳入參數找尋對應的資料庫模型的結構化資訊
        - args: 
            table_name: str, 資料庫表名
    """
    print(f'LLM User requested schema information for table: {table_name}\n')
    try:
        model_class = model_register[table_name]

    except KeyError as e:
        raise ValueError(f"資料表 {table_name} 不存在於資料庫中, 錯誤訊息: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"發生未知錯誤: {str(e)}")
    else:
        return '\n'.join(model_class.get_model_schema())


@tool
def select_from_db(
    table_names: List[str], 
    sql_query: str | None, 
    runtime: ToolRuntime
    ) -> str:
    """
    【高階複合查詢工具】當你需要進行多表聯查（JOIN）、大小比較（>、<）、OR 邏輯、
        排序（ORDER BY）或聚合函數（COUNT、SUM）等複雜查詢時，使用此工具。
    
    Args:
        table_names: (List[str]) -> 這次查詢中所有涉及到的資料表名稱清單（例如: ['user', 'leave_request']），用作權限查核。
        sql_query: (str) -> 標準的 SQL SELECT 語句。請務必使用標準 SQL 語法。
    Hint:
        1. 只有人事部門或是後台管理部門的使用者才有權限去查詢其他使用者的相關資訊包含請假紀錄。
        2. 不是人事部門、後台管理部門的使用者僅能查詢自己本人的請假紀錄及資訊, 
        3. 部門主管能夠查下面員工的相關資訊及請假紀錄, 但不能去查其他部門的任何資訊。
    """
    print(f"LLM User requested to select from table: {table_names}  with SQL query: \n {sql_query}\n")
    
    try:
        select_sql_query_safety(table_names, sql_query, runtime)
        
    except PermissionError as e:
        raise PermissionError(str(e))
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        raise RuntimeError(f"發生未知錯誤: {str(e)}")
    
    try:
        for table_name in table_names:
            if table_name not in model_register:
                raise ValueError(f"資料表 {table_name} 不存在於資料庫中。")
            
        with db_session() as session:
            result = session.execute(text(sql_query))
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            
    except Exception as e:
        raise RuntimeError(f"查詢資料庫時發生錯誤: {str(e)}")
    
    if rows:
        return '\n'.join([str(row) for row in rows])
    
    return f"查詢資料庫成功, 查詢的表為 : [{', '.join(table_names)}], 沒有返回任何資料。\n  SQL 語句: {sql_query}"


@tool
def insert_into_db(
    table_name: str,  
    fields_dict_list: List[dict[str, Any]], 
    runtime: ToolRuntime
    ) -> str:
    """
    插入資料到資料庫
        args: 
            -table_name: str, 資料表名稱
            -fields_dict_list: List[dict[str, Any]], 欄位資料清單，每個 dict 代表一筆資料，key 為欄位名稱，value 為欄位值
    """
    print(f"LLM User requested to insert into table: {table_name}  with fields: \n {fields_dict_list}\n")
    
    if not fields_dict_list:
        raise ValueError("沒有提供任何要插入的欄位資料。")
    
    try:
        alter_or_insert_db_permission(table_name, runtime)
        model_cls = model_register[table_name]
        
        with db_session() as session:
            inserted_records = []
            
            for fields_dict in fields_dict_list:
                valid_fields = {k: v for k, v in fields_dict.items() if hasattr(model_cls, k)}
                new_record = model_cls(**valid_fields)
                inserted_records.append(new_record)
                    
            session.add_all(inserted_records)
            
    except PermissionError as e:
        raise PermissionError(str(e))
    
    except KeyError as e:
        raise ValueError(f"資料表 {table_name} 不存在於資料庫中, 錯誤訊息: {str(e)}")
    
    except Exception as e:
        raise RuntimeError(f"插入資料到資料庫時發生錯誤: {str(e)}")
    
    
    return f"成功插入 {len(inserted_records)} 筆資料到表 [{table_name}] 中。"


@tool
def update_db(
    table_name: str,
    filter_fields_dict: dict[str, Any],
    update_fields_dict: dict[str, Any],
    runtime: ToolRuntime
    ) -> str:
    """
        args: 
            -table_name: str, 資料表名稱
            -filter_fields_dict: dict[str, Any], 過濾條件清單，每個 dict 代表一個過濾條件，key 為欄位名稱，value 為欄位值
            -update_fields_dict: dict[str, Any], 欲更新的欄位資料，key 為欄位名稱，value 為欄位值
    """
    print(f"LLM User requested to update table: {table_name}  with filter: \n {filter_fields_dict} and update fields: \n {update_fields_dict}\n")
    
    try:
        alter_or_insert_db_permission(table_name, runtime)
        model_cls = model_register[table_name]
    
    except PermissionError as e:
        raise PermissionError(str(e))
    except KeyError as e:
        raise ValueError(f"資料表 {table_name} 不存在於資料庫中, 錯誤訊息: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"發生未知錯誤: {str(e)}")
    
    try:
        with db_session() as session:
            execute_update = update(model_cls)
            
            valid_filter_fields = {k: v for k, v in filter_fields_dict.items() if hasattr(model_cls, k)}
            valid_update_fields = {k: v for k, v in update_fields_dict.items() if hasattr(model_cls, k)}
            
            
            if not valid_filter_fields or not valid_update_fields:
                raise ValueError("沒有提供任何有效的過濾條件欄位或更新欄位。")
            
            for filed_name, value in valid_filter_fields.items():
                column_obj = getattr(model_cls, filed_name)
                
                if isinstance(value, list):
                    execute_update = execute_update.where(column_obj.in_(value))
                else:
                    execute_update = execute_update.where(column_obj == value)

            execute_update = execute_update.values(**valid_update_fields)
            session.execute(execute_update)
        
    except Exception as e:
        raise RuntimeError(f"更新資料庫時發生錯誤: {str(e)}")
    
    return f"成功更新表 [{table_name}] 中符合條件的資料。"

