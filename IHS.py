from osgeo import gdal, gdalconst
import numpy as np
import cv2
import os
from PIL import Image, ImageEnhance
def IHS(rgb,b8):
    low=gdal.Open(rgb)
    hight=gdal.Open(b8)
    hight_array=hight.ReadAsArray().astype(np.float32)# 数值化全色图像
    hight_x,hight_y=hight.RasterXSize,hight.RasterYSize#全色图像的维度
    R=low.GetRasterBand(1).ReadAsArray().astype(np.float)# 数值化多光谱R波段
    G=low.GetRasterBand(2).ReadAsArray().astype(np.float)# 数值化多光谱G波段
    B=low.GetRasterBand(3).ReadAsArray().astype(np.float)# 数值化多光谱B波段
    Rresize=cv2.resize(R,(hight_x,hight_y),interpolation=cv2.INTER_NEAREST)#将低分辨率的RGB影像重采样为全色波段的大小
    Gresize=cv2.resize(G,(hight_x,hight_y),interpolation=cv2.INTER_NEAREST)
    Bresize=cv2.resize(B,(hight_x,hight_y),interpolation=cv2.INTER_NEAREST)
    resample_RGB=np.array((Rresize,Gresize,Bresize)).astype(np.float32)#将重采样的多光谱影像整合为RGB
    reshapeR=Rresize.reshape(1,hight_x*hight_y)
    reshapeG=Gresize.reshape(1,hight_x*hight_y)
    reshapeB=Bresize.reshape(1,hight_x*hight_y)
    change=np.concatenate((reshapeR,reshapeG,reshapeB),axis=0)
    reshapeb8=hight_array.reshape(1,hight_x*hight_y)
    tran1 = np.array([[1/3,1/3,1/3],
            [-np.sqrt(2)/6,-np.sqrt(2)/6,2*np.sqrt(2)/6],
            [1/np.sqrt(2),-1/np.sqrt(2),0]])#正变换矩阵
    tran2= np.array([[1,-1/np.sqrt(2),1/np.sqrt(2)],
          [1,-1/np.sqrt(2),-1/np.sqrt(2)],
          [1,np.sqrt(2),0]])#逆变换矩阵
    #RGB--->IHS
    rgb2ihs=np.dot(tran1,change)
    rgb2ihs[0,:]=reshapeb8
    ihs2rgb=np.dot(tran2,rgb2ihs)
    p=np.zeros(((3,hight_x,hight_y)))
    p[0,:,:]=ihs2rgb[0].reshape((hight_x,hight_y))
    p[1,:,:]=ihs2rgb[1].reshape((hight_x,hight_y))
    p[2,:,:]=ihs2rgb[2].reshape((hight_x,hight_y))
    #p=np.uint8(p)
    img1 = cv2.merge([p[2],p[1],p[0]])

    cv2.imwrite(r"D:\CDUT\intership\experiment1\IHS.png", img1)
def main():
    original_rgb = r"D:\CDUT\intership\experiment1\sample\index.tif"
    original_b8 = r"D:\CDUT\intership\experiment1\sample\b8.tif"
    IHS(original_rgb,original_b8)
if __name__ == '__main__':
    main()
    