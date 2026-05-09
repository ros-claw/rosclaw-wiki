#!/bin/bash
# ROSClaw Wiki — Production Server One-Click Setup
# Run on: ubuntu@43.160.250.80

set -e

WIKI_DIR="/opt/rosclaw-wiki"
REPO_URL="https://github.com/ros-claw/rosclaw-wiki.git"

echo "=== ROSClaw Wiki Production Setup ==="

# 1. Update system
echo "[1/7] Updating system packages..."
sudo apt-get update -y
sudo apt-get install -y curl git nginx certbot python3-certbot-nginx

# 2. Install Docker
echo "[2/7] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker ubuntu
fi

# 3. Install Docker Compose
echo "[3/7] Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# 4. Clone repository
echo "[4/7] Cloning repository..."
sudo mkdir -p "$WIKI_DIR"
if [ -d "$WIKI_DIR/.git" ]; then
    cd "$WIKI_DIR" && sudo git pull
else
    sudo git clone "$REPO_URL" "$WIKI_DIR"
fi

# 5. Configure environment
echo "[5/7] Configuring environment..."
cd "$WIKI_DIR"
if [ ! -f .env ]; then
    sudo cp .env.example .env
    echo "    Created .env from template. EDIT IT before starting services."
fi

# 6. Build and start services
echo "[6/7] Building and starting services..."
cd "$WIKI_DIR"
sudo docker-compose -f docker-compose.prod.yml build
sudo docker-compose -f docker-compose.prod.yml up -d

# 7. Configure SSL
echo "[7/7] Configuring SSL..."
sudo certbot --nginx -d api.rosclaw.io --non-interactive --agree-tos --email admin@rosclaw.io || true

# 8. Health check
echo ""
echo "=== Setup Complete ==="
sleep 5
sudo docker-compose -f docker-compose.prod.yml ps

echo ""
echo "Health check:"
curl -s http://localhost:8000/wiki/v1/health || echo "API not yet ready (may need SSL config)"
echo ""
echo "Next steps:"
echo "  1. Edit $WIKI_DIR/.env with actual API keys and R2 credentials"
echo "  2. Restart: sudo docker-compose -f docker-compose.prod.yml restart"
echo "  3. Import data: docker exec rosclaw-api python import_to_seekdb.py ..."
