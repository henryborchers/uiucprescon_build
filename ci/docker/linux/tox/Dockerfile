ARG PIP_FIND_LINKS=/wheels
ARG PIP_DOWNLOAD_CACHE=/.cache/pip
FROM ubuntu:20.04 as wheel_builder_base
COPY ci/docker/linux/tox/apt-packages.txt /tmp/
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt-get -y install
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
ARG PIP_FIND_LINKS
ARG PIP_DOWNLOAD_CACHE
RUN mkdir -p ${PIP_FIND_LINKS} && \
    chmod -R 777 ${PIP_FIND_LINKS}
COPY requirements/ /tmp/requirements
RUN mkdir -p ${PIP_DOWNLOAD_CACHE} && \
    pip3 install -r /tmp/requirements/requirements-tox.txt "devpi-client<6.0" && \
    chmod -R 777 ${PIP_DOWNLOAD_CACHE}
ENV PIP_DOWNLOAD_CACHE=${PIP_DOWNLOAD_CACHE}
WORKDIR /src
CMD tox --workdir /tmp/tox --recreate
