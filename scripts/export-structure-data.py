from libs.variables import *
from libs.functions import *

tables_to_ignored = ['logs', 'devices_traited_data']
temp_file_path = "/root/exported_data"
data_save_path = save_path + "saves/"

if __name__ == "__main__":
    ssh = build_connect_return_ssh(ssh_key, ssh_host, ssh_username)
    create_my_cnf_file(ssh, ssh_db_username, ssh_db_password)
    export_data(ssh, tables_to_ignored, ssh_db_name, ssh_db_username, temp_file_path)
    zip_data(ssh, temp_file_path)
    download_data_zip(ssh, data_save_path)
    delete_ssh_tracks(ssh, temp_file_path)
    ssh.close()
    rename_data_save_file(data_save_path)
    print("Goodbye")
