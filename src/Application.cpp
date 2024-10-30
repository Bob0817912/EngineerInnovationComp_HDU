#include "Application.hpp"
#include "Camera.hpp"
#include "Detector.hpp"

#include <chrono>
#include <cstdint>
#include <memory>
#include <opencv2/core/types.hpp>
#include <opencv2/highgui.hpp>
#include <thread>

#include <boost/crc.hpp>

#include "Info.hpp"
#include "Protocol.hpp"

Application::Application()
    : status(STATUS::SCAN_QR_CODE)
    , complate_count(0)
{
}

Application::Application(int QRscaner_index, int camera_index)
    : QRscaner_index(QRscaner_index)
    , camera_index(camera_index)
    , status(STATUS::SCAN_QR_CODE)
    , complate_count(0)
{
}

Application &Application::setQRscanerIndex(int index)
{
    QRscaner_index = index;
    return *this;
}

Application &Application::setCameraIndex(int index)
{
    camera_index = index;
    return *this;
}

Application &Application::setSerial(std::string name, unsigned int baud_rate)
{
#ifndef NO_SERIAL
    serial = Serial(name, baud_rate);
#endif
    return *this;
}

Application &Application::start()
{
    camera_thread =
        std::make_shared<std::thread>(&Application::cameraThread, this);
    detector_thread =
        std::make_shared<std::thread>(&Application::detectorThread, this);
    serial_thread =
        std::make_shared<std::thread>(&Application::serialThread, this);

    return *this;
}

Application &Application::join()
{
    // camera_thread->join();
    // detector_thread->join();
    // serial_thread->join();
    auto camera_thread_id = camera_thread->get_id();
    auto detector_thread_id = detector_thread->get_id();
    auto serial_thread_id = serial_thread->get_id();

    // watching dog
    while (true) {
        if (!camera_thread->joinable()) {
            camera_thread =
                std::make_shared<std::thread>(&Application::cameraThread, this);
            WARNING("[Application] camera thread restart.");
        }
        if (!detector_thread->joinable()) {
            detector_thread = std::make_shared<std::thread>(
                &Application::detectorThread, this);
            WARNING("[Application] detector thread restart.");
        }
        if (!serial_thread->joinable()) {
            serial_thread =
                std::make_shared<std::thread>(&Application::serialThread, this);
            WARNING("[Application] serial thread restart.");
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    return *this;
}

void Application::cameraThread()
{
    INFO("[Application] camera thread start.");

    cv::Mat frame;
    Camera camera, QRscaner;
    QRscaner.load(QRscaner_index);
    if (camera_index == QRscaner_index)
        camera = QRscaner;
    else
        camera.load(camera_index);

    while (true) {
        frame = status != STATUS::SCAN_QR_CODE ? camera.get_frame() :
                                                 QRscaner.get_frame();
        img_buffer.write(frame);
    }
    WARNING("[application] camera thread exit.");
}

void Application::detectorThread()
{
    INFO("[Application] detector thread start.");

    cv::Mat frame;
    cv::Point2f diff[3];
    Detector detector;
    while (true) {
        // detector.showDebugWindow();
        frame = img_buffer.read().clone();
        detector.inputMat(frame);
        if (status == STATUS::SCAN_QR_CODE) {
            order = detector.detectQRcode();
            if (order != "") {
                status = STATUS::FIRST_GROUP;
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
            continue;
        }
        diff[0] = diff[1] = diff[2] = cv::Point2f(-999, -999);
        bool r_flag = detector.detectCircle(Detector::CHANNEL::RED, diff[0]);
        std::this_thread::sleep_for(std::chrono::milliseconds(5));
        bool g_flag = detector.detectCircle(Detector::CHANNEL::GREEN, diff[1]);
        std::this_thread::sleep_for(std::chrono::milliseconds(5));
        bool b_flag = detector.detectCircle(Detector::CHANNEL::BLUE, diff[2]);
        std::this_thread::sleep_for(std::chrono::milliseconds(5));

        current_detect_color = (r_flag ? 1 << 2 : 0) | (g_flag ? 1 << 1 : 0) |
                               (b_flag ? 1 << 0 : 0);
        this->r_diff = diff[0];
        this->g_diff = diff[1];
        this->b_diff = diff[2];
    }
    INFO("[Application] detector thread exit.");
}

void Application::serialThread()
{
    INFO("[Application] serial thread start.");
#ifndef NO_SERIAL
    serialSendProtocol_t send_package;
    serialRecvProtocol_t recv_package;
    Serial serial;

    while (true) {
        if (status == STATUS::SCAN_QR_CODE) {
            send_package.order[0] = '0';
            send_package.order[1] = '0';
            send_package.order[2] = '0';
            send_package.order[3] = '0';
            send_package.order[4] = '0';
            send_package.order[5] = '0';
            send_package.order[6] = '0';
        } else {
            send_package.order[0] = order[0];
            send_package.order[1] = order[1];
            send_package.order[2] = order[2];
            send_package.order[3] = order[3];
            send_package.order[4] = order[4];
            send_package.order[5] = order[5];
            send_package.order[6] = order[6];
        }

        send_package.current_detect_color =
            static_cast<uint8_t>(current_detect_color);
        send_package.x_diff[0] = r_diff.load().x;
        send_package.x_diff[1] = g_diff.load().x;
        send_package.x_diff[2] = b_diff.load().x;
        send_package.y_diff[0] = r_diff.load().y;
        send_package.y_diff[1] = g_diff.load().y;
        send_package.y_diff[2] = b_diff.load().y;
        send_package.crc = boost::crc<8, 0x07, 0, 0, false, false>(
            reinterpret_cast<uint8_t *>(send_package.order), 16);

        serial.write(&send_package, sizeof(send_package));
        serial.receive(&recv_package, sizeof(recv_package));

        if (recv_package.complate_count < 0 || recv_package.complate_count > 2)
            ERROR("[Serial] recived complate_count error. value: " +
                  std::to_string(recv_package.complate_count));
        else
            complate_count = recv_package.complate_count;

        if (recv_package.status < 0 || recv_package.status > 3)
            ERROR("[Serial] recived status error. value: " +
                  std::to_string(recv_package.status));
        else
            status = static_cast<STATUS>(recv_package.status);
    }

    INFO("[Application] serial thread exit.");
#endif
    return;
}

Detector::CHANNEL Application::getDetectColor(STATUS status, int complate_count)
{
    int index;
    if (status == STATUS::FIRST_GROUP)
        index = 0 + complate_count;
    if (status == STATUS::SECOND_GROUP)
        index = 4 + complate_count;
    auto color = order[index] - '1';
    return static_cast<Detector::CHANNEL>(color);
}