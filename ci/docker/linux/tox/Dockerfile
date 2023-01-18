ARG PIP_FIND_LINKS=/wheels
FROM ubuntu:20.04 as wheel_builder_base
COPY ci/docker/linux/tox/apt-packages.txt /tmp/
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt-get -y install
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL

COPY requirements/ /tmp/requirements
RUN pip3 install -r /tmp/requirements/requirements-tox.txt "devpi-client<6.0"
WORKDIR /src
CMD tox --workdir /tmp/tox --recreate
