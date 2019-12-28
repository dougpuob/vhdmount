import time
import os
import re
import subprocess
from pathlib import Path


text = b'''
hello world
this is a test
goodbye
'''

def parse_last_volume_number(diskpart_message) -> int:
    match = re.findall(r'Volume\s(\d)', diskpart_message)
    max_numb = 0
    if len(match) > 0:
        max_numb = match[len(match)-1]
    return max_numb

def diskpart_attach_vdisk(vhd_file_path:str) -> int:
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ATTACH VDISK\n", 'utf-8'))
    res1 = p.stdin.write(bytes("LIST VOLUME\n", 'utf-8'))
    stdout, stderr = p.communicate(text)
    output = stdout.decode('utf-8')
    last_volume_index = parse_last_volume_number(output)
    p.kill()
    return last_volume_index

def diskpart_mount_as_folder(last_volume_index:int, mount_point_path:str) -> bool:
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ATTACH VDISK\n", 'utf-8'))
    res1 = p.stdin.write(bytes("SELECT VOLUME " + last_volume_index + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ASSIGN MOUNT=" + mount_point_path + "\n", 'utf-8'))
    stdout, stderr = p.communicate()
    output = stdout.decode('utf-8')
    print(output)

    p.kill()
    return True


if __name__ == '__main__':
    curr_path = os.path.dirname(os.path.abspath(__file__))
    vhd_file_path = os.path.join(curr_path, "sample.vhd")
    mount_point_folder_path = os.path.join(curr_path, "mount-point")

    try:
        os.rmdir(mount_point_folder_path)
    except:
        print("an exception")

    if not os.path.exists(mount_point_folder_path):
        os.mkdir(mount_point_folder_path)

    if os.path.exists(vhd_file_path):
        last_volume_index = diskpart_attach_vdisk(vhd_file_path)
        time.sleep(.5)
        result = diskpart_mount_as_folder(last_volume_index, mount_point_folder_path)
        print(result)