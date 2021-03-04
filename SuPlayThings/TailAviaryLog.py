import os

TMP_FILE = "recent_log"
WORKSPACE_PATH = "workspaces/aviary"

cmd = """ls -ltr {}/src/DadetAviaryService/build/private/var/output/logs | grep "application.log" | tail -1 | grep -oE '[^ ]+$' > {}""".format(WORKSPACE_PATH, TMP_FILE)
os.system(cmd)

os.system("cat {}".format(TMP_FILE))

try:
    with open(TMP_FILE, 'r') as file:
        log_file = file.readline()
        print("log_file = " + log_file)
        cmd = """tail -f {}/src/DadetAviaryService/build/private/var/output/logs/{}""".format(WORKSPACE_PATH, log_file)
        print("tail command = " + cmd)
    os.system(cmd)
finally:
    os.system("rm {}".format(TMP_FILE))
