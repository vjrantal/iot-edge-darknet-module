FROM vjrantal/iot-edge-darknet-base

WORKDIR /

RUN apt-get update
RUN apt-get install -y git

# Use the modules-preview branch for support for IoT Edge modules
RUN git clone -b modules-preview --single-branch https://github.com/Azure/azure-iot-sdk-python.git

WORKDIR /azure-iot-sdk-python

# Use a tested commit of the SDK
RUN git checkout d3619f8d5ec0beca87b0d3b98833ae8053c39419
RUN git submodule update --init --recursive

WORKDIR /azure-iot-sdk-python/build_all/linux
RUN apt-get install -y sudo build-essential pkg-config libcurl3-openssl-dev git cmake libssl-dev uuid-dev libboost-python-dev
RUN ./build.sh
