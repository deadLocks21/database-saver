from libs.variables import *
from libs.functions import *
import paramiko, os, time
from math import ceil

MAX_LINES_IN_ONE_SAVE = 1000000

if __name__ == "__main__":
    start_total_time = time.time()
    ssh = build_connect_return_ssh(ssh_key, ssh_host, ssh_username)
    last_id = get_last_dtd_id(ssh, ssh_db_name, ssh_db_username, ssh_db_password)

    start_time = time.time()
    for i in range(ceil(int(last_id) / MAX_LINES_IN_ONE_SAVE)):
        min = i * MAX_LINES_IN_ONE_SAVE
        max = (i + 1) * MAX_LINES_IN_ONE_SAVE

        if max < last_id:
            export_dtd_min_max(ssh, min, max, ssh_db_name, ssh_db_username, ssh_db_password)
        else:
            export_dtd_min_max(ssh, min, last_id, ssh_db_name, ssh_db_username, ssh_db_password)
    print("--- %s seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    zip_data(ssh, '/tmp/db')
    print("--- %s seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    download_data_zip(ssh, save_path)
    print("--- %s seconds ---" % (time.time() - start_time))

    delete_ssh_tracks(ssh, '/tmp/db')
    ssh.close()
    unzip_force_save(save_path)
    delete_local_tracks(save_path)
    save_last_id_getted(last_id)
    print("Goodbye")

    print("--- %s seconds ---" % (time.time() - start_total_time))