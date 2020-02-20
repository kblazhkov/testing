import os
import re
import timeit
import subprocess

free_space = 1024000  # Kb free space
file_size = 102400  # Kb File size
file_num = 10  # Num of files

df = os.popen('df')
fs = df.read()
i = 1
create_file_time_all = 0.0
for line in fs.split("\n"):
    dev_list = line.split()
    if dev_list and dev_list[0][0:4] == "/dev" and int(dev_list[3]) >= free_space:
        file_dir = dev_list[5]
        while i <= file_num:
            try:
                create_file = subprocess.check_output(['dd', 'if=/dev/zero', 'of=' + file_dir + str(i) + '.txt', 'count=' + str(file_size), 'bs=1024'], stderr=subprocess.STDOUT)
                create_file_time = create_file.split()
                i += 1
                create_file_time_all = create_file_time_all + float(create_file_time[13].decode("utf-8"))
            except Exception as e:
                print(e)
        break
    else:
        print("No free space found")
print("Total time: " + str(create_file_time_all) + " s")
