```markdown
# Proyecto Final de API con Python - Ecommerce

Este repositorio contiene el proyecto final para la asignatura de APIs con Python. Se trata de una aplicación de Ecommerce que permite gestionar productos, usuarios y pedidos de manera eficiente.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente:

- [Docker](https://www.docker.com/)
- Python 3.10
- Virtualenv (si deseas usar un entorno virtual)

## Configuración del Entorno

1. Clona el repositorio:

   ```bash
   git clone https://github.com/JACKATANA/proyectoAPIsFinal.git
   cd proyectoAPIsFinal/venv
   ```

2. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux y macOS
   venv\Scripts\activate  # Para Windows
   ```

3. Asegúrate de tener una base de datos llamada `ecommerce` creada en tu sistema.

## Construcción y Ejecución

Para construir y ejecutar el proyecto, utiliza los siguientes comandos:

1. Construir la imagen Docker:

   ```bash
   docker build -t proyectoAPI .
   ```

2. Ejecutar el contenedor Docker:

   ```bash
   docker run -p 8000:8000 proyectoAPI
   ```

## Acceso a la Aplicación

Una vez que el contenedor esté en funcionamiento, podrás acceder a la aplicación en tu navegador en la siguiente dirección:

```
http://localhost:8000
```

