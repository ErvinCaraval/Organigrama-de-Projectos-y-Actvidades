Aquí tienes el archivo `README.md` actualizado para incluir la creación y activación de un entorno virtual Python llamado `env`, tanto para sistemas Linux como Windows, y la instalación de las dependencias desde `requirements.txt`:

```markdown
# Proyecto Web Backend con Docker Compose

Este proyecto utiliza Docker Compose para desplegar un entorno de desarrollo que incluye una aplicación web basada en Django, una base de datos PostgreSQL y pruebas de carga con Locust.

## Requisitos Previos

- Docker
- Docker Compose
- Python 3.x

## Pasos para Desplegar el Entorno

1. **Clonar el Repositorio**

   Primero, clona este repositorio en tu máquina local:

   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. **Crear y Activar el Entorno Virtual (Linux)**

   Crea un entorno virtual llamado `env` y actívalo:

   ```sh
   python3 -m venv env
   source env/bin/activate
   ```

3. **Crear y Activar el Entorno Virtual (Windows)**

   Crea un entorno virtual llamado `env` y actívalo:

   ```cmd
   python -m venv env
   .\env\Scripts\activate
   ```

4. **Instalar Dependencias**

   Instala las dependencias necesarias desde `requirements.txt`:

   ```sh
   pip install -r requirements.txt
   ```

5. **Crear el Archivo `.env`**

   Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables de entorno con los valores correspondientes:

   ```env
   DB_HOST=db
   DB_NAME=nombre_de_tu_bd
   DB_USER=usuario_de_tu_bd
   DB_PASSWORD=contraseña_de_tu_bd
   ```

6. **Construir y Levantar los Servicios**

   Utiliza el siguiente comando para construir las imágenes de Docker y levantar los servicios definidos en el archivo `docker-compose.yml`:

   ```sh
   docker-compose up --build
   ```

7. **Acceder a la Aplicación Web**

   Una vez que los servicios estén corriendo, puedes acceder a la aplicación web en tu navegador en la siguiente URL:

   ```
   http://localhost:8000
   ```

8. **Acceder a la Base de Datos PostgreSQL**

   La base de datos PostgreSQL estará disponible en el puerto 5433 de tu máquina local. Puedes conectarte a ella usando cualquier cliente de base de datos PostgreSQL.

9. **Ejecutar Pruebas con Locust**

   Para acceder a la interfaz web de Locust y ejecutar pruebas de carga, abre tu navegador y dirígete a:

   ```
   http://localhost:8090
   ```

## Servicios Definidos en `docker-compose.yml`

- **web**: Servicio que ejecuta la aplicación Django.
- **db**: Servicio que ejecuta la base de datos PostgreSQL.
- **tests**: Servicio que ejecuta las pruebas de carga con Locust.

## Detalles Técnicos

- El servicio `web` espera 10 segundos antes de iniciar el servidor Django para asegurarse de que la base de datos esté disponible.
- Los volúmenes y redes son gestionados por Docker Compose para facilitar el desarrollo y la persistencia de datos.

## Comandos Útiles de Docker Compose

- **Levantar los servicios**:

  ```sh
  docker-compose up
  ```

- **Detener los servicios**:

  ```sh
  docker-compose down
  ```

- **Reconstruir las imágenes**:

  ```sh
  docker-compose build
  ```

## Solución de Problemas

- Si tienes problemas con la base de datos, verifica las credenciales en el archivo `.env`.
- Asegúrate de que los puertos necesarios (8000 y 5433) estén disponibles en tu máquina local.

## Contacto

Para cualquier pregunta o problema, por favor abre un issue en el repositorio o contacta directamente.

¡Gracias por utilizar este proyecto!
```
