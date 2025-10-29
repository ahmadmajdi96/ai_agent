#!/bin/bash
set -e

ENVIRONMENT=$1
COMMIT_SHA=$2
APP_NAME="ai_agent"
REGISTRY_URL="tcp://157.180.69.112:5000"

echo "🚀 Deploying $APP_NAME to $ENVIRONMENT environment..."
echo "Commit: $COMMIT_SHA"

# Set environment-specific variables
case $ENVIRONMENT in
  "dev")
    DOMAIN="dev.ai_agent.cortanexai.com"
    REPLICAS=1
    ;;
  "prod")
    DOMAIN="ai_agent.cortanexai.com"
    REPLICAS=2
    ;;
  *)
    echo "❌ Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

STACK_NAME="$APP_NAME-$ENVIRONMENT"


STACK_NAME="$APP_NAME-$ENVIRONMENT"

echo "📦 Pulling latest image..."
docker pull $REGISTRY_URL/$APP_NAME:$ENVIRONMENT-latest

echo "📝 Creating docker-compose file..."
cat > docker-compose.$ENVIRONMENT.yml << DOCKERCOMPOSE
version: '3.8'
services:
  app:
    image: $REGISTRY_URL/$APP_NAME:$ENVIRONMENT-latest
    deploy:
      replicas: $REPLICAS
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    networks:
      - traefik-public
    labels:
      - "traefik.enable=true"
      - "traefik.docker.network=traefik-public"
      - "traefik.http.services.$STACK_NAME.loadbalancer.server.port=9991"
      - "traefik.http.routers.$STACK_NAME.rule=Host(\`$DOMAIN\`)"
      - "traefik.http.routers.$STACK_NAME.entrypoints=web"

networks:
  traefik-public:
    external: true
DOCKERCOMPOSE

echo "🎯 Deploying stack: $STACK_NAME"
docker stack deploy -c docker-compose.$ENVIRONMENT.yml $STACK_NAME --with-registry-auth

echo "⏳ Waiting for deployment to stabilize..."
sleep 30

echo "🔍 Checking service status..."
docker service ls | grep $STACK_NAME || echo "Service not found yet, might still be starting..."

echo "✅ Deployment completed for $DOMAIN"