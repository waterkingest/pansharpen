from osgeo import gdal, gdalconst
import numpy as np
import cv2
import os
from PIL import Image, ImageEnhance

def result_to_image(img):#转换格式
    img = np.array(img)
    max_val, min_val = np.nanmax(img), np.nanmin(img)
    print(max_val, min_val)
    out = (img.astype(np.float) - min_val) / (max_val - min_val)#将像素值换成0~1的值
    out = out*255   #乘以255，像素值换成颜色值
    out = np.uint8(out)#utf-8编码格式转换
    return out
def PCA(rgb,b8):
    low=gdal.Open(rgb)
    hight=gdal.Open(b8)
    hight_array=hight.ReadAsArray().astype(np.float32)# 数值化全色图像
    hight_x,hight_y=hight.RasterXSize,hight.RasterYSize#全色图像的维度
    R=low.GetRasterBand(1).ReadAsArray().astype(np.float32)# 数值化多光谱R波段
    G=low.GetRasterBand(2).ReadAsArray().astype(np.float32)# 数值化多光谱G波段
    B=low.GetRasterBand(3).ReadAsArray().astype(np.float32)# 数值化多光谱B波段
    Rresize=cv2.resize(R,(hight_x,hight_y),interpolation=cv2.INTER_LINEAR)#将低分辨率的RGB影像重采样为全色波段的大小
    Gresize=cv2.resize(G,(hight_x,hight_y),interpolation=cv2.INTER_LINEAR)
    Bresize=cv2.resize(B,(hight_x,hight_y),interpolation=cv2.INTER_LINEAR)
    resample_RGB=np.array((Rresize,Gresize,Bresize)).astype(np.float32)#将重采样的多光谱影像整合为RGB
    RGB_resample = resample_RGB.reshape((hight_x*hight_y, 3)) 
    b8 = hight_array.reshape((hight_x*hight_y, 1))
    RGB_resample_mean = np.mean(RGB_resample, 0) # 按照第一维度(也就是括号里的0)求和，结果维度为（3，1）
    RgbReduceMean = RGB_resample - np.tile(RGB_resample_mean, (hight_x*hight_y, 1))#去均值
    covar = (np.matrix(RgbReduceMean).T * np.matrix(RgbReduceMean)) / (hight_x*hight_y)#求协方差
    value, vector = np.linalg.eig(covar)  # 求特征向量
    vector = np.fliplr(vector)  # 左右对调特征向量
    rgb2pc = np.array(np.matrix(RGB_resample) * np.matrix(vector))  # PCA正变换 
    rgb2pc[:][0] = b8[:][0]#第一主分量用全色波段代替
    RGB_resample = np.array(np.matrix(rgb2pc) * np.linalg.inv(vector)).reshape(3,hight_y, hight_x)#pca逆变换并转换为三维矩阵
    result = np.uint8(RGB_resample)
    img1 = cv2.merge([result[0][:][:],result[1][:][:],result[2][:][:]])
    img=Image.fromarray(img1)   
    img_light=img
    img_light.show()
    img_light.save(r"D:\CDUT\intership\experiment1\PCA.png","png")
    #cv2.imwrite(r"D:\CDUT\intership\experiment1\PCA2.png", img1)
def main():
    original_rgb = r"D:\CDUT\intership\experiment1\sample\index.tif"
    original_b8 = r"D:\CDUT\intership\experiment1\sample\b8.tif"
    PCA(original_rgb,original_b8)
if __name__ == '__main__':
    main()
    