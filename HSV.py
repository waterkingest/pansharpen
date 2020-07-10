from osgeo import gdal, gdalconst
import numpy as np
import cv2
import os
from PIL import Image, ImageEnhance
def HSV(rgb,b8):
    #用gdal打开遥感图像
    low=gdal.Open(rgb)
    hight=gdal.Open(b8)
    hight_array=hight.ReadAsArray().astype(np.float32)# 数值化全色图像
    hight_x,hight_y=hight.RasterXSize,hight.RasterYSize#获取全色图像的维度
    R=low.GetRasterBand(1).ReadAsArray().astype(np.float)# 数值化多光谱R波段
    G=low.GetRasterBand(2).ReadAsArray().astype(np.float)# 数值化多光谱G波段
    B=low.GetRasterBand(3).ReadAsArray().astype(np.float)# 数值化多光谱B波段
    Rresize=cv2.resize(R,(hight_x,hight_y),interpolation=cv2.INTER_NEAREST)#将低分辨率的RGB影像重采样为全色波段的大小
    Gresize=cv2.resize(G,(hight_x,hight_y),interpolation=cv2.INTER_NEAREST)
    Bresize=cv2.resize(B,(hight_x,hight_y),interpolation=cv2.INTER_NEAREST)
    resample_RGB=np.array((Rresize,Gresize,Bresize)).astype(np.float32)#将重采样的多光谱影像整合为RGB
    resample_img=cv2.merge([resample_RGB[0,:,:],resample_RGB[1,:,:],resample_RGB[2,:,:]]) 
    resample_img_hsv=cv2.cvtColor(resample_img, cv2.COLOR_RGB2HSV)#使用opencv将色彩空间RGB转为HSV
    HSVimg=cv2.merge([resample_img_hsv[:,:,0],resample_img_hsv[:,:,1],hight_array])#将多光谱的V用全色影像代替
    RGBimg=cv2.cvtColor(HSVimg, cv2.COLOR_HSV2BGR)#整合为OpenCV中默认的BGR形式
    cv2.imwrite(r"D:\CDUT\intership\experiment1\hsv2.png", RGBimg)
def main():
    original_rgb =  r"D:\CDUT\intership\experiment1\sample\index.tif"
    original_b8 = r"D:\CDUT\intership\experiment1\sample\b8.tif"
    HSV(original_rgb,original_b8)
if __name__ == '__main__':
    main()