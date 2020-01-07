echo "----- Deploying -----"
# Commands in remote host
echo "----- Setup vars, run updated containers -----"
cd /MACBot/docker

rm env-file

# Update sources
git pull origin master

echo "TELEGRAM_TOKEN=$TELEGRAM_TOKEN" > env-file

# Update containers with minimal downtime
docker-compose down
docker-compose up --build -d
