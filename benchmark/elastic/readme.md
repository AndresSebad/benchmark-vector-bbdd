# Recolección de imágenes
For ElasticSearch:
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.11.3

For kibana:
docker pull docker.elastic.co/kibana/kibana:8.11.3

# Entorno 
* Windows 11
* RAM 16 GB
* Docker Desktop

# Instancias
docker run --name es01 -c 1024 -m 2048mb --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.11.3

docker run --name kibana -c 1024 -m 786mb --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.11.3

# Pasos a seguir

1. Instalar Docker Desktop
2. Abrir Docker Desktop
3. En consola correr la recolección de imágenes
4. En consola, ejecutar los comandos para crear las instancias
5. Para configurar Kibana, abrir localhost:5601. Insertar el enrollment key que apareció tras correr la instancia de Elastic. Si no es aceptado, ver https://www.elastic.co/guide/en/elasticsearch/reference/current/create-enrollment-token.html y usar elasticsearch-create-enrollment-token -s kibana. Copiar el nuevo key.
6. Copiar el certificado del contenedor al computador con docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
7. Activar el certificado en el computador
8. Abrir en Colab el notebook correspondiente
9. Conectar Colab al runtime local como se ve aquí: https://research.google.com/colaboratory/local-runtimes.html
10. Reemplazar los datos de autenticación con los otorgados por la instancia de Elastic
11. Correr el notebook
