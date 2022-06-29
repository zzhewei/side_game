# Side Game

***

## If you want to generate requirements.txt
**pipreqs ./ --encoding=utf8 --force** 

## create docker compose by docker-compose.yml
**1. change config.py mysql setting**

**2. enter "docker-compose up -d" and wait for mysql init**

**3. enter "docker exec -it 'flaskname' /bin/bash"**

**4. enter "python -m flask init" to init table data**