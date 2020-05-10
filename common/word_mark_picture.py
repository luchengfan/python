'''
功能描述：
1.字体文件在电脑的如下图标出的位置（C:\Windows\Fonts），选择自己想要的字体复制到项目文件。如：tahoma.ttf
2.在当前创建目录images，并且将需要添加水印的图片全部放进去。
3.添加水印后的图片会放在marked_images下，命名为原文件+__marked
'''
import os
from PIL import Image,ImageDraw,ImageFont

def watermark(filename,text,pic):
    # 实例化图片对象
    img = Image.open(filename)
    w, h = img.size  # 获取图片的宽、高,以便计算图片的相对位置
    print(pic+"图片高度：",h)
    print(pic+"图片宽度：",w)
    print("==========================================")
    # 设置字体、字体大小
    font = ImageFont.truetype("tahoma.ttf", int(w/50))  
    #创建一个可用来对image进行操作的对象。对所有即将使用ImageDraw中操作的图片都要先进行这个对象的创建。
    draw = ImageDraw.Draw(img)
    '''
     draw.text的四个参数设置:文字位置(横坐标，纵坐标)/内容/颜色/字体
     第一个参数调整文字插入的相对位置（屏幕坐标轴的方向如下）
                   →w
                  ↓
                   h
     '''
    draw.text((w/2,h/1.05), text=text, fill=(255, 255, 255), font=font)
    # 不存在如下文件夹则创建
    if not os.path.exists("marked_images"):
        os.mkdir("marked_images")
    save_name=pic.split(".")[0]+"_marked.jpg"#设置添加水印后的图片的名称
    img.save("./marked_images/"+save_name)

if __name__ == '__main__':
    text = input("pls enter the word you need!")
    director_path="./images/"#存放图片文件夹的路径
    pictures=os.listdir(director_path)#获取文件夹下的所有图片名称
    for pic in pictures:
        filename=director_path+pic#构造每张图片的路径名称
        watermark(filename,text,pic)#添加水印
    print("全部处理完毕")

