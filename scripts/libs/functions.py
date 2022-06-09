from paramiko import RSAKey, SSHClient, AutoAddPolicy
from datetime import datetime
from os import rename, system
from json import loads
from math import ceil

def build_connect_return_ssh(ssh_key, ssh_host, ssh_username):
    """Build, connect and return a paramiko.SSHClient object"""
    k = RSAKey.from_private_key_file(ssh_key)
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(hostname=ssh_host, username=ssh_username, pkey=k)
    print("Connected")
    return ssh

def create_my_cnf_file(ssh, db_user, db_pass):
    ssh.exec_command(f"""echo '[mysqldump]
    user={db_user}
    password={db_pass}' > .my.cnf""")

def get_tables(ssh, db_database):
    tables = []
    with ssh.exec_command(f'mysqlshow {db_database}')[1] as stdout:
        tables_unformated = stdout.readlines()[4:]
        tables_unformated.pop()
        for table in tables_unformated:
            tables.append(table.replace('|', '').strip())
    return tables

def get_last_dtd_id(ssh, db_name, db_user, db_password):
    with ssh.exec_command(f'mysql -u {db_user} --password={db_password} {db_name} -e "SELECT id_devices_traited_data FROM devices_traited_data ORDER BY id_devices_traited_data DESC LIMIT 1;"')[1] as stdout:
        last_id = int(stdout.readlines()[1].replace('\n', ''))
    print(f"Last id in devices_traited_data table is {last_id}")
    return last_id

def get_last_dtd_id_getted():
    with open('/last_id_getted.json', 'r') as save_file:
        last_id_getted = loads(save_file.read())['last_id_getted']
    print(f"Last saved id is {last_id_getted}")
    return last_id_getted

def export_data(ssh, to_ignore, db_database, db_user, temp_path):
    for table in get_tables(ssh, db_database):
        if table not in to_ignore:
            ssh.exec_command(
                f'mysqldump --defaults-file="/root/.my.cnf" -u {db_user} --no-create-info {db_database} {table} > "{temp_path}/{table}.sql"')
    ssh.exec_command(f'mysqldump --defaults-file=/root/.my.cnf -u {db_user} --no-data {db_database} > {temp_path}/structure.sql')
    print("Retrieved")

def export_dtd_min_max(ssh, min, max, db_database, db_user, db_password):
    with ssh.exec_command(f"""mysql -u {db_user} --password={db_password} {db_database} -e "SELECT * FROM devices_traited_data WHERE {min} < id_devices_traited_data AND id_devices_traited_data <= {max} INTO OUTFILE '/tmp/db/devices_traited_data_{"{0:02d}".format(int(min / 1000000))}_{"{0:02d}".format(int(ceil(max / 1000000)))}.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\\"' LINES TERMINATED BY '\\n';" """)[1] as stdout:
        a = stdout.readlines()
    print(f'Export rows between {min} and {max}')

def zip_data(ssh, temp_path):
    with ssh.exec_command(f"zip -j data.zip {temp_path}/*")[1] as stdout:
        a = stdout.readlines()
        print("Zipped")

def download_data_zip(ssh, save_path):
    sftp = ssh.open_sftp()
    sftp.get("/root/data.zip", f"{save_path}data.zip")
    sftp.close()
    print("Repatriated")

def unzip_force_save(save_path):
    system(f'unzip -o {save_path}/data.zip -d {save_path}/exported_data/')
    print("Unziped")

def delete_ssh_tracks(ssh, temp_path):
    ssh.exec_command("rm .my.cnf")
    ssh.exec_command(f"rm {temp_path}/*")
    ssh.exec_command("rm data.zip")
    print("Deleted tracks")

def delete_local_tracks(save_path):
    system(f'rm {save_path}/data.zip')
    print("Deleted local tracks")

def rename_data_save_file(save_path):
    rename(f'{save_path}data.zip', f'{save_path}{datetime.today().strftime("%Y-%m-%d %H:%M")}.zip')
    print("Renamed")

def save_last_id_getted(last_id):
    with open('last_id_getted.json', 'w+') as save_file:
        save_file.write(f'{{ "last_id_getted": {last_id} }}')
    print("Last id getted saved")