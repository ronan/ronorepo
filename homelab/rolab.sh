#!/bin/bash

ARCH="amd64";
DIST="debian.12~bookworm_$ARCH"
BASE="https://download.docker.com/linux/debian/dists/bookworm/pool/stable/$ARCH";

PKGS=( \
  "containerd.io_1.6.26-1_$ARCH.deb" \
  "docker-ce_24.0.7-1~$DIST.deb" \
  "docker-ce-cli_24.0.7-1~$DIST.deb" \
  "docker-buildx-plugin_0.11.2-1~$DIST.deb" \
  "docker-compose-plugin_2.21.0-1~$DIST.deb" \
)

for pkg in $PKGS; do
  curl $BASE/$pkg -o /tmp/$pkg
  sudo dpkg -i /tmp/$pkg
done

PASS=`docker run --rm httpd:2.4-alpine htpasswd -nbB admin "portaineradmin" | cut -d ":" -f 2`;
echo $PASS > ~/portainer-admin-password.txt
sudo docker-composer up -f ./docker-compose.yml

sudo docker run -d -p 8000:80 -p 9443:443 \
          --name portainer --restart=always \
          -v /var/run/docker.sock:/var/run/docker.sock \
          -v portainer_data:/data portainer/portainer-ce:latest \
          --admin-password="$ENC";
