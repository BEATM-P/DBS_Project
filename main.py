# Import libraries
from db_conn import load_db_table
from config import get_project_root
# Project root
PROJECT_ROOT = get_project_root()
# Read database - PostgreSQL
df = load_db_table(config_db = 'database.ini', query = 'SELECT * FROM tablename LIMIT 5')
print(df)