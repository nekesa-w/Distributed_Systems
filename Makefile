# Variables
IMAGE_NAME := loadbalancer
DOCKERFILE := Dockerfile2
DOCKER_COMPOSE_FILE := docker-compose.yml

# Build the Docker image
build:
    @docker build -t $(IMAGE_NAME) -f $(DOCKERFILE) .

# Run the load balancer container
run:
    @docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Stop and remove the load balancer container
stop:
    @docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Remove the Docker image
clean:
    @docker rmi $(IMAGE_NAME)
