import os
import cv2
import numpy as np

def readImagesAndTimes():
    """[读取时间和图像]
    
    Returns:
        [list of images] -- [图像]
        [list of times] -- [时间]
    """
    times = np.array([1/30,0.25,2.5,15],dtype=np.float32)
    filenames = ["img_0.033.jpg","img_0.25.jpg","img_2.5.jpg","img_15.jpg"]
    images = []
    for filename in filenames:
        im = cv2.imread(filename)
        images.append(im)
    return images,times

def main():
    #读取多张曝光的图像
    images,times = readImagesAndTimes()

    #对齐图像
    alignMTB = cv2.createAlignMTB()
    alignMTB.process(images, images)

    #恢复相机响应函数
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(images, times)

    # 将多张图像融合成hdr
    mergeDebevec = cv2.createMergeDebevec()
    hdrDebevec = mergeDebevec.process(images, times, responseDebevec)
    # 保存融合结果，可用ps打开
    cv2.imwrite("hdrDebevec.hdr", hdrDebevec)

    # Tonemap using Drago's method to obtain 24-bit color image
    tonemapDrago = cv2.createTonemapDrago(1.0, 0.7)
    ldrDrago = tonemapDrago.process(hdrDebevec)
    ldrDrago = 3 * ldrDrago
    cv2.imwrite("ldr-Drago.jpg", ldrDrago * 255)

    # Tonemap using Durand's method obtain 24-bit color image
    tonemapDurand = cv2.createTonemapDurand(1.5,4,1.0,1,1)
    ldrDurand = tonemapDurand.process(hdrDebevec)
    ldrDurand = 3 * ldrDurand
    cv2.imwrite("ldr-Durand.jpg", ldrDurand * 255)

    # Tonemap using Reinhard's method to obtain 24-bit color image
    tonemapReinhard = cv2.createTonemapReinhard(1.5, 0,0,0)
    ldrReinhard = tonemapReinhard.process(hdrDebevec)
    cv2.imwrite("ldr-Reinhard.jpg", ldrReinhard * 255)

    # Tonemap using Mantiuk's method to obtain 24-bit color image
    tonemapMantiuk = cv2.createTonemapMantiuk(2.2,0.85, 1.2)
    ldrMantiuk = tonemapMantiuk.process(hdrDebevec)
    ldrMantiuk = 3 * ldrMantiuk
    cv2.imwrite("ldr-Mantiuk.jpg", ldrMantiuk * 255)

if __name__=="__main__":
    main()
