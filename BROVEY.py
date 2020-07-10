from osgeo import gdal, gdalconst
import numpy as np
import cv2
import os
from PIL import Image, ImageEnhance
class image_enhance():
    """
    图像增强类：包括亮度和对比度
    """
    def __init__(self, img, brightness, contrast):
        self.img = img
        self.brightness = brightness
        self.contrast = contrast
    def image_brightened(self):
        enh_bri = ImageEnhance.Brightness(self.img)
        image_brightened = enh_bri.enhance(self.brightness)
        return image_brightened

    def image_contrasted(self):
        enh_con = ImageEnhance.Contrast(self.img)
        img_contrasted = enh_con.enhance(self.contrast)
        return img_contrasted
def BROVEY(rgb,b8):
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
   
    change = np.zeros(((3,hight_x,hight_y)))
    change[0,:,:]=np.multiply(np.true_divide(
        resample_RGB[0,:,:],resample_RGB[0,:,:]+resample_RGB[1,:,:]+resample_RGB[2,:,:]),hight_array)
    change[1,:,:]=np.multiply(np.true_divide(
        resample_RGB[1,:,:],resample_RGB[0,:,:]+resample_RGB[1,:,:]+resample_RGB[2,:,:]),hight_array)
    change[2,:,:]=np.multiply(np.true_divide(
        resample_RGB[2,:,:],resample_RGB[0,:,:]+resample_RGB[1,:,:]+resample_RGB[2,:,:]),hight_array)
    change=np.uint8(change)
    img = cv2.merge([change[0],change[1],change[2]])
    img=Image.fromarray(img)
    img.show()
    img_light = ImageEnhance.Brightness(img).enhance(3) #调用类
    img_light.show()
    img_light.save(r"D:\CDUT\intership\experiment1\broveyenhance.png","png")
    #cv2.imwrite(r"D:\CDUT\intership\experiment1\broveyenhance.png", img_light)
def main():
    original_rgb = r"D:\CDUT\intership\experiment1\sample\index.tif"
    original_b8 = r"D:\CDUT\intership\experiment1\sample\b8.tif"
    BROVEY(original_rgb,original_b8)
if __name__ == '__main__':
    main()
    