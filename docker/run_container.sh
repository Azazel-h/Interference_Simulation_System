port="4000"
if [ $# -eq 1 ]; then
	port=$1
fi

echo "Building image..."

docker build .. --tag interferometer

if [ $? -ne 0 ]; then
	echo "Building error"
	exit 1
fi

dir="$(pwd)"
parent="$(dirname "$dir")"

echo "Running on port: $port..."
docker run --rm -it -p "$port":8000 -v "$parent":/project interferometer

if [ $? -ne 0 ]; then
	echo "Running error"
	exit 1
fi
