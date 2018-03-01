FROM vjrantal/iot-edge-darknet-base

ARG gpu

WORKDIR /

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
RUN git checkout 80d9bec20f0a44ab07616215c6eadb2d633492fe
RUN apt-get install -y libopencv-dev pkg-config wget

RUN sed -i 's/OPENCV=0/OPENCV=1/g' Makefile
RUN if [ "x$gpu" = "x1" ] ; then sed -i 's/GPU=0/GPU=1/g' Makefile ; fi

RUN make

RUN wget https://pjreddie.com/media/files/yolo.weights
