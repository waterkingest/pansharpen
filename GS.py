from osgeo import gdal, gdalconst
import numpy as np
import cv2
import os
from PIL import Image, ImageEnhance
def GS(rgb,b8):
    low=gdal.Open(rgb)
    hight=gdal.Open(b8)
    hight_array=hight.ReadAsArray().astype(np.float32)# 数值化全色图像
    hight_x,hight_y=hight.RasterXSize,hight.RasterYSize#全色图像的维度
    R=low.GetRasterBand(1).ReadAsArray().astype(np.float)# 数值化多光谱R波段
    G=low.GetRasterBand(2).ReadAsArray().astype(np.float)# 数值化多光谱G波段
    B=low.GetRasterBand(3).ReadAsArray().astype(np.float)# 数值化多光谱B波段
    Rresize=cv2.resize(R,(hight_x,hight_y),interpolation=cv2.INTER_LINEAR)#将低分辨率的RGB影像重采样为全色波段的大小
    Gresize=cv2.resize(G,(hight_x,hight_y),interpolation=cv2.INTER_LINEAR)
    Bresize=cv2.resize(B,(hight_x,hight_y),interpolation=cv2.INTER_LINEAR)
    resample_RGB=np.array((Rresize,Gresize,Bresize)).astype(np.float32)#将重采样的多光谱影像整合为RGB
    resample_RGB=cv2.merge([Rresize,Gresize,Bresize])
    means = np.mean(resample_RGB, axis=(0, 1))
    image_lr = resample_RGB-means   
    #sintetic intensity
    I = np.mean(resample_RGB, axis=2, keepdims=True)
    I0 = I-np.mean(I)  
    image_hr = (hight_array-np.mean(hight_array))*(np.std(I0, ddof=1)/np.std(hight_array, ddof=1))+np.mean(I0)
    image_hr=np.reshape(image_hr,[hight_x,hight_y,1])
    #computing coefficients
    g = []
    g.append(1)  
    for i in range(3):
        temp_h = image_lr[:, :, i]
        c = np.cov(np.reshape(I0, (-1,)), np.reshape(temp_h, (-1,)), ddof=1)
        g.append(c[0,1]/np.var(I0))
    g = np.array(g)
    print(I0.shape)
    #detail extraction
    delta = image_hr-I0
    
    deltam = np.tile(delta, (1, 1, 3+1))  
    #fusion
    V = np.concatenate((I0, image_lr), axis=-1)
    g = np.expand_dims(g, 0)
    g = np.expand_dims(g, 0) 
    g = np.tile(g, (hight_x, hight_y, 1))
    V_hat = V+ g*deltam
    I_GS = V_hat[:, :, 1:]
    I_GS = I_GS - np.mean(I_GS, axis=(0, 1))+means
    #adjustment
    change_rgb=I_GS#np.uint8(I_GS)
    print(change_rgb.shape)
    img1 = cv2.merge([change_rgb[:,:,2],change_rgb[:,:,1],change_rgb[:,:,0]])
    print(img1)
    #img=Image.fromarray(img1)
    #enhance = image_enhance(img, 1, 1.5) #调用类
    #img_light = enhance.image_brightened()
    #img.show()
   #img.save(r"D:\CDUT\intership\experiment1\GS.png","png")
    cv2.imwrite(r"D:\CDUT\intership\experiment1\GS.png", img1)
def main():
    original_rgb = r"D:\CDUT\intership\experiment1\sample\index.tif"
    original_b8 = r"D:\CDUT\intership\experiment1\sample\b8.tif"
    GS(original_rgb,original_b8)
if __name__ == '__main__':
    main()