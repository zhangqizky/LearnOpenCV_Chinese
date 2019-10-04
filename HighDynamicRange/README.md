## 前言
在这篇教程中，我们学习如何利用同一时刻不同曝光水平拍摄的图像来合成高动态范围图像(HDR)，并给出python和C++的代码。

## 什么是高动态范围成像？
大多数的拍摄设备成像都是24位的，三个颜色通道每个各8bit，是一个0～255之间的像素值。也就是说，一个常规的相机成像的像素值范
非常有限。然而真实的世界的色彩是非常丰富多彩的。比如说，当没有灯光的时候，草地也会呈现黑色，如果直接在大太阳下面看
则会非常亮。即使不考虑这些极端情况，8-bits也很难去捕获所有的场景。所以，相机试图去估计当前场景中的亮度，并且
自动设置合适的曝光量，这样所成的像就会有很大的范围。
在下面的图像中，左边的图是正常曝光的，注意到天空已经看不清了。右边的是用iPhone拍摄的HDR图像。  

![]("https://www.learnopencv.com/wp-content/uploads/2017/09/high-dynamic-range-hdr.jpg")
iPhone怎么拍摄HDR图像？实际上，它利用三个曝光度拍摄三张图像，这三张图像基本上是在同一时刻拍摄的，所以基本上没有移动。
然后再利用这三张图像去合成HDR图像。

## HDR成像如何工作？

### 第一步：利用不同曝光度拍摄图像
  当我们使用相机拍摄照片时，我们只有每秒8位来表示场景的动态范围（亮度范围）。但我们可以通过改变快门速度，在不同的曝光量下拍摄多幅场景图像。大多数单反相机都有一个称为自动曝光支架（AEB）的功能，可以让我们只需按一个按钮就可以在不同的曝光量下拍摄多张照片。如果你使用的是iphone，你可以使用这个AutoBracket App，如果你是android用户，你可以尝试一个更好的相机App。
  使用相机上的AEB或手机上的自动包围应用程序，我们可以一张接一张地快速拍摄多张照片，这样场景就不会改变。当我们在iphone中使用hdr模式时，它会拍三张照片。
  - 曝光不足的图像：这个图像比适当曝光的图像暗。目标是捕捉图像中非常明亮的部分。
  - 适当曝光的图像：这是相机根据其估计的亮度拍摄的规则图像。 
  - 曝光过度的图像：这个图像比正确曝光的图像更亮。目标是捕捉图像中非常暗的部分。
 然而，如果场景的动态范围非常大，我们可以拍摄三张以上的照片来合成hdr图像。在本教程中，我们将使用曝光时间1/30、0.25、2.5和15秒拍摄的4幅图像。四幅图像的缩略图如下所示。
 关于SLR相机或电话所使用的曝光时间和其他设置的信息通常存储在JPEG文件的EXIF元数据中。(请查看此链接)[]，以查看在Windows和MAC中存储在JPEG文件中的ExIF元数据。或者，可以使用我最喜欢的exif命令行实用程序(exiftool)[]。
 
### 第二步：对齐图像
HDR成像时，虽然几张图像的拍摄时间基本上是一致的，但是设备的抖动是不能完全避免的，所以图像还是会有细微的差距，如果不对齐这几张图像，就会在合成图像中产生一些肉眼可见的效应。比如说下图，左边是没有对齐的HDR成像，右边是对齐之后的HDR成像。OpenCV提供了算法来对齐图像，AlignMTB。此算法将所有的图像转换为中值阈值位图，该算法将所有图像转换为中值阈值位图（MTB）。比中值更亮的像素分配1，否则分配0。MTB对曝光时间是不变的。因此，可以在不要求我们指定曝光时间的情况下对齐。代码如下：
'''
alignMTB = cv2.creatAlignMTB()
alignMTB.process(images,images)
'''
### 第三步：恢复相机响应函数
相机对场景亮度的响应并不是线性的。这个的意思是当一个相机拍摄两个物体，其中一个的亮度是另一个的两倍，但成像之后亮的物体并不会比暗的物体亮2倍。所以如果不顾及相机的响应函数CRF，我们不可能将一系列图像融合成一张HDR图像。
融合图像成一张HDR图像是什么意思？考虑一张图像(x,y)位置的像素，如果CRF是线性的，除去像素太亮(接近255)，太暗(接近0)，则这个像素值则直接与曝光时间成正比。我们可以滤除太亮或者太暗的像素，并且通过将像素值除以曝光时间来估计像素处的亮度，然后在像素不坏（太暗或太亮）的所有图像上平均该亮度值。我们可以对所有像素执行此操作，并获得一幅图像，其中所有像素通过平均“好”像素来获得。但是相机的CRF是非线性的，所以我们首先得估计相机的响应函数。如果我们知道每个图像的曝光时间，就可以从图像中估计出CRF。与计算机视觉中的许多问题一样，寻找CRF的问题被设置为优化问题，其目标是最小化由数据项和平滑项组成的目标函数。这些问题通常归结为一个线性最小二乘问题，该问题是使用奇异值分解（svd）来求解的，奇异值分解是所有线性代数包的一部分。当然，这些在OpenCV中已经实现了，代码如下：
```
calibrateDebevec = cv2.createCalibrateDebevec()
responseDebevec = calibrateDebevec.process(images, times)
```
### 第四步：融合图像
当CRF被估计出来之后，我们可以用MergeDebevec这个函数来融合生成HDR图像。
```
mergeDebevec = cv2.createMergeDebevec()
hdrDebevec = mergeDebevec.process(images, times, responseDebevec)
cv2.imwrite("hdrDebevec.hdr", hdrDebevec)
```
### 第五步：色调映射
现在我们已经将曝光图像合并为一个HDR图像。你能猜出这个图像的最小和最大像素值吗？对于变黑条件，最小值显然为0。理论最大值是多少？无限的！实际上，最大值在不同的情况下是不同的。如果场景包含非常亮的光源，我们将看到非常大的最大值。下面尽管我们已经使用多个图像恢复了相对亮度信息，但我们现在仍面临将该信息保存为24位图像以供显示的挑战。
下面需要做的就是色调映射。在保持尽可能多细节的同时，将高动态范围（HDR）图像转换成8比特的每个信道图像的过程称为色调映射。映射有很多种办法，OpenCV中实现了四种，需要注意的是并没有绝对的好映射，也没有绝对的坏映射，各个方法都有自己的优点和缺点，我们应该根据自己的需求选择合适的方法，首先看下四种方法的参数：

