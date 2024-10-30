#include "Application.hpp"

int main(int argc, char *argv[])
{
    // ignore SIGPIPE
    signal(SIGPIPE, SIG_IGN);

    Application app;
    app.setQRscanerIndex(std::stoi(argv[1]))
        .setCameraIndex(std::stoi(argv[2]))
        .setSerial(argv[3], 115200)
        .start()
        .join();
    return 0;
}
