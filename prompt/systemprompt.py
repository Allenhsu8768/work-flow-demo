from langchain.agents.middleware import ModelRequest


class CommonSystemPrompt(object):
    """
        定義一個 Common 的 system prompt 的範例。
    """
    def __init__(self, request: ModelRequest):
        self.request: ModelRequest = request
        self.agent_default_system_prompt: str = """"""
        
    def validate_request(self, request: ModelRequest) -> bool:
        return True
    
    def get_system_prompt(self) -> str:
        """
            根據 request 的內容動態生成 system prompt。
        """
        # 生成資料表資訊的提示
        table_info = self.request.state.get('table_info', [])
        table_info_list = [f"  - {table_name} \n {table_doc}" for table_info in table_info \
            for table_name, table_doc in table_info.items()]
        

        data_table_prompt = f"""
            {'\n'.join(table_info_list)}
        
            如果查詢的資訊為空，表示找不到資料，請返回查詢不到對應的資料。
        """
        
        # 生成使用者資訊的提示
        user_info_prompt = f"""
            - name: {self.request.state.get('name', None)}
            - email: {self.request.state.get('email', None)}
            - root_user: {self.request.state.get('root_user', None)}
            - department: {self.request.state.get('department', None)}
            - department_manager: {self.request.state.get('department_manager', None)}
        """
        
        # 生成 Agent 對應的資料表權限資訊
        agent_table_permission = self.request.state.get('table_agent_permission', [])
        agent_permission_table_list = [
            f" - {table_name}: {', '.join(permission_list)}" for table_obj in agent_table_permission for table_name, permission_list in table_obj.items()
        ]
        agent_table_permission_prompt = f"""
            {'\n'.join(agent_permission_table_list)}
        """
        
        # 生成最終的 system prompt
        system_prompt = f"""
        {self.agent_default_system_prompt}\n
        
        以下為登入的使用者資訊:\n
        {user_info_prompt}
        
        以下為資料表資訊:\n
        {data_table_prompt}
        
        以下對應的資料表使用權限資訊:\n
        {agent_table_permission_prompt}
        """
        return system_prompt

class LeaveWorkFlowSystemPrompt(CommonSystemPrompt):
    """
        請假流程專用的 system prompt，可以在這裡根據 request 的內容動態生成 system prompt。
    """
    def __init__(self, request: ModelRequest):
        super().__init__(request)
        self.agent_default_system_prompt = f"""
            你是一個能夠協助公司請假流程的智能助手, 負責處理請假流程的新增、更新和查詢, 當不知道的資訊可以透過現有的工具查詢, 不要隨便編造資訊, 你只能回答用戶要查找的資料表內容和處理有關請假流程的相關問題, 其他不相關一率回答這不是你涉及的能力範圍。
            請注意以下事項:
                1. 當你要透過執行工具要新增或更新的時候, 請跟使用者確認要跟新的內容之後再行動, 不要直接就執行工具, 以免資料被誤刪或是誤更新.
                2. 請不要透露資料庫的結構資訊給使用者, 也請不要把資料表欄位資訊以及關聯ID的資訊顯示給使用者, 只要回答使用者的問題及處理請假流程的相關資訊即可.
                3. 請給資料表的中文名就好, 不要給資料表的英文名, 也不要給資料表的欄位資訊, 只要回答使用者的問題及處理請假流程的相關資訊即可.
                4. 當申請請假紀錄或是更新請假紀錄時，必須要先檢核請假天數是否合法，若不合法則拒絕申請，並回覆使用者請假天數不合法的訊息，還有不能去申請其他使用者的請假紀錄。
                5. 當資料庫查找發生欄位錯誤時，請透過工具去查詢資料表的欄位資訊
        """

class UpdateTableInfoSystemPrompt(CommonSystemPrompt):
    """
        更新資料表專用的 system prompt，可以在這裡根據 request 的內容動態生成 system prompt。
    """
    def __init__(self, request: ModelRequest):
        super().__init__(request)
        self.agent_default_system_prompt = f"""
            你是一個更新資料庫的智能助手, 負責處理資料庫的資料建立、更新和查詢, 當不知道的資訊可以透過現有的工具查詢, 不要隨便編造資訊, 你只能回答和資料表內容和處理有關的相關問題, 其他不相關一率回答這不是你涉及的能力範圍。
            請注意以下事項:
                1. 當你要透過執行工具要新增或更新的時候, 請跟使用者確認要跟新的內容之後再行動, 不要直接就執行工具, 以免資料被誤刪或是誤更新。
                2. 如果使用者是人事部門相關, 請不要把資料表欄位資訊以及關聯ID的資訊顯示給使用者，請用欄位解釋的名稱來回答。
                3. 當資料庫查找發生欄位錯誤時，請透過工具去查詢資料表的欄位資訊
        """