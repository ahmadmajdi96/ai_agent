ENVIRONMENT=$1
COMMIT_SHA=$2
APP_NAME="ai_agent"
REGISTRY_URL="157.180.69.112:5000"

echo "🚀 Deploying $APP_NAME to $ENVIRONMENT environment..."
echo "Commit: $COMMIT_SHA"

case $ENVIRONMENT in
  "dev")
    REPLICAS=1
    RULE="Host(\`157.180.69.112\`)"
    ;;
  "prod")
    REPLICAS=2
    RULE="Host(\`157.180.69.112\`)"
    ;;
  *)
    echo "❌ Unknown environment: $ENVIRONMENT"
    exit 1
    ;;
esac

STACK_NAME="$APP_NAME-$ENVIRONMENT"

echo "📦 Pulling latest image..."
if ! docker pull $REGISTRY_URL/$APP_NAME:$ENVIRONMENT-latest; then
    echo "❌ ERROR: Image $REGISTRY_URL/$APP_NAME:$ENVIRONMENT-latest not found in registry!"
    echo "💡 Check GitHub Actions build logs - the image was never built/pushed"
    exit 1
fi

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
      - "traefik.http.services.$STACK_NAME.loadbalancer.server.port=8000"
      - "traefik.http.routers.$STACK_NAME.rule=$RULE"
      - "traefik.http.routers.$STACK_NAME.entrypoints=web"

networks:
  traefik-public:
    external: true
DOCKERCOMPOSE

echo "🎯 Deploying stack: $STACK_NAME"
docker stack deploy -c docker-compose.$ENVIRONMENT.yml $STACK_NAME --with-registry-auth

echo "⏳ Waiting for deployment..."
sleep 30

echo "✅ Deployment completed!"
echo "🌐 Access at: http://157.180.69.112"

