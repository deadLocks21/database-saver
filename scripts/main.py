import paramiko, os, dotenv
from datetime import datetime

dotenv.load_dotenv()

## SSH params
ssh_key = os.getenv('SSH_KEY_PATH')
ssh_host = os.getenv('SSH_HOST')
ssh_username = os.getenv('SSH_USERNAME')

## Distant db params
ssh_db_name = os.getenv('SSH_DB_NAME')
ssh_db_username = os.getenv('SSH_DB_USERNAME')
ssh_db_password = os.getenv('SSH_DB_PASSWORD')
ssh_db_data_to_ignore = f"--ignore-table={ssh_db_name}.devices_traited_data --ignore-table={ssh_db_name}.logs"

save_path = os.getenv('SAVE_PATH')
tables_to_ignored = ['logs', 'devices_traited_data']
temp_file_path = "/root/exported_data"

if __name__ == "__main__":
    k = paramiko.RSAKey.from_private_key_file(ssh_key)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ssh_host, username=ssh_username, pkey=k)
    print("Connected")

    ssh.exec_command(f"""echo '[mysqldump]
    user={ssh_db_username}
    password={ssh_db_password}' > .my.cnf""")

    with ssh.exec_command(f'mysqlshow db_quatrefactorielle')[1] as stdout:
        tables = stdout.readlines()[4:]
        tables.pop()

    # Exports table data.
    for table in tables:
        table = table.replace('|', '').strip()
        if table not in tables_to_ignored:
            ssh.exec_command(
                f'mysqldump --defaults-file="/root/.my.cnf" -u {ssh_db_username} --no-create-info {ssh_db_name} {table} > "{temp_file_path}/{table}.sql"')
    # ssh.exec_command(f'mysqldump --defaults-file="/root/.my.cnf" -u {ssh_db_username} --no-data {ssh_db_name} --ignore-table={ssh_db_name}.devices_traited_data --ignore-table={ssh_db_name}.logs > "{temp_file_path}/structure.sql"')
    ssh.exec_command(
        f'mysqldump --defaults-file=/root/.my.cnf -u {ssh_db_username} --no-data {ssh_db_name} > structure.sql')
    print("Retrieved")

    with ssh.exec_command(f"zip data.zip /root/exported_data/*")[1] as stdout:
        a = stdout.readlines()
        print("Zipped")

    sftp = ssh.open_sftp()
    sftp.get("/root/data.zip", f"{save_path}data.zip")
    sftp.close()
    print("Repatriated")

    ssh.exec_command("rm .my.cnf")
    ssh.exec_command("rm data.sql")
    ssh.exec_command("rm data.zip")
    print("Deleted tracks")

    ssh.close()

    os.rename(f'{save_path}data.zip', f'{save_path}{datetime.today().strftime("%Y-%m-%d %H:%M")}.zip')
    print("Renamed")

    print("Goodbye")
