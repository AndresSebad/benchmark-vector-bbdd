#!/bin/bash

# Construir imagen de Docker
echo "Construyendo imagen de Docker..."
START_BUILD=$(date +%s)
docker-compose build
END_BUILD=$(date +%s)
BUILD_TIME=$((END_BUILD - START_BUILD))
echo "Tiempo de construcción: $BUILD_TIME segundos"

# Iniciar contenedores
echo "Iniciando contenedores..."
docker-compose up -d

# Espera para asegurar que los contenedores están corriendo
sleep 10

# Inspeccionar el contenedor de la aplicación
APP_CONTAINER="pg_application"  # Asegúrate de que este sea el nombre correcto
echo "Inspeccionando el contenedor: $APP_CONTAINER"
docker inspect $APP_CONTAINER

# Agregar aquí cualquier otra métrica o comando que desees ejecutar
