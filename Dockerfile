FROM resin/rpi-raspbian

# switch on systemd init system in container
ENV INITSYSTEM on
ENV READTHEDOCS True
ENV VERSION=0.0.1

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        pkg-config \
        python2.7 \
        python-dev \
        rsync \
        rpi-update \
        wget \
        unzip

# clean up dependencies
RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

# install pip
RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
        rm get-pip.py

# copy sources
COPY . /app
WORKDIR /app

# pip install python deps from requirements.txt
# for caching until requirements.txt changes
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# update Raspberry firmwares
RUN rpi-update

# set timezone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# video libraries (https://raspberrypi.stackexchange.com/questions/34107/libmmal-core-so-missing)
RUN echo /opt/vc/lib > pi_vc_core.conf && chown root.root pi_vc_core.conf && mv pi_vc_core.conf /etc/ld.so.conf && ldconfig

# run robot
CMD ["bash", "start.sh"]
