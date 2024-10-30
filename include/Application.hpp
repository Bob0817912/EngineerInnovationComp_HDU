#pragma once

#include <atomic>
#include <opencv2/core/types.hpp>
#include <thread>

#include "Camera.hpp"
#include "Serial.hpp"
#include "Detector.hpp"

#include "DoubleBuffer.hpp"

class Application {
public:
    enum STATUS {
        SCAN_QR_CODE = 0,
        FIRST_GROUP = 1,
        SECOND_GROUP = 2,
        MOVING = 3
    };
    Application();
    Application(int QRscaner_index, int camera_index);
    ~Application() = default;

    Application &setQRscanerIndex(int index);
    Application &setCameraIndex(int index);
    Application &setSerial(std::string name, unsigned int baud_rate);

    Application &start();
    Application &join();

private:
    // Camera QRscaner;
    // Camera camera;
    // Detector detector;
    // Serial serial;
    int camera_index, QRscaner_index;

    std::string order;
    uint8_t current_detect_color;
    std::atomic<STATUS> status;
    std::atomic<int> complate_count;
    std::atomic<cv::Point2f> r_diff;
    std::atomic<cv::Point2f> g_diff;
    std::atomic<cv::Point2f> b_diff;

    std::shared_ptr<std::thread> camera_thread;
    std::shared_ptr<std::thread> detector_thread;
    std::shared_ptr<std::thread> serial_thread;

    DoubleBuffer<cv::Mat> img_buffer;

    void cameraThread();
    void detectorThread();
    void serialThread();
    Detector::CHANNEL getDetectColor(STATUS status, int complate_count);
};