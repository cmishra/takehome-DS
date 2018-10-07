function buildName() {
    TAG=$1
    if [[ -z "$TAG" ]]; then
        TAG=$USER
    fi
    echo jupyterlab:$TAG
}

function buildImage() {
    IMAGE=$(buildName $1)
    docker build -t $IMAGE -f Dockerfile .
}

function launchServer() {
   IMAGE=$(buildName $1)
   docker run -it -p 27017:27017 --rm -v `pwd`:/workingdir \
       $IMAGE
}

function runScript() {
    docker exec -it `docker ps -q` python /workingdir/run.py "$@"
}
