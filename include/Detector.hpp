#pragma once

#include "opencv2/core/types.hpp"
#include <string>
#include <opencv2/opencv.hpp>
#include <opencv2/ximgproc.hpp>

class Detector {
public:
    enum class CHANNEL { BLUE = 2, GREEN = 1, RED = 0, NOT_FOUND = -1 };
    Detector();
    ~Detector() = default;
    Detector &inputMat(cv::Mat &raw);
    std::string detectQRcode();
    bool detectCircle(CHANNEL color, cv::Point2f &diff_to_Icenter);

    int showDebugWindow();

private:
    cv::Mat raw;
    cv::Mat channels[3];
    bool raw_empty;
    cv::Ptr<cv::ximgproc::EdgeDrawing> ed;

    cv::Mat channels_binary_mat[3];
    cv::Mat channels_show_mat[3];
};
