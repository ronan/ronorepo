#!/bin/bash

ARCH="amd64";
DIST="debian.12~bookworm_$ARCH"
BASE="https://download.docker.com/linux/debian/dists/bookworm/pool/stable/$ARCH";

DEBIAN_FRONTEND=noninteractive;

apt-get
apt-get update; apg-get upgrade;
apt-get install git curl;

PKGS=("containerd.io_1.6.26-1_$ARCH.deb" "docker-ce_24.0.7-1~$DIST.deb" "docker-ce-cli_24.0.7-1~$DIST.deb" "docker-buildx-plugin_0.11.2-1~$DIST.deb" "docker-compose-plugin_2.21.0-1~$DIST.deb")
for pkg in ${PKGS[@]}; do
  curl $BASE/$pkg -o /tmp/$pkg;
  dpkg -i /tmp/$pkg;
done
apt-get -f install

PASS=`docker run --rm httpd:2.4-alpine htpasswd -nbB admin "portaineradmin" | cut -d ":" -f 2`;
echo $PASS > ~/portainer-admin-password.txt
docker-compose up -f ./docker-compose.yml
