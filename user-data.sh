#!/bin/bash

apt update -y
apt install -y docker.io awscli

systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

cat <<EOF > /home/ubuntu/start-app.sh
#!/bin/bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 142166253229.dkr.ecr.ap-south-1.amazonaws.com
docker pull 142166253229.dkr.ecr.ap-south-1.amazonaws.com/online-quiz-system:latest
docker stop online-quiz-system || true
docker rm online-quiz-system || true
docker run -d -p 5000:5000 --name online-quiz-system 142166253229.dkr.ecr.ap-south-1.amazonaws.com/online-quiz-system:latest
EOF

chmod +x /home/ubuntu/start-app.sh

# Run at startup
echo "@reboot /home/ubuntu/start-app.sh" >> /var/spool/cron/crontabs/ubuntu