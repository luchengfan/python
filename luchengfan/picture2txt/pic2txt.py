# coding:utf-8 
# 为一张图片生成对应的字符集图片 

from PIL import Image

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
#ascii_char = list('MW$#@%&KERTYOJKLUIC{}*mnxgouic()<>\!~:;^·.')

# 将256灰度映射到70个字符上，也就是RGB值转字符的函数：
def get_char(r , g , b , alpha = 256):
    if (alpha == 0):
        return ''
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)  # 计算灰度
    unit = (256.0 + 1)/length # 不同的灰度对应着不同的字符
    return ascii_char[int(gray/unit)]  # 通过灰度来区分色块

if __name__ == '__main__': 
    img = 'chenchaoxiong.jpg'
    im = Image.open(img)
    WIDTH = im.width
    HEIGHT = im.height
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ''

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i))) # 获得相应的字符
        txt += '\n'

# 字符画输出到文件
output_filename = img[:-4]+'.txt'
with open(output_filename, 'w') as f:
    f.write(txt)
print(img[:-4] + "制作完成，请查看文件" + output_filename)
