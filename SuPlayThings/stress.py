import os, sys, time
from multiprocessing.dummy import Pool as ThreadPool

FILES_PER_FOLDER = 1000
ROOT_FOLDER = "folders"


def clear_folder():
    os.system("rm -rf {}".format(ROOT_FOLDER))
    os.system("mkdir {}".format(ROOT_FOLDER))


def get_folder_path(value):
    remainder = value % FILES_PER_FOLDER
    start = value - remainder
    end = start + FILES_PER_FOLDER - 1
    return "{}/{}_{}".format(ROOT_FOLDER, start, end)


def create_folders(count):
    for folder_id in range(0, count, FILES_PER_FOLDER):
        folder_path = get_folder_path(folder_id)
        command = "mkdir {}".format(folder_path)
        os.system(command)


def create_sub_folder(value):
    folder = value / FILES_PER_FOLDER
    command = "mkdir {}/{}".format(ROOT_FOLDER, str(folder))
    os.system(command)


def network_call(value):
    folder_path = get_folder_path(value)
    command = "wget http://100.26.188.62/audiobooks/{} -O {}/{}".format(
        str(value), folder_path, str(value))
    os.system(command)


args = sys.argv

if len(args) != 3:
    raise Exception("wrong argument")

count = int(args[1])
thread_pool_size = int(args[2])

if count < 1:
    raise Exception("count must >= 1")

if thread_pool_size < 1:
    raise Exception("thread_pool_size must >= 1")

clear_folder()
create_folders(count)

start = time.time()
pool = ThreadPool(thread_pool_size)
values = [val for val in range(count)]
pool.map(network_call, values)
end = time.time()
print("stress count = {}, thread pool size = {}, time used = {}".format(
    str(count), str(thread_pool_size), str(end - start)))

