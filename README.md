# IoT Edge Darknet module

[![Build Status](https://travis-ci.org/vjrantal/iot-edge-darknet-module.svg?branch=master)](https://travis-ci.org/vjrantal/iot-edge-darknet-module)

Sample module for IoT Edge that uses [Darknet](https://github.com/pjreddie/darknet) for object detection.

When run in the context of [Azure IoT Edge](https://azure.microsoft.com/en-us/services/iot-edge/), this module will send the objects detected from a camera feed to the cloud.

For example, if the camera sees a view such as below:

![Sample view from camera](https://user-images.githubusercontent.com/207474/39513881-5a658de0-4dfe-11e8-9074-d9cbedb28fea.png)

The data sent to the cloud would contain something like:

```
[
  [
    "backpack", // label
    0.7220373749732971, // probability
    [ // bounding box
      125.79165649414062,
      330.9345397949219,
      177.0498046875,
      230.3690948486328
    ]
  ],
  [
    "car",
    ...
  ],
  [
    "cup",
    ...
  ]
]
```

Below instructions to run locally (testing it out does not require GPU or connected camera), on a GPU virtual machine and on [Jetson TX2](https://developer.nvidia.com/embedded/buy/jetson-tx2) (or Drive PX2).

# Running locally

```
docker run vjrantal/iot-edge-darknet-module
```

Above should work on any machine and without the IoT Edge runtime. The code within above image has conditional functionality depending on if run within the IoT Edge context and whether a camera is detected (loops the included static image if camera not found).

# Building docker images

```
docker build -f base/Dockerfile -t vjrantal/iot-edge-darknet-base .
docker build -f azure-iot-sdk-python/Dockerfile -t vjrantal/azure-iot-sdk-python .
docker build -f darknet/Dockerfile -t vjrantal/darknet .
docker build -t vjrantal/iot-edge-darknet-module .
```

# Deploying to IoT Edge

If you have installed the [extension for Azure CLI 2.0](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-create-deployment-with-cli-iot-extension), you can deploy the pre-built docker image with command like:

```
az iot edge set-modules --device-id <device-id> --hub-name <hub-name> --content deployment.json
```

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

# Running on Jetson TX2 (or Drive PX2)

The architecture of the Jetson TX2 device is:

```
root@tegra-ubuntu:~# uname -m
aarch64
```

There is currently no release of the IoT Edge runtime for that particular architecture so following the [installation instructions](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux) as is does not work.

Instead of installing the runtime like [here](https://docs.microsoft.com/en-us/azure/iot-edge/quickstart-linux#install-and-configure-the-iot-edge-security-daemon) you can install the pre-built runtime version 1.0.2 that can be downloaded [here](https://github.com/vjrantal/iot-edge-darknet-module/files/2423742/iotedge-libiothsm-std-aarch64.zip). After unzipping, the packages can be installed with:

```
sudo dpkg -i libiothsm-std-1.0.2-aarch64.deb
sudo dpkg -i iotedge_1.0.2-1_aarch64.deb
```

Also, since IoT Edge has not published images for this exact architecture, the default configurations will fail. The daemon must be configured to pull in the arm32 image for all system modules, which can be achieved with this change in the configuration file:

```
diff /etc/iotedge/config.yaml.orig /etc/iotedge/config.yaml
74c74
<     image: "mcr.microsoft.com/azureiotedge-agent:1.0"
---
>     image: "mcr.microsoft.com/azureiotedge-agent:1.0.0-linux-arm32v7"
<     image: "mcr.microsoft.com/azureiotedge-hub:1.0"
---
>     image: "mcr.microsoft.com/azureiotedge-hub:1.0.0-linux-arm32v7"
```

The IoT Edge Hub image is chosen during deployment and one can see an example at [./jetson-tx2/deployment.json](./jetson-tx2/deployment.json).

Deployment can be done with a command like:

```
az iot edge set-modules --device-id <device-id> --hub-name <hub-name> --content ./jetson-tx2/deployment.json
```

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

## Default docker engine

If you want to use GPU within the deployed Edge modules, configure the default docker runtime to be `nvidia`.
For example, if you run docker on Ubuntu via systemd, you can edit the file `/etc/docker/daemon.json` to contain:

```
    "default-runtime": "nvidia"
```

And then run `sudo service docker restart` to make the change effective.

If you had Edge already running, it is good to run `iotedgectl restart` and after that, verify that containers gets started with the `nvidia` runtime with a command such as:

```
docker inspect iot-edge-darknet-module | grep Runtime
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
