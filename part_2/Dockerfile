FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
        build-essential \
        cmake \
        g++ \
        gcc \
        mc
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .


#RUN mkdir build && cd build && cmake .. && make && ls -l

RUN rm -rf build/* && cd build && cmake .. && make # && ls -l && sleep 11

CMD ["./build/MathClient/MathClient"]
