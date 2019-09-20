## 什么是alpha blending？
Alpha blending是将前景图像加在一个背景图像上,透明度是图像的第四通道的值，一般是一个四通道的png图像，当然也可能是一张单独的黑白图像，一般被称为
alpha掩膜。在下面这张图中，左上是前景图像，右上是alpha掩膜，下面是背景图像。

![alpha-blending-using-opencv.jpg](https://github.com/zhangqizky/LearnOpenCV_Chinese/blob/master/AlphaBlending/alpha-blending-using-opencv.jpg)

alpha blending背后的数学知识很简单，对于每个像素，都是通过前景图像和背景图像由alpha掩膜的值加权而来。   
 I = a*F + (1-a)B

从上面的公式可以看出：
- 当 a=0的时候，输出像素就是背景图像的像素
- 当 a=1的时候，输出图像的像素是前景图像的像素
- 当0<a<1的时候，输出图像的像素是前景和背景图像的混合像素

## 如何实现？  
```
#include<opencv2/opencv.hpp>

using namespace cv;

int main()
{
    //读取图像
    Mat foreground = imread("puppets.png");
    Mat background = imread("ocean.png");
    Mat alpha = imread("puppets_alpha.png");
    
    //为了防止计算溢出，使用浮点数去计算
    foreground.convertTo(foreground,CV_32FC3);
    background.convertTo(background,CV_32FC3);
    alpha.convertTo(alpha,CV_32FC3,1.0/255);
    
    Mat outImage = Mat::zeros(foreground.size(),foreground.type());
    //对两者进行加权
    multiply(alpha,foreground,foreground);
    multiply(Scalar::all(1.0)-alpha,background,background);
    add(foreground,background,outImage);
    //imshow这个函数是可以显示0-255之间整数的矩阵和0-1之间浮点数的矩阵
    imshow("outImage",outImage/255);
    waitKey(0);
    return 0;    
}
```
