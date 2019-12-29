import time
import os
import re
import argparse
import subprocess
import locale

def get_locale_lang() ->str:
    ret_locale = list(locale.getdefaultlocale())
    if ret_locale[1] == 'cp950':
        return 'Big5'
    elif ret_locale[1] == 'cp1252':
        return 'utf8'
    else:
        return 'utf8'



def parse_last_volume_number(diskpart_message) -> int:
    new_diskpart_message = diskpart_message
    new_diskpart_message = new_diskpart_message.replace('磁碟區'       , 'Volume') # Taiwan
    new_diskpart_message = new_diskpart_message.replace('磁碟区'       , 'Volume') # China
    new_diskpart_message = new_diskpart_message.replace('양'           , 'Volume') # Korea
    new_diskpart_message = new_diskpart_message.replace('ボリューム'   , 'Volume') # Japan
    match = re.findall(r'Volume\s(\d)', new_diskpart_message)
    max_numb = 0
    if len(match) > 0:
        max_numb = match[len(match)-1]
    return max_numb

def diskpart_attach_vdisk(vhd_file_path:str) -> int:
    ret_locale_lang = get_locale_lang()
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ATTACH VDISK\n", 'utf-8'))
    res1 = p.stdin.write(bytes("LIST VOLUME\n", 'utf-8'))
    stdout, stderr = p.communicate()
    #output = stdout.decode('utf-8', errors='ignore')
    output = stdout.decode(ret_locale_lang, errors='ignore')
    last_volume_index = parse_last_volume_number(output)
    p.kill()
    return last_volume_index

def diskpart_mount_as_folder(last_volume_index:int, mount_point_path:str) -> bool:
    ret_locale_lang = get_locale_lang()
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ATTACH VDISK\n", 'utf-8'))
    res1 = p.stdin.write(bytes("SELECT VOLUME " + str(last_volume_index) + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ASSIGN MOUNT=" + mount_point_path + "\n", 'utf-8'))
    stdout, stderr = p.communicate()
    output = stdout.decode(ret_locale_lang, errors='ignore')
    #output = stdout.decode('utf-8', errors='ignore')
    print(output)

    p.kill()
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-source'   , help='aaaaaaaaaaaaaaaaaaaaaaa', required=True)
    parser.add_argument('-folder'   , help='aaaaaaaaaaaaaaaaaaaaaaa', dest='folder')
    parser.add_argument('-drive '   , help='aaaaaaaaaaaaaaaaaaaaaaa', dest='drive')
    parser.add_argument('-mount '   , help='aaaaaaaaaaaaaaaaaaaaaaa', dest='mount')
    parser.add_argument('-unmount ' , help='aaaaaaaaaaaaaaaaaaaaaaa', dest='unmount')

    #args = parser.parse_args()
    args = parser.parse_args()

    if None == args.source:
        exit(1)

    if not os.path.exists(args.source):
        exit(2)

    input_source = args.source.lower()
    if not input_source.endswith('.vhd') and not input_source.endswith('.vhdx'):
        exit(3)

    if not args.folder and  not args.drive:
        exit(4)

    # either, can't be both
    if args.folder and args.drive:
        exit(5)

    vhd_file_path = os.path.abspath(args.source)
    folder_path   = os.path.abspath(args.folder)
    last_volume_index = diskpart_attach_vdisk(vhd_file_path)

    print('VHD    = ' + str(vhd_file_path))
    print('Folder = ' + str(folder_path))
    print('Drive  = ' + str(args.drive))
    print('Volume = ' + str(last_volume_index))

    ret_status = False
    if args.folder:
        try:
            os.rmdir(folder_path)
        except:
            print("an exception")

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        ret_status = True

    elif args.drive:
        ret_status = False

    if ret_status:
        ret_status = diskpart_mount_as_folder(last_volume_index, folder_path)

    print(ret_status)
