#include <iomanip>
#include <iostream>
#include <chrono>

#include "Info.hpp"

Info::Info()
{
    colors["red"] = "\033[1;31m";
    colors["green"] = "\033[1;32m";
    colors["yellow"] = "\033[1;33m";
    colors["blue"] = "\033[1;34m";
    colors["magenta"] = "\033[1;35m";
    colors["cyan"] = "\033[1;36m";
    colors["white"] = "\033[1;37m";
    colors["default"] = "\033[0m";

    print = [&](std::string msg, std::string color) {
        std::lock_guard<std::mutex> lock(mtx);
        std::string currTime = "[" + get_currTime_time() + "]";
        std::cout << colors[color] << currTime << msg << colors["default"]
                  << std::endl;
    };
}

std::string Info::get_currTime_time()
{
    auto now = std::chrono::system_clock::now();
    auto now_c = std::chrono::system_clock::to_time_t(now);
    auto now_ms = std::chrono::duration_cast<std::chrono::nanoseconds>(
                      now.time_since_epoch()) %
                  1000000000;
    std::tm *ptm = std::localtime(&now_c);
    std::stringstream ss;
    ss << std::put_time(ptm, "%X") << '.' << std::setfill('0') << std::setw(9)
       << now_ms.count();
    return ss.str();
}

Info::~Info()
{
}

Info info;