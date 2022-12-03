import numpy as np
import cv2 as cv
from Screenshot import capture
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT,HWND

def alone_matching(img,temp,mode=cv.TM_CCORR_NORMED):
    '''
    单个模板匹配并描绘矩阵
    :param image: 要进行匹配的图像对象
    :param template_fine: 模板对象(保留alpha)
    :return: 描绘完成后的图像
    '''
    if img.shape[:1] > temp.shape[:1]:
        temp = cv.cvtColor(temp, cv.COLOR_BGRA2GRAY)
        alpha = temp[:,:,2]
        gray = cv.cvtColor(img,cv.COLOR_BGRA2GRAY)
        h,w = temp.shape[:2]#接收模板行和列的数量
        match = cv.matchTemplate(gray,temp,mode,mask=alpha)
        min_val,max_val,min_loc,max_loc = cv.minMaxLoc(match)
        top_lest = max_loc
        bittom_right = (top_lest[0] + w, top_lest[1] + h)
        cv.rectangle(img,top_lest,bittom_right,(0,255,0),1)
        cv.imshow('alone',img)
        cv.waitKey()
        return img
    else:
        print('请检查传参顺序,重新传入')
        pass
    pass
def many_matching(img,temp,mode=cv.TM_CCOEFF_NORMED,threshold=0.7):
    '''
    多个对象匹配模板
    :param img: 要进行匹配的图像(png)
    :param temp:模板(保留Alpha,png格式,读取模式为-1)
    :param mode:匹配模式,默认为相关系数匹配法
    :param threshold:匹配程度阈值
    :return:完成矩阵绘画后的图形
    '''
    if img.shape[:1] > temp.shape[:1]:
        img = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
        alpha = temp[:, :, 2]  # 取出Alpha
        temp = cv.cvtColor(temp, cv.COLOR_BGRA2GRAY)
        img = cv.merge([img, img, img])
        gary = cv.cvtColor(img,cv.COLOR_BGRA2GRAY)#转换为灰色图
        w,h = temp.shape[::-1]#接收模板行和列的数量
        res = cv.matchTemplate(gary,temp,mode,mask=alpha)
        top_lest = np.where(res>=threshold)
        for pt in zip(*top_lest[::-1]):
            bittom_right = (pt[0]+ w, pt[1] + h)
            cv.rectangle(img,pt,bittom_right,(0,255,0),1)
            pass
        cv.imshow('many',img)
        cv.waitKey()
        return img
    else:
        print('请检查传参顺序,重新传入')
        pass
    pass


if __name__ == '__main__':
    handle = windll.user32.FindWindowW(None,"地下城与勇士登录程序")
    image = capture(handle)
    temaplate = cv.imread(r'D:\sparrow\kaishi.png',-1)
    cxk = cv.imread(r'F:\python_new\img\cxk.png',0)
    kun = cv.imread(r'F:\python_new\img\kuntou.png',0)
    # alone_matching(image,temaplate)
    max_img = cv.imread(r'D:\sparrow\png\gebulin.png')
    min_temap = cv.imread(r'D:\sparrow\png\2022-11\min_gbl.png',-1)
    zuo = cv.imread(r'D:\sparrow\png\2022-11\CZ6HkRTtNp.png')
    tubiao = cv.imread(r'D:\sparrow\png\2022-11\GzySzNN4GN.png',-1)
    many_matching(max_img,min_temap)








