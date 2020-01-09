import time
import os
import re
import argparse
import subprocess
import locale

g_DebugEnabled=False

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

def diskpart_attach_vdisk(vhd_file_path:str, readonly:bool=False) -> int:
    ret_locale_lang = get_locale_lang()
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
    
    if readonly:
        res1 = p.stdin.write(bytes("ATTACH VDISK READONLY\n", 'utf-8'))
    else:
        res1 = p.stdin.write(bytes("ATTACH VDISK\n", 'utf-8'))
        
    res1 = p.stdin.write(bytes("LIST VOLUME\n", 'utf-8'))
    stdout, stderr = p.communicate()
    output = stdout.decode(ret_locale_lang, errors='ignore')
    last_volume_index = parse_last_volume_number(output)
    
    if g_DebugEnabled:
        print(output)

    p.kill()
    return last_volume_index

def diskpart_unmount(vhd_file_path:str, last_volume_index:int) -> bool:
    print('running for unmount ...')

    ret_locale_lang = get_locale_lang()
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VOLUME " + str(last_volume_index) + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("REMOVE ALL DISMOUNT\n", 'utf-8'))

    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("DETACH VDISK\n", 'utf-8'))

    stdout, stderr = p.communicate()
    output = stdout.decode(ret_locale_lang, errors='ignore')
    
    if g_DebugEnabled:
        print(output)

    p.kill()
    return True

def diskpart_mount_as_folder(last_volume_index:int, mount_point_path:str, readonly:bool=False) -> bool:
    print('running for mount ...')
    ret_locale_lang = get_locale_lang()
    p = subprocess.Popen("diskpart", stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=os.environ, )
    res1 = p.stdin.write(bytes("SELECT VDISK FILE=" + vhd_file_path + "\n", 'utf-8'))
        
    if readonly:
        res1 = p.stdin.write(bytes("ATTACH VDISK READONLY\n", 'utf-8'))
    else:
        res1 = p.stdin.write(bytes("ATTACH VDISK\n", 'utf-8'))
    
    res1 = p.stdin.write(bytes("SELECT VOLUME " + str(last_volume_index) + "\n", 'utf-8'))
    res1 = p.stdin.write(bytes("REMOVE ALL DISMOUNT\n", 'utf-8'))
    res1 = p.stdin.write(bytes("ASSIGN MOUNT=" + mount_point_path + "\n", 'utf-8'))
    stdout, stderr = p.communicate()
    output = stdout.decode(ret_locale_lang, errors='ignore')
    
    if g_DebugEnabled:
        print(output)

    p.kill()
    return True


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m'    , '-mount'    , help='mount a vhd image.'         , dest='mount'      , action='store_true')
    parser.add_argument('-u'    , '-unmount'  , help='unmount a vhd image.'       , dest='unmount'    , action='store_true')
    parser.add_argument('-dbg'  , '-debug'    , help='Enable debugging message.'  , dest='debug'      , action='store_true')
    parser.add_argument('-r'    , '-readonly' , help='Mount as readonly.'         , dest='readonly'   , action='store_true')
    parser.add_argument('-s'    , '-source'   , help='vhd image file location'    , dest='source'     , required='True'  )
    parser.add_argument('-f'    , '-folder'   , help='target mount point foler'   , dest='folder')
    parser.add_argument('-d'    , '-drive '   , help='target mount disk letter'   , dest='drive')

    
    args = parser.parse_args()
    g_DebugEnabled = args.debug

    if None == args.source:
        print('ERROR: missed -source.')
        exit(1)

    if not os.path.exists(args.source):
        print('ERROR: source fail not found.')
        exit(2)

    input_source = args.source.lower()
    if not input_source.endswith('.vhd') and not input_source.endswith('.vhdx'):
        print('ERROR: input source file extension name is not .vhd or .vhdx.')
        exit(3)

    if not args.mount and not args.unmount:
        print('ERROR: missed -mount or -unmount.')
        exit(4)

    folder_path = ''
    if args.mount:
        if not args.folder and  not args.drive:
            print('ERROR: missed -folder or -drive.')
            exit(5)

        # either, can't be both
        if args.folder and args.drive:
            print('ERROR: either -folder or -drive at the same time.')
            exit(6)


        folder_path = os.path.abspath(args.folder)

    vhd_file_path = os.path.abspath(args.source)
    last_volume_index = diskpart_attach_vdisk(vhd_file_path, args.readonly)

    print('Mount    = ' + str(args.mount))
    print('Unmount  = ' + str(args.unmount))
    print('VHD      = ' + str(vhd_file_path))
    print('Folder   = ' + str(folder_path))
    print('Drive    = ' + str(args.drive))
    print('Volume   = ' + str(last_volume_index))
    print('Debug    = ' + str(args.debug))
    print('ReadOnly = ' + str(args.readonly))

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

    elif args.unmount:
        ret_status = True

    if ret_status:
        if args.mount:
            if args.folder:
                ret_status = diskpart_mount_as_folder(last_volume_index, folder_path, args.readonly)
            elif args.disk:
                print('-drive option is supported now.')
        elif args.unmount:
            ret_status = diskpart_unmount(vhd_file_path, last_volume_index)

    print('Result  = ' + str(ret_status))
