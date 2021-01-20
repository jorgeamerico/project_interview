# project_interview

Projeto feito em debian10 e py3

ajustes no S.O.

apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget python3-pip redis-server net-tools
$python3 -m pip install redis
$python3 -m pip install flask


Desafio A. POP
curl -H "Content-Type: application/json" -X POST http://x.x.x.x:5000/api/queue/pop

Desafio B. PUSH
curl -H "Content-Type: application/json" -X POST -d "{\"\"thing\":\"CBR\"}" http://x.x.x.x:5000/api/queue/push

Desafio B. COUNT
curl -H "Content-type: application/json" -X GET http://x.x.x.x:5000/api/queue/count
