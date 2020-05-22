'''
功能描述：
1.在当前创建目录images，并且将需要添加水印的图片全部放进去。
2.转换格式后的图片会放在convert_images下，明明为源文件+_convert
3.运行脚本：python3 convert_picture.py ，然后根据需求输入要求的格式,如png，jpg等等。
'''
import os
from PIL import Image,ImageDraw,ImageFont

def convert_picture(filename,pic,target_format):
    # 实例化图片对象
    img = Image.open(filename)
    img_format = img.format  # 获取图片的格式
    print(pic+"原来图片格式：",img_format)
    # 不存在如下文件夹则创建
    if not os.path.exists("convert_images"):
        os.mkdir("convert_images")
    save_name=pic.split(".")[0]+"_convert." + target_format#设置转化格式后的名字
    img.save("./convert_images/"+save_name)
    target_img = Image.open("./convert_images/"+save_name)
    target_img_format = target_img.format
    print(save_name+"转换后的图片格式："+target_img_format)
    print("==========================================")
if __name__ == '__main__':
    target_format = input("请输入你需要转换的目标格式，如jpg,png等等：")
    director_path="./images/"#存放图片文件夹的路径
    pictures=os.listdir(director_path)#获取文件夹下的所有图片名称
    for pic in pictures:
        filename=director_path+pic#构造每张图片的路径名称
        convert_picture(filename,pic,target_format)#添加水印
    print("全部处理完毕")

