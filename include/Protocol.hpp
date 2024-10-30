#pragma once

#include <stdint.h>

#pragma pack(1)

/*!!!!!!!!!! small dian !!!!!!!!!!*/

// clang-format off
typedef struct serialSendProtocol_s {
    uint8_t start = 's';            // 0 ~ 1 起始位，默认 's'
    uint8_t order[7];               // 1 ~ 8 放置顺序，例如 123+321，二维码识别到后此项固定，否则为 0
    uint8_t current_detect_color;   // 8 ~ 9 当前识别到的颜色，取值 0 ~ 7, 含义如下：
                                    //              0 0 0 0 0 0 0 0
                                    //                        R G B
    float x_diff[3];                // 9 ~ 21 识别到的各颜色中心点与图像中心点 x 方向的差值，值域(-340,340)
    float y_diff[3];                // 21 ~ 33 识别到的各颜色中心点与图像中心点 y 方向的差值，值域(-240,240)
                                    // 下标顺序 RGB
                                    // 当未识别到某颜色时，x_diff[color], y_diff[color] 均赋值为 -999
    uint8_t crc;                    // 33 ~ 34 数据段 crc 校验，使用 CRC-8
    uint8_t end = 'e';              // 34 ~ 35 结束位，默认 'e'
} serialSendProtocol_t; // 35 Byte

typedef struct serialRecvProtocol_s {
    uint8_t start = 's';        // 0 ~ 1 起始位，默认 's'
    uint8_t status;             // 1 ~ 2 当前状态，取值及含义如下：
                                // 1: 第一组， 2: 第二组， 3: moving
    uint8_t complate_count;     // 2 ~ 3 当前批次完成搬运的个数，取值 0,1,2
                                // 拿取和放置时均要重置
    uint8_t end = 'e';          // 3 ~ 4 结束位，默认 'e'
} serialRecvProtocol_t; // 4 Byte
// clang-format on

#pragma pack()