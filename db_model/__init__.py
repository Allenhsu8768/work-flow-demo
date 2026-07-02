from db_model.department import export_model_class as department_export_model_class
from db_model.user import export_model_class as user_export_model_class
from db_model.leave import export_model_class as leave_export_model_class


model_register = {}
model_register.update(user_export_model_class)
model_register.update(department_export_model_class)
model_register.update(leave_export_model_class)
