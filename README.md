<!-- // mac -->

install docker

cmd = brew install colima docker docker-compose
cmd = docker --version
cmd = docker compose version
cmd = colima start
cmd = colima start --cpu 2 --memory 2
cmd = colima status

<!-- for run the in debug -->

cmd = docker compose up --build

<!-- for run the in detached mode, prod -->

cmd = docker compose up -d

<!-- // mac close -->
