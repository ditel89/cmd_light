echo "Down load docker image"
docker pull ditel89/light-control:v1.1

sleep 1

echo "setting config.cfg"
echo -e "URL=ketibnt.iptime.org\nPORT=3883\nTOPIC_CMD=light/cmd\nTOPIC_STATUS=light/status" > config.cfg
echo -e "INTERVAL=3\nDEVICE=/dev/ttyTHS0" >> config.cfg

sleep 2

echo "setting docker run script"
echo "docker run -it --name light-control --rm --device=/dev/ttyTHS0 --env-file config.cfg ditel89/light-control:v1.1" > run_cmdLigth.sh

chmod +x run_cmdLigth.sh

sleep 2

echo "setting device /dev/ttyTHS0"

sudo adduser $USER tty

sudo systemctl disable nvgetty.service

echo "reboot after 5sec"

sleep 5

sudo reboot