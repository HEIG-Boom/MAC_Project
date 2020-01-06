echo "----- Deploying -----"

# Check for needed software
echo "----- Download openssh -----"
apt-get install openssh

# SSH config
echo "----- SSH Config -----"
mkdir -p ~/.ssh
chmod 700 ~/.ssh

eval "$(ssh-agent -s)"
echo "$PROD_SERVER_PRIVATE_KEY" | tr -d '\r' | ssh-add - > /dev/null

ssh-keyscan -H $PROD_HOSTNAME >> ~/.ssh/known_hosts
chmod 644 ~/.ssh/known_hosts

# Commands in remote host
echo "----- Setup vars, run updated containers -----"
ssh -T $PROD_SERVER_USER@$PROD_HOSTNAME << EOF
    cd /MACBot

    # Update sources
    git pull origin master

    # Update containers with minimal downtime
    docker-compose down
	  docker-compose up --build -d
EOF
