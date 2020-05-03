'''
功能描述：
1、遍历当前文件夹及其子目录的图片文件，支持的图片类型见:image_type_list
2、修改图片的分辨率，并在图片命名后加上分辨率，保存在当前目录的change_pic_XXX文件夹下
3、遍历文件夹以及文件夹子目录时会排除change_pic_XXX文件夹，目的是为了避免多次运行后会生成大量的图片
'''
from PIL import Image
from shutil import copyfile
import os

save_file_folder = "change_pic_"

def image_file(image_file_path):
    '''
    获取传参路径下的图片文件
    返回当前文件夹及其子目录下所有的图片文件(包括绝对路径)
    '''
    image_type_list = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
    image_list = []
    for root, dirs, files in os.walk(image_file_path):
        remove_save_path = "\\" + save_file_folder
        if remove_save_path not in root:#去出掉保存图片的文件夹
            for file in files:
                for image_type in image_type_list:
                    if file.endswith(image_type):
                        filename = root + "/" + file #注意不要改动"/"
                        image_list.append(filename)
    return image_list

def change_image_resolution(width, height):
    '''
    按照输入的高度和宽度修改图片
    '''
    save_path = save_file_folder + str(width) + "_" + str(height)
    image_file_list = image_file(os.getcwd())
    if image_file_list == []:
        print("当前目录及其子目录下无图片文件")
        return

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    try:
        for file in image_file_list:
            image = Image.open(file)
            #如果图片的分辨率同要转化的分辨率则拷贝，避免转化影响图片质量
            if image.width == width and image.height == height: 
                copy_file = os.path.join(save_path, file.split("/")[1])#注意不要改动"/"
                copyfile(file, copy_file)
            else:
                image_res = image.resize((width, height), Image.ANTIALIAS)
                image_name_old = file.split("/")[1] #注意不要改动"/"
                image_name_res = image_name_old.split(".")[0]+ "_"+ str(width)+ "_"+ str(height)+ "."+ image_name_old.split(".")[1]
                name = os.path.join(save_path, image_name_res)
                image_res.save(name)

        print("共处理了", len(image_file_list), "张图片")
        print("图片处理完成...")
    except Exception as e:
        print(e)

def main():
    width = 0
    height = 0
    
    while True:
        try:
            width,height = map(int,input("请输入图片的宽度和高度(默认是0,输入-1 -1退出),例如1920 1080：").split())
            if width == 0 or height == 0:
                print("您输入的宽度或者高度为0，请重新输入")
            elif width == -1 or height == -1:
                print("退出该程序...")
                return
            else:
                break
        except:
            print("您输入的数据不规范，请重新输入：")

    change_image_resolution(width, height)
    
if __name__ == "__main__":
    main()