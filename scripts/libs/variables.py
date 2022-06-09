from dotenv import load_dotenv
from os import getenv

load_dotenv()

## SSH params
ssh_key = getenv('SSH_KEY_PATH')
ssh_host = getenv('SSH_HOST')
ssh_username = getenv('SSH_USERNAME')

## Distant db params
ssh_db_name = getenv('SSH_DB_NAME')
ssh_db_username = getenv('SSH_DB_USERNAME')
ssh_db_password = getenv('SSH_DB_PASSWORD')

save_path = getenv('SAVE_PATH')