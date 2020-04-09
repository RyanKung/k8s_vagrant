build:
	docker build . -t 192.168.50.10:5000/pong:v1
	docker push 192.168.50.10:5000/pong:v1
	kubectl apply -f depolyment.yml
