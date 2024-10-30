#pragma once

#include <opencv2/opencv.hpp>

class Camera {
public:
    Camera() = default;
    Camera(int index);
    ~Camera();
    Camera &load(int index);
    cv::Mat get_frame();

    Camera &operator=(Camera &src);

private:
    cv::VideoCapture cap;
    cv::Mat frame;
};