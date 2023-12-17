# Home Lab Stuff

edge:

- Translates nDNS hosts (dashboard.local) to IP:Port combo (192.168.0.245:8484).
- Pretty much just needs to handle http(s).
- Should speak https with self signed certs and talk internall to whichever (ignoring upstream certs).
- Broadcasts mdns for services that can't (or maybe all for consistency)
- Firewall?
- VPN?
- Cloudflare?
- traefik

dashboard:

- Links to all the other stuff
- Integrates with key store for automatic login
- Or whatever

portainer:

- Check on and play with docker
- Anything done should be "freezable" to a version controlled contrib

proxmox:

- Check on VM and LVX container.

haos:

- Custom deb? distro for running home assistant
- Do I need this?

containers.local:

- An LXC in proxmox
- Do I need this to be an LXC?
- Put it in a docker with everything else
- rancheros?
- boot2docker?
- debian + docker + docker-compose ?


```bash
docker run  \
        --name=Heimdall \
        --volume=0e0004561b091df4fcce602e252fdc49ced867160a8a1db305865ead31d4191b:/config \
        --network=zone \
        --restart=unless-stopped \
        --detach=true \
        lscr.io/linuxserver/heimdall:latest


docker run \
    -p 8000:8000 \
    -p 9443:9443 \
 \
    --restart=unless-stopped \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data portainer/portainer-ce:latest

```

## Home Lab First Server
Name:       rolab1
Address:    rolab1.local
Hardware:   HP1


### Install process

- Install Proxmox
  - https://enterprise.proxmox.com/iso/proxmox-ve_8.1-1.iso
- Pull and load docker-compose.yml
- Ansible?
- 