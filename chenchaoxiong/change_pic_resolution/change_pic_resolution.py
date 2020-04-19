#!/usr/bin/env python3

from glob import glob
from PIL import Image
import os

def file_dir(file_dir):   
    for root, dirs, files in os.walk(file_dir):
        for dir in dirs: 
                return dir
def main():
    img_dir = file_dir(os.getcwd())
    print(img_dir)
    #os.chdir(img_dir)
    pic_x = input("input picture x(like 1920):")
    pic_y = input("input picture y(like 1080):")
    img_path = glob(img_dir + "/*.jpg")
    path_save = "change_pic_" + pic_x + "_" + pic_y
    os.mkdir(path_save)
    for file in img_path:
        im = Image.open(file)
        out = im.resize((int(pic_x),int(pic_y)),Image.ANTIALIAS)
        pic = file.split('/')[1]
        name = os.path.join(path_save, pic)
        print(name)
        out.save(name)

if __name__ == "__main__":
    main()
