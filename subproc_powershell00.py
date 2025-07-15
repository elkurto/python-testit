import subprocess
import time
import os

"""
## sample output (on mac zsh)
% python3 subproc08ps.py
initial output ::: 

first command output ::: 
hello 1111

second command output ::: 
bar.txt
foo.txt
hello.py
subproc00.py
subproc01.py
subproc02.py
subproc03.py
subproc04.py
subproc05.py
subproc08ps.py

third command output ::: 
hello 3333

"""

def read_if_ouput_available( readable_streamlike, seconds_duration_sleep=1.0):
    """
        @param readable_streamlike - process.stdout or process.stderr 
          - a readable stream
        @param seconds_duration_sleep - float -
          - duration to sleep before attempting first read
          - default =1.0 (ie one second)
          - None or 0.0 means no sleep
    """
    # magic ingredient to prevent blocking
    os.set_blocking( readable_streamlike.fileno(), False) # magic ingredient

    # sleep
    if seconds_duration_sleep:
        f_seconds_duration_sleep =float(seconds_duration_sleep)
        time.sleep(f_seconds_duration_sleep)
    
    # collect and return available output (if any)
    output =''
    while True:
        data = readable_streamlike.readline()

        if len(data) > 0:
            output += data.strip() + "\n"
            continue
        else:
            break
    #end-while
    return output
#end-method 'read_if_ouput_available'

# Example commands for interactive shells
cmd_on_win10 =['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass']
cmd_on_mac   =['/bin/zsh', '-s']

interactive_subprocess =subprocess.Popen(
    cmd_on_win10, 
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True, # '\n' instead of random newline
    shell=True,  # run commands as current user # could be unsecure
    text=True # decodes stdin/stdout as text
    )

cmd_output =read_if_ouput_available( interactive_subprocess.stdout, 1.0)
print(f"initial output ::: \n{cmd_output}")

# send first command
# - trailing newline required 
os.write( interactive_subprocess.stdin.fileno(), 'echo "hello 1111"\n'.encode())
interactive_subprocess.stdin.flush() #ensure command is send to shell
cmd_output =read_if_ouput_available( interactive_subprocess.stdout, 1.0)
print(f"first command output ::: \n{cmd_output}")


# send second command
# - trailing newline required 
os.write( interactive_subprocess.stdin.fileno(), 'ls \n'.encode())
interactive_subprocess.stdin.flush() #ensure command is send to shell
cmd_output =read_if_ouput_available( interactive_subprocess.stdout, 1.0)
print(f"second command output ::: \n{cmd_output}")


# send third command
# - trailing newline required 
os.write( interactive_subprocess.stdin.fileno(), 'echo "hello 3333"\n'.encode())
interactive_subprocess.stdin.flush() #ensure command is send to shell
cmd_output =read_if_ouput_available( interactive_subprocess.stdout, 1.0)
print(f"third command output ::: \n{cmd_output}")

