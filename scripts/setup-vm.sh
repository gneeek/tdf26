#!/bin/bash
# Set up a fresh Ubuntu VM for hosting the Correze Travelogue static site.
#
# Usage: sudo ./setup-vm.sh <domain>
# Example: sudo ./setup-vm.sh tour26.iamsosmrt.com
#
# Run this on the VM after initial SSH setup.
# Idempotent — safe to run multiple times.

set -e

if [ "$EUID" -ne 0 ]; then
    echo "Error: Run with sudo"
    exit 1
fi

DOMAIN="${1:-}"
if [ -z "$DOMAIN" ]; then
    echo "Usage: sudo ./setup-vm.sh <domain>"
    echo "Example: sudo ./setup-vm.sh tour26.iamsosmrt.com"
    exit 1
fi

SITE_DIR="/var/www/correze-travelogue"
DEPLOY_USER="deploy"

echo "=== Correze Travelogue VM Setup ==="
echo "Domain: $DOMAIN"
echo "Site dir: $SITE_DIR"
echo ""

# --- Step 1: System updates ---
echo "--- Step 1: Updating system packages ---"
apt-get update -qq
apt-get upgrade -y -qq
echo ""

# --- Step 2: Create deploy user ---
echo "--- Step 2: Creating deploy user ---"
if id "$DEPLOY_USER" &>/dev/null; then
    echo "User $DEPLOY_USER already exists."
else
    useradd -m -s /bin/bash "$DEPLOY_USER"
    echo "Created user $DEPLOY_USER."
fi

# Set up SSH for deploy user (copy authorized_keys from root/current user)
DEPLOY_HOME=$(eval echo ~$DEPLOY_USER)
mkdir -p "$DEPLOY_HOME/.ssh"
if [ -f /root/.ssh/authorized_keys ]; then
    cp /root/.ssh/authorized_keys "$DEPLOY_HOME/.ssh/authorized_keys"
elif [ -f "$HOME/.ssh/authorized_keys" ]; then
    cp "$HOME/.ssh/authorized_keys" "$DEPLOY_HOME/.ssh/authorized_keys"
fi
chown -R "$DEPLOY_USER:$DEPLOY_USER" "$DEPLOY_HOME/.ssh"
chmod 700 "$DEPLOY_HOME/.ssh"
chmod 600 "$DEPLOY_HOME/.ssh/authorized_keys" 2>/dev/null || true
echo ""

# --- Step 3: Create site directory ---
echo "--- Step 3: Creating site directory ---"
mkdir -p "$SITE_DIR"
chown -R "$DEPLOY_USER:$DEPLOY_USER" "$SITE_DIR"

# Placeholder index
if [ ! -f "$SITE_DIR/index.html" ]; then
    echo "<html><body><h1>$DOMAIN</h1><p>Coming soon.</p></body></html>" > "$SITE_DIR/index.html"
    chown "$DEPLOY_USER:$DEPLOY_USER" "$SITE_DIR/index.html"
fi
echo "Site directory: $SITE_DIR"
echo ""

# --- Step 4: Install Caddy ---
echo "--- Step 4: Installing Caddy ---"
if command -v caddy &>/dev/null; then
    echo "Caddy already installed: $(caddy version)"
else
    apt-get install -y -qq debian-keyring debian-archive-keyring apt-transport-https curl
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
    apt-get update -qq
    apt-get install -y -qq caddy
    echo "Caddy installed: $(caddy version)"
fi
echo ""

# --- Step 5: Configure Caddy ---
echo "--- Step 5: Configuring Caddy ---"
cat > /etc/caddy/Caddyfile << EOF
$DOMAIN {
    root * $SITE_DIR
    file_server
    encode gzip

    handle_errors {
        rewrite * /404.html
        file_server
    }

    header {
        # Cache static assets
        /gpx/* Cache-Control "public, max-age=86400"
        /_nuxt/* Cache-Control "public, max-age=31536000, immutable"
    }
}
EOF

echo "Caddyfile written for $DOMAIN"
echo ""

# --- Step 6: Configure firewall ---
echo "--- Step 6: Configuring firewall ---"
if command -v ufw &>/dev/null; then
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw allow 22/tcp
    ufw --force enable
    echo "Firewall configured: 80, 443, 22 allowed."
else
    echo "ufw not found, skipping firewall setup."
fi
echo ""

# --- Step 7: Start Caddy ---
echo "--- Step 7: Starting Caddy ---"
systemctl enable caddy
systemctl restart caddy
echo "Caddy started."
echo ""

# --- Summary ---
echo "=== Setup Complete ==="
echo ""
echo "Domain:      $DOMAIN"
echo "Site dir:    $SITE_DIR"
echo "Deploy user: $DEPLOY_USER"
echo "Web server:  Caddy (auto-SSL via Let's Encrypt)"
echo ""
echo "Next steps:"
echo "  1. Point DNS A record for $DOMAIN to this VM's IP"
echo "  2. Caddy will auto-provision SSL once DNS propagates"
echo "  3. Deploy with: tar -czf - -C .output/public . | ssh $DEPLOY_USER@$DOMAIN \"tar -xzf - -C $SITE_DIR\""
echo ""
