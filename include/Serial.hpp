#pragma once

#include <boost/asio.hpp>
#include <boost/bind.hpp>
#include <iostream>

using namespace boost::asio;

class Serial {
public:
    Serial() = default;
    /**
   * @brief Serial构造函数, 对象创建后会自动打开串口
   * @param serial_name 串口名
   * @param baud_rate 波特率
   * @param character_size 数据位 默认8
   * @param flow_control 流量控制 默认无
   * @param parity 校验位 默认无
   * @param stop_bits 停止位 默认1
   */
    Serial(std::string serial_name, unsigned int baud_rate,
           unsigned int character_size = 8U,
           serial_port::flow_control flow_control =
               serial_port::flow_control(serial_port::flow_control::none),
           serial_port::parity parity =
               serial_port::parity(serial_port::parity::none),
           serial_port::stop_bits stop_bits =
               serial_port::stop_bits(serial_port::stop_bits::one));
    Serial(Serial &serial);
    ~Serial();

    /**
   * @brief 串口发送函数
   * @tparam T 发送数据结构
   * @param data 发送数据指针
   * @param size 发送数据大小（字节数）
   * @return 发送成功返回true，否则返回false
   */
    template <typename T> bool write(T *data, size_t size)
    {
        return write_((uint8_t *)data, size);
    }
    /**
   * @brief 串口接收函数
   * @tparam T 接收数据结构
   * @param data 接收数据指针
   * @param size 接收数据大小（字节数）
   * @return 接收成功返回true，否则返回false
   */
    template <typename T> bool receive(T *data, size_t size)
    {
        return receive_((uint8_t *)data, size);
    }
    /**
     * @brief 发送并接收串口数据
     * 
     * @tparam sendT 发送消息类型
     * @tparam recvT 接收消息类型
     * @param send_data 发送的数据包
     * @param send_size 发送的数据包大小
     * @param recv_data 接收的数据包
     * @param recv_size 接收的数据包大小
     * @return true 成功
     * @return false 失败
     */
    template <typename sendT, typename recvT>
    bool writeRecv(sendT *send_data, size_t send_size, recvT *recv_data,
                   size_t recv_size)
    {
        return write_((uint8_t *)send_data, send_size) &&
               receive_((uint8_t *)recv_data, recv_size);
    }
    /**
   * @brief 获取串口开启状态
   * @return 打开返回true，否则返回false
   */
    bool isOpened();

    /**
   * @brief 串口关闭函数
   * @return 关闭成功返回true，否则返回false
   */
    bool close();

    /**
     * @brief 移动构造函数
     * 
     * @param serial 移动对象
     * @return Serial&&
     */
    Serial &&operator=(Serial &&serial);

private:
    io_service io_service_;
    std::shared_ptr<serial_port> serial_port_;

    /**
   * @brief 串口发送函数原型
   * @param data 发送数据指针
   * @param size 发送数据大小
   * @return 发送成功返回true，否则返回false
   */
    bool write_(uint8_t *data, size_t size);
    /**
   * @brief 串口接收函数原型
   * @param data 接收数据指针
   * @param size 接收数据大小
   * @return 接收成功返回true，否则返回false
   */
    bool receive_(uint8_t *data, size_t size);
};