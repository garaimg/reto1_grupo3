# Reto1 Grupo3 - Desarrollo de aplicaciones IoT

# Proyecto: Captación de Datos mediante MAGE

Este proyecto implementa una solución ETL (Extract, Transform, Load) utilizando Mage AI y PostgreSQL, orquestados
mediante Docker Compose. Se extraen datos de una tabla de origen, se transforman mediante un script en Python y se
cargan en una tabla de destino. Además, se ha configurado un trigger para ejecutar el pipeline de forma automática cada
minuto.

---

## Miembros del Equipo

- **Miembro 1:** Markel Aguirre
- **Miembro 2:** Garai Martínez de Santos
- **Miembro 3:** Pablo Ruiz de Azúa

---

## Explicación de los Pasos Seguidos

1. **Configuración de Contenedores con Docker Compose:**
    - **Mage AI:** Contenedor que ejecuta la plataforma Mage y sus pipelines.
    - **PostgreSQL:** Contenedor que actúa como base de datos para almacenar las tablas y sus datos.
    - **pgAdmin:** Contenedor opcional que facilita la administración y visualización de las tablas en la base de datos.

   El archivo `docker-compose.yml` define estos servicios y utiliza un archivo `.env` para gestionar las variables de
   entorno de postgres y pgAdmin (nombre de base de datos, usuario, contraseña, host, puerto, email de pgAdmin,
   contraseña de pgAdmin, etc.).

2. **Definición de la Infraestructura en la Base de Datos:**
    - **Tabla `ventas`:** Tabla de origen donde se insertan los datos de ventas.
    - **Tabla `detalle_ventas`:** Tabla destino donde se guardan los datos transformados.

   La creación de estas tablas se realiza mediante la primera etapa del pipeline en Mage.

3. **Inserción de Datos:**
    - Se ejecuta una segunda etapa de la pipeline que inserta datos aleatorios en la tabla `ventas`. Con cada ejecución
      se añaden nuevos registros, simulando un flujo continuo de datos.

4. **Lectura y Transformación de Datos:**

- Se ha desarrollado una etapa de la pipeline en Mage, donde se realizan las siguientes transformaciones mediante el uso
  de dataframes de Pandas:

- **Lectura:**  
  Se extraen los datos de la tabla `ventas` utilizando una consulta SQL que selecciona únicamente los registros
  nuevos.

- **Procesamiento Incremental:** Se filtra la extracción para que solo se procesen los registros cuyo `id` sea mayor que
  el último `id` procesado (consultando el valor máximo de `id` en `detalle_ventas`), evitando duplicar registros ya
  transformados.

- **Conversión de Tipos:**  
  Se aseguran los tipos de datos correctos para cada columna (por ejemplo, convertir a `int` o `float` según
  corresponda).

- **Cálculo del Total de Venta:**  
  Se multiplica la `cantidad` por el `precio_unitario` para obtener el campo `total_venta`.

- **Clasificación de la Venta:**  
  Se asigna una categoría (`Alta`, `Media` o `Baja`) en función del valor de `total_venta`.

- **Extracción del Mes:**  
  Se convierte la fecha de venta a formato `datetime` y se extrae el mes correspondiente, creando así una nueva columna
  con el mes de venta.

- **Validación:**
  Se implementan pruebas para garantizar que los datos transformados sean correctos, que las columnas generadas existan
  y que los id sean únicos.

5. **Escritura de Datos Transformados:**
    - Los datos resultantes se exportan a la tabla `detalle_ventas` en PostgreSQL, completando el proceso ETL.

6. **Automatización de la Pipeline:**
    - Se ha configurado un trigger en el archivo `triggers.yaml` para que la pipeline se ejecute automáticamente cada
      minuto, permitiendo la captación y transformación continua de los datos.

7. **Configuración de Conexión a la Base de Datos:**
    - El archivo `io_config.yml` se ha configurado para conectar Mage AI con PostgreSQL utilizando las variables de
      entorno definidas en el archivo `.env`.
    - Se ha definido un perfil de configuración llamado dev, que es el específico para este proyecto. Este perfil
      permite gestionar la conexión a la base de datos dentro de Mage AI.
    - En caso de necesitar otros entornos, como producción (prod) o pruebas (test), se podrían añadir más perfiles en
      io_config.yml.

---

## Instrucciones de Uso

1. **Requisitos Previos:**
    - Tener instalado [Docker](https://www.docker.com/get-started)
      y [Docker Compose](https://docs.docker.com/compose/install/).
    - Clonar el repositorio del proyecto.

2. **Configuración del Entorno:**
    - Revisar y, de ser necesario, modificar las variables en el archivo `.env` para adecuarlas a la configuración de tu
      entorno.

3. **Levantar los Contenedores:**
    - Ejecutar el siguiente comando en la terminal:
      ```bash
      docker-compose up -d
      ```
    - Esto iniciará los contenedores de Mage AI, PostgreSQL y pgAdmin.

4. **Acceso a las Herramientas:**
    - **Mage AI:** [http://localhost:6789](http://localhost:6789)
    - **pgAdmin:** [http://localhost:5050](http://localhost:5050)  
      Con pgAdmin podrás visualizar y gestionar las tablas `ventas` y `detalle_ventas`.

5. **Ejecución de Pipelines:**
    - Por último, se ejecutarán todas las etapas de la pipeline cada minuto de manera continua, gracias al trigger
      configurado.

---

## Posibles Vías de Mejora

- **Gestión de Errores:**
    - Mejorar la captura y notificación de errores durante la ejecución de los pipelines para facilitar la depuración.

- **Monitorización y Logging:**
    - Integrar herramientas de monitorización para obtener alertas y logs detallados sobre el procesamiento de datos.

- **Escalabilidad:**
    - Explorar el uso de procesamiento distribuido o caché para mejorar la eficiencia y capacidad de manejo de grandes
      volúmenes de datos a medida que el proyecto crece, reduciendo tiempos de ejecución y aumentando la capacidad de
      respuesta del sistema.

- **Documentación Ampliada:**
    - Documentar más el proyecto para facilitar el mantenimiento y la comprensión del sistema.

---

## Problemas / Retos Encontrados

- **Sincronización entre Servicios:**
    - Asegurar que PostgreSQL esté completamente iniciado antes de que Mage AI intente conectarse, lo que se solucionó
      utilizando `depends_on` en Docker Compose.

- **Manejo de la Incrementalidad:**
    - Implementar un mecanismo para procesar solo los registros nuevos (filtrando por el último `id` procesado) y evitar
      duplicaciones.

- **Configuración de Variables de Entorno:**
    - Mantener la coherencia entre el archivo `.env`, `io_config.yml` y la configuración de Docker Compose.

---

## Alternativas Posibles

- **Uso de Otras Herramientas ETL:**
    - Evaluar el uso de Apache Airflow u otras plataformas ETL que permitan una orquestación más compleja.

- **Almacenamiento en Data Lakes:**
    - Considerar el uso de soluciones de almacenamiento escalables (como un Data Lake) para manejar volúmenes muy
      grandes de datos.

- **Control y Seguimiento de Transformaciones:**
    - Establecer un proceso para documentar y rastrear las transformaciones de datos, asegurando que cualquier cambio se
      realice de manera organizada y pueda ser fácilmente revisado y revertido si es necesario.

---
