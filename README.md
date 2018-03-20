# IoT Edge Darknet module

Sample module for IoT Edge that uses [Darknet](https://github.com/pjreddie/darknet) for object detection.

[![Build Status](https://travis-ci.org/vjrantal/iot-edge-darknet-module.svg?branch=master)](https://travis-ci.org/vjrantal/iot-edge-darknet-module)

# Deploying to IoT Edge

If you have installed the [extension for Azure CLI 2.0](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-create-deployment-with-cli-iot-extension), you can deploy the pre-built docker image with command like:

```
az iot hub apply-configuration --device-id <device-id> --hub-name <hub-name> --content deployment.json
```

# Building docker images

```
docker build -f base/Dockerfile -t vjrantal/iot-edge-darknet-base .
docker build -f azure-iot-sdk-python/Dockerfile -t vjrantal/azure-iot-sdk-python .
docker build -f darknet/Dockerfile -t vjrantal/darknet .
docker build -t vjrantal/iot-edge-darknet-module .
```

# Running locally

If you want to run outside of docker, you need to build the azure-iot-sdk-python and darknet projects on your host machine and copy the build assets onto this directory. See the Dockerfile in the root which files need to be copied.

# Video device selection

The code tries to detect a video device by default using index 0. In practice, those indexes map to devices under /dev. You can check what devices you have available in the docker context, for example, with a command like:

```
root@tegra-ubuntu:~# docker run --privileged alpine ls /dev/video*
/dev/video0
/dev/video1
```

In above sample, I had two devices connected to a Jetson TX2 Developer Kit. The default 0 index would be the in-built camera, but I would like to use the index 1 which is the USB-connected camera.

The environment variable `OPENCV_CAMERA_INDEX` can be set to select the used index so selecting `/dev/video1` in my IoT Edge deployment would mean that the `createOptions` in the [deployment.json](deployment.json) should be:

```
"createOptions": "{\"Env\":[\"OPENCV_CAMERA_INDEX=1\"],\"HostConfig\":{\"Privileged\":true}}"
```

# Running on Jetson TX2

The architecture of the Jetson TX2 device is:

```
root@tegra-ubuntu:~# uname -m
aarch64
```

Since IoT Edge has not published images for that exact architecture, the default options will fail. Luckily, the arm32v7 images that can be found from [https://hub.docker.com/r/microsoft/azureiotedge-agent/tags/](https://hub.docker.com/r/microsoft/azureiotedge-agent/tags/), but one must explicitly choose those.

The IoT Edge Agent image is chosen in the setup phase and can be done with flag:

```
  --image               Set the Edge Agent image. Optional.
```
To the `iotedgectl setup` command. The image I tested with was `microsoft/azureiotedge-agent:1.0.0-preview021-linux-arm32v7`.

The IoT Edge Hub image is chosen during deployment and one can see an example at [./jetson-tx2/deployment.json](./jetson-tx2/deployment.json).

When building the docker images, two things should be noted. The base used should the one from[./jetson-tx2/Dockerfile](./jetson-tx2/Dockerfile) and one should pass `gpu=1` to the darknet image so that GPU support will be enabled. Overall, the right commands to build the module would be like:

```
docker build -f jetson-tx2/Dockerfile -t vjrantal/iot-edge-darknet-base .
docker build -f azure-iot-sdk-python/Dockerfile -t vjrantal/azure-iot-sdk-python .
docker build -f darknet/Dockerfile -t vjrantal/darknet . --build-arg gpu=1
docker build -t vjrantal/iot-edge-darknet-module .
```

# Running on DSVM

Azure has so called [DSVM](https://azure.microsoft.com/en-us/services/virtual-machines/data-science-virtual-machines/) that is pre-configured for data science workflows. After creating the DSVM, make sure you have latest nvidia-docker installed. To check that this pre-step is working, run this command:

```
docker run --runtime=nvidia nvidia/cuda:9.0-devel-ubuntu16.04 nvidia-smi
```

If above works, you can build the module with these commands:

```
docker build -f nvidia-docker/Dockerfile -t vjrantal/iot-edge-darknet-base .
docker build -f azure-iot-sdk-python/Dockerfile -t vjrantal/azure-iot-sdk-python .
docker build -f darknet/Dockerfile -t vjrantal/darknet . --build-arg gpu=1
docker build -t vjrantal/iot-edge-darknet-module .
```

# Performance results

Performance comparison while running the detection within docker using [this static image](https://github.com/pjreddie/darknet/blob/8f1b4e0962857d402f9d017fcbf387ef0eceb7c4/data/dog.jpg).

| Environment | Seconds per detection | Notes |
| --- | --- | --- |
| Jetson TX2 | 0.75 | 256 core NVIDIA Pascal GPU |
| MacBook Pro | 10.3 | Using CPU (2,8 GHz Intel Core i7) |
| Raspberry Pi 3 | 337.6 | CPU (had to increase swap size to run) |
| Standard NC6 DSVM | 0.23 | One-half NVIDIA K80 GPU (using nvidia-docker) |
| Standard NV6 DSVM | 0.22 | One-half NVIDIA M60 GPU (using nvidia-docker) |
