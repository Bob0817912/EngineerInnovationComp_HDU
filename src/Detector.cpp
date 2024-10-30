#include "Detector.hpp"

#include <cmath>

#include "Info.hpp"
#include <exception>
#include <opencv2/core.hpp>
#include <opencv2/core/matx.hpp>
#include <opencv2/core/types.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/objdetect.hpp>

#include <opencv2/opencv.hpp>
#include <opencv4/opencv2/core/types.hpp>
#include <string>
#include <vector>

Detector::Detector()
    : ed(cv::ximgproc::createEdgeDrawing())
    , raw_empty(true)
{
    ed->params.EdgeDetectionOperator = cv::ximgproc::EdgeDrawing::SOBEL;
    ed->params.GradientThresholdValue = 35;
    ed->params.AnchorThresholdValue = 8;
}

Detector &Detector::inputMat(cv::Mat &raw)
{
    if (raw.empty()) {
        DEBUG("[Detector] input mat is empty.");
        raw_empty = true;
        return *this;
    }
    raw_empty = false;

    this->raw = raw.clone();
    // 识别地面背景白色
    cv::Mat hsv;
    cv::cvtColor(raw, hsv, cv::COLOR_BGR2HSV);
    cv::GaussianBlur(hsv, hsv, cv::Size(3, 3), 1, 2);

    cv::Mat mask;
    cv::inRange(hsv, cv::Scalar(0, 0, 46), cv::Scalar(180, 43, 255), mask);
    raw.setTo(cv::Scalar(0, 0, 0), mask);
    cv::Mat Rmask;
    // 分离通道
    cv::inRange(hsv, cv::Scalar(100, 43, 64), cv::Scalar(124, 255, 255),
                channels[2]);
    cv::inRange(hsv, cv::Scalar(35, 43, 46), cv::Scalar(77, 255, 255),
                channels[1]);
    cv::inRange(hsv, cv::Scalar(0, 43, 46), cv::Scalar(10, 255, 255),
                channels[0]);
    cv::inRange(hsv, cv::Scalar(156, 43, 46), cv::Scalar(180, 255, 255), Rmask);

    cv::bitwise_or(channels[0], Rmask, channels[0]);

    return *this;
}

std::string Detector::detectQRcode()
{
    if (raw_empty) {
        return "";
    }
    cv::QRCodeDetector qrDecoder;
    std::string data = qrDecoder.detectAndDecode(raw);
    if (!data.empty()) {
        INFO("[detectQRcode] QR code detected: " + data);
        return data;
    }
    DEBUG("[detectQRcode] no QR code detected.");
    return "";
}

bool Detector::detectCircle(CHANNEL color, cv::Point2f &diff_to_Icenter)
{
    if (raw_empty) {
        return false;
    }
    channels_binary_mat[static_cast<int>(color)] =
        channels[static_cast<int>(color)].clone();
    // 物料俯视图是圆形，所以检测圆形
    cv::Mat binary = channels_binary_mat[static_cast<int>(color)];
    // 去除噪声
    // cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));
    // cv::morphologyEx(binary, binary, cv::MORPH_OPEN, element);
    // cv::morphologyEx(binary, binary, cv::MORPH_CLOSE, element);
    // element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));

    // 拟合圆形
    std::vector<cv::Vec6d> ellipses;
    try {
        ed->detectEdges(binary);
        ed->detectEllipses(ellipses);
    } catch (cv::Exception &e) {
        std::cerr << e.what() << std::endl;
    } catch (std::exception &e) {
        std::cerr << e.what() << std::endl;
    } catch (...) {
        std::cerr << "Unknown exception." << std::endl;
    }

    if (ellipses.empty()) {
        DEBUG("[detectCircle] no ellipses detected.");
        return false;
    }
    // 选择最大的圆
    float max_radius = 10;
    cv::Point2f center;
    for (auto &ellipse : ellipses) {
        // 中心点
        auto c = cv::Point2f(ellipse[0], ellipse[1]);
        // 长轴和短轴
        auto axes = cv::Size(ellipse[2] + ellipse[3], ellipse[2] + ellipse[4]);
        // 角度
        auto angle = ellipse[5];
        // 计算离心率
        auto e = std::sqrt(1.0 - (1.0 * axes.height / axes.width) *
                                     (1.0 * axes.height / axes.width));
        // 计算半径
        auto r = (axes.height + axes.width) / 2.;
        // 根据离心率找到正圆，离心率小于0.1，二值化后不为黑色
        if (e < 0.1 && binary.at<uchar>(c) > 0) {
            DEBUG("[detectCircle] circle found at (" +
                  std::to_string(center.x) + ", " + std::to_string(center.y) +
                  "), radius = " + std::to_string(r));
            if (r > max_radius) {
                max_radius = r;
                center = c;
            }
            cv::ellipse(raw, c, axes, angle, 0, 360, cv::Scalar(0, 255, 255));
        }
    }
    if (center.x == 0 && center.y == 0) {
        WARNING("[detectCircle] " + std::to_string(ellipses.size()) +
                " ellipses detected, but no valied circle. color: " +
                std::to_string(static_cast<int>(color)));
        return false;
    }

    cv::Point2f diff = center - cv::Point2f(raw.cols / 2., raw.rows / 2.);
    cv::circle(raw, cv::Point(raw.cols / 2, raw.rows / 2), 3,
               cv::Scalar(12, 34, 56), -1);
    cv::circle(raw, center, 3, cv::Scalar(12, 34, 56), -1);
    cv::line(raw, cv::Point(raw.cols / 2, raw.rows / 2), center,
             cv::Scalar(12, 34, 56), 2);

    diff_to_Icenter = diff;
    INFO("[detectCircle] biggest circle detected at (" +
         std::to_string(center.x) + ", " + std::to_string(center.y) +
         "), color: " + std::to_string(static_cast<int>(color)));

    return true;
}

int Detector::showDebugWindow()
{
    if (raw_empty) {
        return -1;
    }

    cv::imshow("raw", raw);
    for (int i = 0; i < 3; i++) {
        if (!channels[i].empty())
            cv::imshow("RGB channel " + std::to_string(i), channels[i]);
        if (!channels_binary_mat[i].empty())
            cv::imshow("RGB channel_bin" + std::to_string(i),
                       channels_binary_mat[i]);
        if (!channels_show_mat[i].empty())
            cv::imshow("RGB channel_res " + std::to_string(i),
                       channels_show_mat[i]);
    }

    cv::waitKey(10);

    return 0;
}
