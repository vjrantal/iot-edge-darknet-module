FROM vjrantal/azure-iot-sdk-python:latest as azure-iot-sdk-python
FROM vjrantal/darknet:latest as darknet

# Was planning to use alpine as the runtime from image, but
# some required packages were missing from the default
# repository so keeping it simple and going with ubuntu for now.

FROM vjrantal/iot-edge-darknet-base

WORKDIR /

# Copy in required dependencies

COPY --from=azure-iot-sdk-python /azure-iot-sdk-python/device/samples/iothub_client.so .

COPY --from=darknet /darknet/libdarknet.so /usr/lib/
COPY --from=darknet /darknet/python/darknet.py .
COPY --from=darknet /darknet/yolo.weights .
COPY --from=darknet /darknet/cfg ./cfg
COPY --from=darknet /darknet/data ./data

RUN apt-get update
RUN apt-get install -y libboost-python1.58.0 python-opencv libcurl3

COPY *.py /

CMD ["python", "-u", "module.py"]
