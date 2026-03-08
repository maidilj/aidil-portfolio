pytho# Portfolio Deployment Guide

## Run Locally (Day 1 — test this first)

```bash
cd portfolio
pip install flask
python app.py
# Open: http://localhost:5000
```

---

## Docker (Day 2 — Morning)

### Build & test locally
```bash
docker build -t aidil-portfolio .
docker run -p 5000:5000 aidil-portfolio
# Open: http://localhost:5000
```

### Push to Docker Hub
```bash
docker login
docker tag aidil-portfolio YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
docker push YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
```

---

## Deploy to AWS EC2 (Day 2 — Afternoon)

### Step 1 — Launch EC2 instance
1. Go to AWS Console → EC2 → Launch Instance
2. Choose: **Ubuntu Server 22.04 LTS** (free tier eligible)
3. Instance type: **t2.micro** (free tier)
4. Create or select a key pair (.pem file) — save it somewhere safe
5. Security Group — add these inbound rules:
   - SSH: port 22, source: My IP
   - Custom TCP: **port 80**, source: Anywhere (0.0.0.0/0)
   - Custom TCP: **port 5000**, source: Anywhere (0.0.0.0/0)
6. Launch instance

### Step 2 — SSH into your instance
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3 — Install Docker on EC2
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
# Log out and back in for group change to take effect
exit
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 4 — Pull and run your container
```bash
docker pull YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
docker run -d -p 80:5000 --restart always YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
```

### Step 5 — Share the link
Your portfolio is now live at:
```
http://YOUR_EC2_PUBLIC_IP
```
Share this URL with interviewers. 

---

## Updating the site
```bash
# On your local machine:
docker build -t aidil-portfolio .
docker tag aidil-portfolio YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
docker push YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest

# On EC2:
docker pull YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
docker stop $(docker ps -q)
docker run -d -p 80:5000 --restart always YOUR_DOCKERHUB_USERNAME/aidil-portfolio:latest
```

---

## Common Issues

**Port 5000 not accessible?**
Check EC2 Security Group has port 5000 (or 80) open to 0.0.0.0/0

**Container exits immediately?**
Run `docker logs $(docker ps -lq)` to see the error

**Fonts not loading?**
The site uses Google Fonts CDN — make sure the EC2 instance has outbound internet access (it does by default)
