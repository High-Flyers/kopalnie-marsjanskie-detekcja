Narzędzia i kod wspierający tworzenie modelu do detekcji obrazu na konkurs kopalnie marsjańskie w ramach Droniady 2024

Komenda do uruchomienia modelu do trenowania:
```sh
yolo task=detect mode=train model=yolov8n.pt imgsz=640 data=kopalnie_v8.yaml epochs=50 batch=16 name={name} cache 
```
Komenda powinna być uruchomiona z poziomu katalogu zawierającego plik `kopalnie_v8.yaml` (katalog `model`).

[Plan projektu](https://app.clickup.com/9005008627/v/b/6-901202027603-2)

### Docker
Build - if it is not avalible on docker hub or you introduced some modifications in image
```bash
docker build -f docker/Dockerfile-minimal-intel-ros -t highflyers/martian-minimal-intel-ros .
```
#### Run - with main simulation
Run uav_simulation container according to a readme from repo [uav_simulation](https://github.com/High-Flyers/uav_simulation)

Run the container with martian mines main system:

```bash
    # replace <path_to_repo> with the absolute path, for example: /home/user/Documents/repos/martian-mines-object-detection
docker run --privileged --rm --gpus all -it --net host --ipc host \                  
    -e DISPLAY=${DISPLAY} \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    -e ROS_DOMAIN_ID=0 \
    -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
    -v <path_to_repo>/ros:/home/docker/ws/src/ \
    highflyers/martian-minimal-intel-ros /bin/bash
```
Build ros workspace and source setup script
```
catkin build
source devel/setup.bash
```
Run our detector - it should show a preview of video from simulation, with marked detected objects.
```
roslaunch martian-mines detector.launch 
```