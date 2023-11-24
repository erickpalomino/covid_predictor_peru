from src.models.data_manager import update_database
from src.models.database import setup_database,shutdown_database

setup_database()
update_database()
shutdown_database()