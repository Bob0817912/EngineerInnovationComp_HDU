#ifndef INFO_HPP
#define INFO_HPP

#include <mutex>
#include <map>
#include <functional>
#include <string>

/**
 * @brief Info 类, 用于输出信息。进程内单例, 用于防止多线程输出混乱。
 * 
 */
class Info {
public:
    /**
     * @brief Info 构造函数
     * 
     */
    Info();
    /**
     * @brief Info 析构函数
     * 
     */
    ~Info();
    std::function<void(std::string, std::string)> print; ///< 输出函数
private:
    std::mutex mtx; ///< 互斥锁
    std::map<std::string, std::string> colors; ///< 输出颜色

    /**
     * @brief 获取当前时间
     * 
     * @return std::string 当前时间字符串
     */
    std::string get_currTime_time();
};

extern Info info;

// 定义输出宏
#define INFO_LEVEL_QUITE 0
#define INFO_LEVEL_ERROR 1
#define INFO_LEVEL_WARNING 2
#define INFO_LEVEL_INFO 3
#define INFO_LEVEL_DEBUG 4

#if INFO_LEVEL >= INFO_LEVEL_ERROR
#define ERROR(msg) info.print("[ERROR]\t| " + std::string(msg), "red")
#else
#define ERROR(msg)
#endif
#if INFO_LEVEL >= INFO_LEVEL_WARNING
#define WARNING(msg) info.print("[WARNING]\t| " + std::string(msg), "yellow")
#else
#define WARNING(msg)
#endif
#if INFO_LEVEL >= INFO_LEVEL_INFO
#define INFO(msg) info.print("[INFO]\t| " + std::string(msg), "white")
#else
#define INFO(msg)
#endif
#if INFO_LEVEL >= INFO_LEVEL_DEBUG
#define DEBUG(msg) info.print("[DEBUG]\t| " + std::string(msg), "blue")
#define SUCCESS(msg) info.print("[SUCCESS]\t| " + std::string(msg), "green")
#else
#define DEBUG(msg)
#define SUCCESS(msg)
#endif

#endif