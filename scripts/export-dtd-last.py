from libs.variables import *
from libs.functions import *
from os import system
from math import ceil

MAX_LINES_IN_ONE_SAVE = 1000000

if __name__ == "__main__":
    ssh = build_connect_return_ssh(ssh_key, ssh_host, ssh_username)
    last_id = get_last_dtd_id(ssh, ssh_db_name, ssh_db_username, ssh_db_password)
    last_id_getted = get_last_dtd_id_getted()

    if last_id > last_id_getted:
        if ceil(last_id_getted / MAX_LINES_IN_ONE_SAVE) * MAX_LINES_IN_ONE_SAVE < last_id:
            min_index = (ceil(last_id_getted / MAX_LINES_IN_ONE_SAVE) - 1)
            max_index = ceil(last_id / MAX_LINES_IN_ONE_SAVE)

            for i in range(max_index - min_index):
                min = (min_index + i) * MAX_LINES_IN_ONE_SAVE
                max = (min_index + i + 1) * MAX_LINES_IN_ONE_SAVE

                if max < last_id:
                    export_dtd_min_max(ssh, min, max, ssh_db_name, ssh_db_username, ssh_db_password)
                else:
                    export_dtd_min_max(ssh, min, last_id, ssh_db_name, ssh_db_username, ssh_db_password)
        else:
            min = (ceil(last_id_getted / MAX_LINES_IN_ONE_SAVE) - 1) * MAX_LINES_IN_ONE_SAVE
            export_dtd_min_max(ssh, min, last_id, ssh_db_name, ssh_db_username, ssh_db_password)

    
    zip_data(ssh, '/tmp/db')
    download_data_zip(ssh, save_path)
    delete_ssh_tracks(ssh, '/tmp/db')
    ssh.close()
    unzip_force_save(save_path)
    delete_local_tracks(save_path)
    save_last_id_getted(last_id)
    print("Goodbye")