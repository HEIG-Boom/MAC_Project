echo "----- Deploying -----"
# Commands in remote host
echo "----- Setup vars, run updated containers -----"
cd /MACBot/docker

# Update sources
git pull origin master

# Update containers with minimal downtime
dockr-compose down
docker-compose up --build -d
