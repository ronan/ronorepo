FROM docker.io/library/python:3

RUN apt-get update && apt-get install avahi-utils -y

RUN pip install zeroconf

CMD [ "/usr/bin/avahi-publish-address", "whoami.local", "-R", "192.168.0.250" ]