$home_dir = $args[0]

write-output $home_dir

set-location -path "${home_dir}\dev\docker\nginx_flask"

docker build --tag tos .

set-location -path "${home_dir}\dev\tos"

$docker_run = "docker run -idt --rm --name tos --hostname tos -v ${home_dir}\www:/usr/share/nginx/html -v ${home_dir}\dev\tos:/tos -p 9080:80 tos"

iex -command $docker_run

docker exec -it tos sh -c "uwsgi --ini tos.ini --daemonize2 /var/log/uwsgi.log && /bin/bash"