- 伽马：该参数通过应用伽马校正来压缩动态范围。当gamma等于1时，不应用校正。小于1的gamma会使图像变暗，大于1的gamma会使图像变亮；
- 饱和度：此参数用于增加或减少饱和度。当饱和度高时，颜色更丰富，更强烈。饱和度值接近于零，使颜色淡入灰度；
- 对比度：控制输出图像的对比度（即log（maxpixelvalue/minpixelvalue）

##### Drago Tonemap
Drago Tonemap的参数如下所示：
```
createTonemapDrago
(
float   gamma = 1.0f,
float   saturation = 1.0f,
float   bias = 0.85f 
)  
```
融合的代码如下：
```
# Tonemap using Drago's method to obtain 24-bit color image
tonemapDrago = cv2.createTonemapDrago(1.0, 0.7)
ldrDrago = tonemapDrago.process(hdrDebevec)
ldrDrago = 3 * ldrDrago
cv2.imwrite("ldr-Drago.jpg", ldrDrago * 255)
```
##### Durand Tonemap
参数如下：
```
createTonemapDurand 
(   
  float     gamma = 1.0f, 
  float     contrast = 4.0f,
  float     saturation = 1.0f,
  float     sigma_space = 2.0f,
  float     sigma_color = 2.0f 
); 
```
该算法基于图像分解为基础层和细节层。使用称为双边滤波器的边缘保持滤波器获得基层。sigma_空间和sigma_颜色是双边滤波器的参数，它们分别控制空间域和颜色域中的平滑量。融合代码如下：
```
# Tonemap using Durand's method obtain 24-bit color image
 tonemapDurand = cv2.createTonemapDurand(1.5,4,1.0,1,1)
 ldrDurand = tonemapDurand.process(hdrDebevec)
 ldrDurand = 3 * ldrDurand
 cv2.imwrite("ldr-Durand.jpg", ldrDurand * 255)
```
##### Reinhard Tonemap
```
createTonemapReinhard
(
float   gamma = 1.0f,
float   intensity = 0.0f,
float   light_adapt = 1.0f,
float   color_adapt = 0.0f 
)  
```
参数强度应在[-8，8]范围内。强度值越大，结果越亮。光线自适应控制光线自适应，并处于[0，1]范围内。值1表示仅基于像素值的自适应，值0表示全局自适应。中间值可用于两者的加权组合。参数color_adapt控制色度自适应，并在[0，1]范围内。如果该值被设置为1，则信道被独立地处理；如果该值被设置为0，则每个信道的自适应级别都相同。中间值可用于两者的加权组合。代码如下：
```
# Tonemap using Reinhard's method to obtain 24-bit color image
tonemapReinhard = cv2.createTonemapReinhard(1.5, 0,0,0)
ldrReinhard = tonemapReinhard.process(hdrDebevec)
cv2.imwrite("ldr-Reinhard.jpg", ldrReinhard * 255)
```
##### Mantiuk Tonemap
```
createTonemapMantiuk
(   
float   gamma = 1.0f,
float   scale = 0.7f,
float   saturation = 1.0f 
)  
```
scale是控制对比度的参数,0.6到0.9为最好的。
代码如下：
```
# Tonemap using Mantiuk's method to obtain 24-bit color image
tonemapMantiuk = cv2.createTonemapMantiuk(2.2,0.85, 1.2)
ldrMantiuk = tonemapMantiuk.process(hdrDebevec)
ldrMantiuk = 3 * ldrMantiuk
cv2.imwrite("ldr-Mantiuk.jpg", ldrMantiuk * 255)
```
