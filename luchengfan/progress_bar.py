#显示文本进度条
import time
scale = 50
print("执行开始".center(scale, "-"))#居中对齐
start = time.perf_counter()#获取起始时间
print('起始时间：{:.2f}s'.format(start))
for i in range(scale+1):
    a = i*'*'
    b = (scale-i)*'.'
    percentage = (i/scale)*100
    dur = time.perf_counter()#每次获取当前时间
    #输出百分比，图形进度以及当前所用的时间,控制end为空使得不用换行
    #\r让光标回退到当前行初始位置
    print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(percentage, a, b, dur), end='')
    time.sleep(0.1)
print('\n'+"结束执行".center(scale, '-'))