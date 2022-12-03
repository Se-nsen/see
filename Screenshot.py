from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT,HWND
import numpy as np
from time import sleep,perf_counter
from os import startfile
import cv2 as cv

# 排除缩放干扰
windll.user32.SetProcessDPIAware()

def capture(handle:HWND):#窗口句柄
    """窗口客户区截图

    Args:
        handle (HWND): 要截图的窗口句柄

    Returns:
        numpy.ndarray: 截图数据
    """
    GetDC = windll.user32.GetDC  # 返回指定窗口显示设备描述表的句柄
    CreateCompatibleDC = windll.gdi32.CreateCompatibleDC  # 创建一个与特定设备场景一致的内存设备场景
    GetClientRect = windll.user32.GetClientRect  # 返回用户区域的坐标
    CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap  # 创建一幅与设备有关位图，它与指定的设备场景兼容
    SelectObject = windll.gdi32.SelectObject  # 为当前设备场景选择图形对象
    BitBlt = windll.gdi32.BitBlt  # 将一幅位图从一个设备场景复制到另一个
    SRCCOPY = 0x00CC0020
    GetBitmapBits = windll.gdi32.GetBitmapBits  # 将来自位图的二进制位复制到一个缓冲区
    DeleteObject = windll.gdi32.DeleteObject  # 删除GDI对象，对象使用的所有系统资源都会被释放
    ReleaseDC = windll.user32.ReleaseDC  # 释放指定的设备描述表

    # 获取窗口客户区的大小
    r = RECT()   #结构按其左上角和右下角的坐标定义矩形
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    # 开始截图
    dc = GetDC(handle)#检查DC窗口句柄
    cdc = CreateCompatibleDC(dc)#创建与指定设备兼容的内存设备上下文
    bitmap = CreateCompatibleBitmap(dc, width, height)#函数创建与与指定设备上下文关联的设备的位图
    SelectObject(cdc, bitmap)#函数将对象选择到指定的设备上下文中(DC) 新对象替换同一类型的上一个对象
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)#执行与从指定源设备上下文到目标设备上下文中的像素矩形对应的颜色数据的位块传输
    # 截图是BGRA排列，因此总元素个数需要乘以4
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)#返回一个新字节数组
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    # 返回截图数据为numpy.ndarray
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)



if __name__ == "__main__":
    start = perf_counter()
    startfile(r"E:\dnf\地下城与勇士\TCLS\Client.exe")
    sleep(8)
    end = perf_counter()
    print('打开程序用时:',end - start,'(秒)','包含等待时长8秒')

    handle = windll.user32.FindWindowW(None, "地下城与勇士登录程序")
    image = capture(handle)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)#转为灰度图
    template = cv.imread(r'D:\sparrow\kaishi.png',0)
    h,w = template.shape[:2]
    res = cv.matchTemplate(gray,template,cv.TM_CCORR_NORMED)
    min_val,max_val,min_loc,max_loc = cv.minMaxLoc(res)
    top_lest = max_loc
    bottom_right = (top_lest[0]+w,top_lest[1]+h)
    cv.rectangle(image,top_lest,bottom_right,(0,0,255),2)
    cv.imshow('Match Template', image)
    cv.waitKey()