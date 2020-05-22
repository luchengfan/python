from PIL import Image
import os
import numpy as np

def replace_color_tran(img, src_clr, dst_clr):
	''' 通过遍历颜色替换程序
	@param	img:	图像矩阵
	@param	src_clr:	需要替换的颜色(r,g,b)
	@param	dst_clr:	目标颜色		(r,g,b)
	@return				替换后的图像矩阵
	'''
	img_arr = np.asarray(img, dtype=np.double)
	
	dst_arr = img_arr.copy()
	for i in range(img_arr.shape[1]):	
		for j in range(img_arr.shape[0]):
			if (img_arr[j][i] == src_clr)[0] == True:
				dst_arr[j][i] = dst_clr
		
	return np.asarray(dst_arr, dtype=np.uint8)

def main():
    img = '1.jpg'
    img = Image.open(img).convert('RGB')

    dst_img = replace_color_tran(img, (254,0,0), (255,255,255))
    res_img = dst_img
    res_img = Image.fromarray(res_img)
    res_img.save('2.jpg')

if __name__ == "__main__":
    main()
