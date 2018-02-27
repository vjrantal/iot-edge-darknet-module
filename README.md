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
