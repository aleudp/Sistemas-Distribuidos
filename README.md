<h1 align="center" id="title">Tarea 1 SD</h1>

<p id="description">Sistema de caché para solicitudes DNS</p>

<h2>🚀 Demo</h2>

[https://www.youtube.com/watch?v=Rh7tPnaVEhw](https://www.youtube.com/watch?v=Rh7tPnaVEhw)

<h2>🛠️ Installation Steps:</h2>

<p>1. Descargar dataset y extraer archivo csv dentro del directorio principal del proyecto..</p>

```
https://www. kaggle.com/datasets/domainsindex/secondlevel-domains-listzone-file
```

<p>2. Ingresar a directorio principal del proyecto y construir los contenedores.</p>

```
docker compose build
```

<p>3. Cambiar puerto de base de datos postgres_memory en el archivo postres.conf cambiar línea:</p>

```
#Port 5432
```

```
Port 5433
```

<p>5. Editar la cantidad de memoria y criterio de remoción dentro de dockercompose.yml</p>

<p>6. Cambiar parámetros en archivo server.py dentro del directorio server acorde a la cantidad de particiones que se desea utilizar.</p>

```
PARTITION=                                 
```

```
Partition
```

<p>8. Levantar los contenedores utilizando:</p>

```
docker compose up
```

<p>9. Puede acceder directamente a la base de datos en postgres.</p>

```
docker exec -it  psql -U user -d dns_cache
```

<p>10. Puede ingresar al cache de Redis para ver los dominios presentes utilizando:</p>

```
docker exec -it "contenedor" redis-cli
```

<p>11. Extraer resumen de resultados:</p>

```
python3 datos.py
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Redis
*   Docker
*   Python
*   Docker Compose
*   Kaggle
*   Youtube
*   ChatGPT
