#!/usr/bin/env python

import os
import sys

try:
    import ansible
except:
    print("Ansible is not installed")
    sys.exit(1)

ansible_path = ansible.__path__[0]
module_utils = ansible_path + '/module_utils/'
extras_path = ansible_path + '/modules/extras'
server_path = extras_path + '/server'
ucs_path = server_path + '/cisco'


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

#Let's make this recursive.
#Base Case #1 - In Empty Folder
#Base Case #2 - Has Only Files

#Next Step #1 - Has Only Folders
#Next Step #2 - Has Folders and Files
def copy_files(src, dest):
    import shutil
    
    src_ls = os.listdir(src)
    #The base case 1 is handled with a for loop
    #Because an empty dir returns []
    for ls_item in src_ls:
        src_file = os.path.join(src, ls_item)
        dst_file = os.path.join(dest, ls_item)
        if os.path.isfile(src_file):
            print(src_file, "===>", dst_file)
            
            shutil.copy(src_file, dst_file)
        elif os.path.isdir(src_file):
            os.makedirs(dst_file)
            copy_files(src_file, dst_file)


# Create the directory for the main module under extras/server/cisco repo
if not os.path.isdir(ucs_path):
    os.makedirs(ucs_path)
touch(server_path + '/__init__.py')
touch(ucs_path + '/__init__.py')

# Copy files from library folder to ucs_path
copy_files(os.getcwd() + '/library', ucs_path)

# Copy common files to module_util
copy_files(os.getcwd() + '/utils', module_utils)



