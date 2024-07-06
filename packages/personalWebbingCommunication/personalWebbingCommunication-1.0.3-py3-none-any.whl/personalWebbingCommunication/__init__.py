from log_data import custom_logger
webcom_log = custom_logger()
webcom_log.initialise_database()
print("here:",webcom_log.backup_notion_page_id)
from .multipart import *
from .test import *