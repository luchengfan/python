'''
功能描述：
1、根据图片显示其轮廓
2、图片的浮雕效果显示

补充：ImageFilter类中预定义了如下滤波方法：
• BLUR：模糊滤波
• CONTOUR：轮廓滤波
• DETAIL：细节滤波
• EDGE_ENHANCE：边界增强滤波
• EDGE_ENHANCE_MORE：边界增强滤波（程度更深）
• EMBOSS：浮雕滤波
• FIND_EDGES：寻找边界滤波
• SMOOTH：平滑滤波
• SMOOTH_MORE：平滑滤波（程度更深）
• SHARPEN：锐化滤波
• GaussianBlur(radius=2)：高斯模糊
可参考：https://www.jb51.net/article/181373.htm
'''
from PIL import Image,ImageFilter
import os

def main():
    while True:
        picture = input("请输入要处理的图片(输入N退出)：")
        if picture == "N" or picture == "n":
            return
        elif not os.path.exists(picture):
            print("您输入的图片不存在，" , end = "")
        else:
            break

    img = Image.open(picture)

    img_outline = img.filter(ImageFilter.CONTOUR)
    img_outline.save("轮廓效果.jpg" , "JPEG")

    img_relievo = img.filter(ImageFilter.EMBOSS)
    img_relievo.save("浮雕效果.jpg" , "JPEG")
    print("图片处理完成...")

if __name__ == "__main__":
    main()