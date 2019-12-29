# py-vhdmount
This Python program can mount/unmount VHD or VHDX virtual image as a drive or a folder on Windows.

The main purpose of this project is helping testing jobs easier, I hate spending lots of time to do test repeatly manually.

## Usage
**Help**  
There is a `vhdfile-10mb.vhd` VHD image in the `vhdfile-10mb.zip` file. You need to unzip it first to the project root folder. Then try the following examples.

```cmd
python vhdmount.py -h
usage: vhdmount.py [-h] [-mount] [-unmount] -source SOURCE [-folder FOLDER] [-drive  DRIVE]

optional arguments:
  -h, --help      show this help message and exit
  -mount          mount a vhd image.
  -unmount        unmount a vhd image.
  -source SOURCE  vhd image file location
  -folder FOLDER  target mount point foler
  -drive  DRIVE   target mount disk letter

:: Mount a VHD image file as a folder(mount-point)
python vhdmount.py -mount -source vhdfile-10mb.vhd -folder mount-point

:: Unmount the folder or drive and detach the VHD image from system.
python vhdmount.py -unmount -source vhdfile-10mb.vhd
```

## LICENSE
MIT
