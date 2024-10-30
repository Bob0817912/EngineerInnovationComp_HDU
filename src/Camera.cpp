#include "Camera.hpp"
#include "Info.hpp"
#include <opencv2/opencv.hpp>

Camera::Camera(int index)
{
    if (index == 0)
        cap.open(index);
    else
        cap.open(index, cv::CAP_V4L2);
    if (!cap.isOpened()) {
        ERROR("[Camera] Error opening video stream or file.");
        exit(-1);
    }
}

Camera::~Camera()
{
    cap.release();
}

Camera &Camera::load(int index)
{
    if (index == 0)
        cap.open(index);
    else
        cap.open(index, cv::CAP_V4L2);
    if (!cap.isOpened()) {
        ERROR("[Camera] Error opening video stream or file.");
        exit(-1);
    }
    return *this;
}

cv::Mat Camera::get_frame()
{
    cv::Mat frame;
    cap >> frame;
    if (frame.empty()) {
        ERROR("[Camera] No captured frame.");
        return cv::Mat();
    }
    return frame;
}

Camera &Camera::operator=(Camera &src)
{
    this->cap = src.cap;
    return *this;
}