# Actividad 5: Orquestación de Infraestructura con Docker Compose

## Descripción del Proyecto
Este proyecto representa la consolidación del módulo de infraestructura, transformando un pipeline de datos aislado en una solución integrada, automatizada y orquestada mediante **Docker Compose**. La arquitectura implementada opera bajo el principio de Infraestructura como Código (IaC), permitiendo el despliegue de servicios distribuidos con un control unificado.

## Componentes de la Infraestructura Orquestada
El archivo `docker-compose.yml` gestiona el ciclo de vida, las redes y la interacción de los siguientes elementos:
* **Servicio de Procesamiento:** Ejecuta de forma automática el pipeline modular bajo la arquitectura Medallion (`pipeline_paralelo.py`).
* **Persistencia de Volúmenes:** Configuración de almacenamiento persistente para asegurar que los datos procesados en las capas `bronze`, `silver` y `gold` no se pierdan al apagar o reiniciar los contenedores.
* **Entorno Científico (`notebooks/`):** Directorio estructurado para montar entornos interactivos (como Jupyter Notebooks) enfocados en consumir la data limpia de la capa Gold para desplegar reportería analítica avanzada.

## Ventajas del Despliegue Automatizado
1. **Reproducibilidad Absoluta:** El entorno completo se levanta idéntico en cualquier máquina de desarrollo, pruebas o producción.
2. **Eficiencia Operacional:** Redes internas, compilación de imágenes y montaje de volúmenes se configuran automáticamente con un comando unificado.

## Instrucciones de Despliegue
Para levantar la infraestructura completa de forma automatizada y verificar el pipeline, sitúese en la raíz del proyecto y ejecute:
```bash
docker compose up --build
