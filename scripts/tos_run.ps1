$home_dir = $args[0]  # get the base directory to work from

# stop and remove the container if it exists
docker container stop tos
docker container rm tos

set-location -path "${home_dir}\dev\docker\nginx_flask"  # cd to the docker build directory

# copy requirements file to build dir
copy-item "${home_dir}\dev\tos\requirements.nix" -Destination "."

docker build --tag tos .  # build the image, no cache b/c docker is ignoring changes

set-location -path "${home_dir}\dev\tos"  # change to the flask app directory - don't recall why?

# setup the docker command w/variables replaced, then execute it
$docker_run = "docker run -idt --rm --name tos --hostname tos -v ${home_dir}\www:/usr/share/nginx/html -v ${home_dir}\dev\tos\tos:/tos -p 9080:80 tos"
iex -command $docker_run

# pip install requirements, in case they changed
docker exec tos sh -c "python3 -m pip install -r /requirements.nix"

# run the uwsgi app server w/the app
docker exec -it tos sh -c "uwsgi --ini tos.ini --daemonize2 /var/log/uwsgi.log && /bin/bash"