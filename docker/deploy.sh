echo "----- Deploying -----"
# Commands in remote host
echo "----- Setup vars, run updated containers -----"
cd /MACBot/docker

# Update sources
git pull origin master

# Source env vars
source env-file

# Update containers with minimal downtime
docker-compose down
docker-compose up --build -d
