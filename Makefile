SERVICE1_PATH = bwconverter.yaml
SERVICE2_PATH = sepiaconverter.yaml
SERVICE3_PATH = traffic_splitting.yaml


# Default target to run all commands
all:create_namespace init_services kubectl_get_pods kubectl_get_services kn_service_list

setup:
	@echo "Setting up the environment"
	minikube start
	kubectl get po -A
	kn quickstart minikube
	minikube profile list
	
create_namespace:
	@echo "Creating namespace converter"
	kubectl create namespace converter

init_services:
	@echo "creating services"
	kubectl apply -f $(SERVICE1_PATH) -n converter
	kubectl apply -f $(SERVICE2_PATH) -n converter
	kubectl apply -f $(SERVICE3_PATH) -n converter

kubectl_get_pods:
	@echo "Running kubectl get pods"
	kubectl get pods

kubectl_get_services:
	@echo "Running kubectl get services"
	kubectl get services

kn_service_list:
	@echo "Running kn service list"
	kn service list -A


# Clean target (optional)
clean:
	@echo "Cleaning up..."
	# Add any clean-up commands here
