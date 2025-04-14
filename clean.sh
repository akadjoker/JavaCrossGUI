docker rmi -f $(docker images -q)
docker builder prune -a
docker build -t luisakadjoker/javafx-builder .
docker push luisakadjoker/javafx-builder:latest

xhost +local:docker  

python3 builder.py --create com.djokersoft.simplegame SimpleGame


python3 builder.py --create com.djokersoft.simplegame SimpleGame


docker run -it --rm   -v $PWD/samples:/app/samples  luisakadjoker/javafx-builder   samples/HelloWorld --create com.djokersoft.simplegame SimpleGame

docker run -it --rm   -v $PWD/samples:/app/samples  luisakadjoker/javafx-builder   samples/SimpleGame com.djokersoft.simplegame --target desktop --name SimpleGame --run

docker run -it --rm   -v $PWD/samples:/app/samples  luisakadjoker/javafx-builder   samples/SimpleGame --create com.djokersoft.simplegame SimpleGame


python3 builder.py samples/SimpleGame com.djokersoft.simplegame --target desktop --name SimpleGame --run
python3 builder.py samples/SimpleGame com.djokersoft.simplegame --target android --name SimpleGame --run

docker run -it --rm   -e DISPLAY=$DISPLAY   -v /tmp/.X11-unix:/tmp/.X11-unix   -v $PWD/samples:/app/samples   luisakadjoker/javafx-builder samples/SimpleGame com.djokersoft.simplegame --target desktop --name SimpleGame --run

