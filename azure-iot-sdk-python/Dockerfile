FROM vjrantal/iot-edge-darknet-base

WORKDIR /

RUN apt-get update
RUN apt-get install -y git

RUN git clone -b master --single-branch https://github.com/Azure/azure-iot-sdk-python.git

WORKDIR /azure-iot-sdk-python

# Use a tested release of the SDK
RUN git checkout release_2018_09_17
RUN git submodule update --init --recursive

WORKDIR /azure-iot-sdk-python/build_all/linux
RUN apt-get install -y sudo build-essential pkg-config libcurl3-openssl-dev git cmake libssl-dev uuid-dev libboost-python-dev
RUN ./build.sh
