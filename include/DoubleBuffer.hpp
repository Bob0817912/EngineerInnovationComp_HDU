#pragma once

#include <atomic>
#include <vector>

template <typename T> class DoubleBuffer {
public:
    DoubleBuffer();
    ~DoubleBuffer() = default;
    int write(T);
    T &read();
    int swap();
    bool clear();

private:
    std::atomic<int> w_index;
    std::vector<T> buffer;
};

template <typename T>
DoubleBuffer<T>::DoubleBuffer()
    : w_index(0)
    , buffer({ T(), T() })
{
}

template <typename T> int DoubleBuffer<T>::write(T data)
{
    buffer[w_index] = data;
    swap();
    return 0;
}

template <typename T> T &DoubleBuffer<T>::read()
{
    return buffer[1 - w_index];
}

template <typename T> int DoubleBuffer<T>::swap()
{
    w_index = 1 - w_index;
    return 0;
}

template <typename T> bool DoubleBuffer<T>::clear()
{
    buffer.clear();
    w_index = 0;
    return true;
}