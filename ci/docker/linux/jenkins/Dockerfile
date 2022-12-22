FROM ubuntu:20.04
COPY ci/docker/linux/jenkins/apt-packages.txt /tmp/
RUN apt update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    cat /tmp/apt-packages.txt | xargs apt-get -y install
ARG PIP_EXTRA_INDEX_URL
ARG PIP_INDEX_URL
COPY requirements/ /tmp/requirements/requirements/
COPY requirements-ci.txt /tmp/requirements/
RUN pip install -r /tmp/requirements/requirements-ci.txt
