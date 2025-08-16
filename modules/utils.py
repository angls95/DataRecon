import os
from datetime import datetime

def separator(msg, target):
    if len(target) > 0:
        print("\n%s\n\n\t%s\n\tTarget: %s\n\n%s\n" % ('-'*50, msg, target, '-'*50))
    else:
        print("\n%s\n\n\t%s\n\n%s\n" % ('='*50, msg, '='*50))

def remove_repeted(unsorted_list):
    tmp = list()
    
    for i in unsorted_list:
        for j in i.splitlines():
            tmp.append(j)
    
    return sorted(set(tmp))

def get_dir_log():
    d_name = f"logs/{datetime.today().strftime('%Y-%m-%d')}"
    
    if not os.path.isdir(d_name):
        try:
            os.mkdir(d_name)
            print(f"\nDirectory '{d_name}' created successfully.")
        except Exception as e:
            print(f"[!] An error occurred: {e}")
    
    return d_name

def val_log_exists(f_path, f_log):
    file_path = f_path + f_log
    
    if not os.path.exists(file_path):
        return file_path
    else:
        count = 0
        s = file_path.split('_')
        while os.path.exists(file_path):
            if len(s[-1]) == 1:
                count = int(s[-1]) + 1
                file_path = f'{"_".join(s[:-1])}_{count}'
            else: 
                count += 1
                file_path = f'{"_".join(s)}_{count}'
        return file_path

def create_log_file(target, data, activitie):
    f_path = get_dir_log()
    f_log = val_log_exists(f_path, f"/{target}_{activitie}")
    
    with open(f_log, 'a') as log:
        log.write(data)
    
    print("\nThe information was stored in the log file '%s'" % f_log)