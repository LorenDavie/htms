dropdb makesense
createdb makesense
./local.sh migrate auth
./local.sh migrate contenttypes
./local.sh migrate

