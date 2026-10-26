# Clúster de 3 servidores con el almacenamiento de tu laptop

Requisito: Docker Desktop (o Docker + Compose) instalado.

## Iniciar
    cd cluster3
    docker compose up -d

## Probar (el balanceador reparte entre los 3 servidores)
    curl http://localhost:8080/                       # repite varias veces: cambia "atendido_por"
    curl -X POST "http://localhost:8080/guardar?nombre=hola.txt&donde=compartido" -d "hola mundo"
    curl -X POST "http://localhost:8080/guardar?nombre=solo.txt&donde=local" -d "dato local"
    curl http://localhost:8080/archivos

## Dónde quedan tus datos (en tu laptop, dentro de esta carpeta)
- almacenamiento/compartido : visible por los 3 servidores
- almacenamiento/s1, s2, s3 : carpeta propia de cada servidor

## Probar tolerancia a fallos
    docker compose stop s2     # el sistema sigue respondiendo con s1 y s3
    docker compose start s2

## Detener
    docker compose down        # tus archivos se conservan en ./almacenamiento
