#include opencv2/opencv.hpp
 
using namespace cv;
using namespace std;
 
int main(int argc, char** argv)
{
 
    Mat foreground = imread("puppets.png");
    Mat background = imread("ocean.png");
    Mat alpha = imread("puppets_alpha.png");
     
    foreground.convertTo(foreground, CV_32FC3);
    background.convertTo(background, CV_32FC3);
    alpha.convertTo(alpha, CV_32FC3, 1.0/255); 
 

    Mat ouImage = Mat::zeros(foreground.size(), foreground.type());
 

    multiply(alpha, foreground, foreground); 

    multiply(Scalar::all(1.0)-alpha, background, background); 
 

    add(foreground, background, ouImage); 

    imshow("alpha blended image", ouImage/255);
    waitKey(0);
     
    return 0;
}
