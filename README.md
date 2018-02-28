# IoT Edge Darknet module

Sample module for IoT Edge that uses [Darknet](https://github.com/pjreddie/darknet) for object detection.

# Deploying to IoT Edge

If you have installed the [extension for Azure CLI 2.0](https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-create-deployment-with-cli-iot-extension), you can deploy the pre-built docker image with command like:

```
az iot hub apply-configuration --device-id <device-id> --hub-name <hub-name> --content deployment.json
```

# Building docker images

```
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
