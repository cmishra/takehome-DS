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
   docker run -p 8888:8888 -it --rm -v `pwd`:/workingdir \
       $IMAGE
}
