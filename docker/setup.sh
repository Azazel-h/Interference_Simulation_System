if [ ! -f /.dockerenv ]; then
	echo "Not in container!"
	exit 1
fi

if [ ! -d "/project" ]; then
	echo "Directory not mounted!"
	exit 1
fi

cd /project
./manage.py makemigrations fabry_perot
./manage.py makemigrations michelson
./manage.py migrate
./manage.py runserver 0.0.0.0:8000
