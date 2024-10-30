#include "Serial.hpp"

Serial::Serial(std::string serial_name, unsigned int baud_rate,
               unsigned int character_size,
               serial_port::flow_control flow_control,
               serial_port::parity parity, serial_port::stop_bits stop_bits)
{
    serial_port_ = std::make_shared<serial_port>(io_service_, serial_name);
    serial_port_->set_option(serial_port::baud_rate(baud_rate));
    serial_port_->set_option(serial_port::character_size(character_size));
    serial_port_->set_option(flow_control);
    serial_port_->set_option(parity);
    serial_port_->set_option(stop_bits);

    if (!this->isOpened())
        serial_port_->open(serial_name);
}

Serial::Serial(Serial &serial)
{
    serial_port_ = serial.serial_port_;
}

Serial::~Serial()
{
    this->close();
}

bool Serial::isOpened()
{
    return serial_port_->is_open();
}

bool Serial::close()
{
    if (isOpened()) {
        serial_port_->close();
        return true;
    }
    return false;
}

bool Serial::write_(uint8_t *data, size_t size)
{
    return boost::asio::write(*serial_port_, buffer(data, size)) == size;
}

bool Serial::receive_(uint8_t *data, size_t size)
{
    return boost::asio::read(*serial_port_, buffer(data, size)) == size;
}

Serial &&Serial::operator=(Serial &&serial)
{
    serial_port_ = serial.serial_port_;
    return std::move(*this);
}