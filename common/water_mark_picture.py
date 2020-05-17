'''
功能描述：
1.将水印文件放到当前目录下，命名为water.xxx,xxx为图片格式，这里不做更改，如：water.png
2.在当前创建目录images，并且将需要添加水印的图片全部放进去。
3.添加水印后的图片会放在marked_images下，命名为原文件+__marked
4.执行脚本：python3 water_mark_picture.py water.png
'''
import os
from PIL import Image,ImageDraw,ImageFont
import sys

def img_water_mark(img_file, wm_file, pic):
    img = Image.open(img_file)  # 打开图片
    watermark = Image.open(wm_file)  # 打开水印
    img_size = img.size
    wm_size = watermark.size
    # 如果图片大小小于水印大小
    if img_size[0] < wm_size[0]:
        watermark.resize(tuple(map(lambda x: int(x * 0.5), watermark.size)))
    print('图片大小：', img_size)
    wm_position = (img_size[0]-wm_size[0],img_size[1]-wm_size[1]) # 默认设定水印位置为右下角
    layer = Image.new('RGBA', img.size)  # 新建一个图层
    layer.paste(watermark, wm_position)  # 将水印图片添加到图层上
    mark_img = Image.composite(layer, img, layer)
    if not os.path.exists("marked_images"):
        os.mkdir("marked_images")
    save_name = pic.split(".")[0]+"_marked.jpg"
    mark_img.save("./marked_images/"+save_name)


if __name__ == '__main__':
    water_file = sys.argv[1]
    director_path="./images/"#存放图片文件夹的路径
    pictures=os.listdir(director_path)#获取文件夹下的所有图片名称
    for pic in pictures:
        filename=director_path+pic#构造每张图片的路径名称
        img_water_mark(filename,water_file,pic)#添加水印
    print("全部处理完毕")

