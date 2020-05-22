'''
功能描述：
1.在当前创建目录images，并且将需要旋转的图片放入。
2.旋转后的图片会放在rotate_images下，明明为源文件+_rotate
3.运行脚本：python3 rotate_picture.py ，然后根据需求输入要求的角度,如45，-45，90，-90等等。
'''
import os
from PIL import Image,ImageDraw,ImageFont

def rotate_picture(filename,pic,rotate_pic):
    # 实例化图片对象
    img = Image.open(filename)
    # 不存在如下文件夹则创建
    if not os.path.exists("rotate_images"):
        os.mkdir("rotate_images")
    save_name=pic.split(".")[0]+"_rotate.jpg" #设置旋转后的图片名字
    img=img.rotate(int(rotate_pic))
    img.save("./rotate_images/"+save_name)
    print(pic+"旋转角度为：",rotate_pic)
    print("==========================================")
if __name__ == '__main__':
    rotate_pic = input("请输入你需要旋转的角度，如45，-45，90，-90：")
    director_path="./images/"#存放图片文件夹的路径
    pictures=os.listdir(director_path)#获取文件夹下的所有图片名称
    for pic in pictures:
        filename=director_path+pic#构造每张图片的路径名称
        rotate_picture(filename,pic,rotate_pic)#旋转图片
    print("全部处理完毕")

