FROM debian

RUN apt-get update && apt-get install avahi-utils -y

ADD entrypoint.sh /opt/entrypoint.sh
ADD mdns.service  /etc/systemd/system/mdns.service
ADD avahi-daemon.conf  /etc/avahi/avahi-daemon.conf
RUN chmod 755 /etc/systemd/system/mdns.service;

ENTRYPOINT ["/opt/entrypoint.sh"]