FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y git

RUN git clone https://github.com/pjreddie/darknet.git
WORKDIR /darknet
RUN git checkout 80d9bec20f0a44ab07616215c6eadb2d633492fe
RUN apt-get install -y libopencv-dev pkg-config wget
RUN make

RUN wget https://pjreddie.com/media/files/yolo.weights

#RUN cp libdarknet.so python/darknet.py /
