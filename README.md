########################################################################################################################
### Cómo ejecutar la API localmente. #####

1. Descomprimir la carpeta POKEAPI
2. Ingresar al carpeta descomprimida: clic izquierdo si es que estamos en windows, abrir un powershell o un CMD y colocar el sigueinte comando
>>> code .
Esto nos abrirá el editor
3. Estando alli podremos observar la carpeta con todo los archivos incluido el requirements.txt, desde la consola CMD o desde la terminal del Visual COde ejecutar el siguiente comando:
>>> python -m pip install -r requirements.txt
lo que hara esto es traer toda las dependencias y paquetes que necesita el proyecto APi para que esta funcione. validar que todo los paquetes se hayn instalado correctamente.
4. En esta misma ruta ejecutar la siguiente linea de comando
>>>  uvicorn main:app --reload
5. En el CMD o la consola noes muestra esta informacion

PS C:\Users\DELL\Desktop\POKEAPI> uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['C:\\Users\\DELL\\Desktop\\POKEAPI']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [23088] using StatReload
INFO:     Started server process [20604]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

usamremos la direccion mostrada :  http://127.0.0.1:8000 pero le agregamos la ruta docs es decir:
http://127.0.0.1:8000/docs y esto es lo que copiaremos y colocaremos en la barra de direcciones de un browser , sea internet explorer, Google Chrome entre otro. Esto nos llevar a la interfaz de Swagger desde el navegador.

6. Estando alli podemos observa la interfaz API, podemos observar que las APis estan impentadas, usando el metodo POST

POST
/login
Login


POST
/pokemon
Get Pokemons

### Cómo probar los endpoints. ####

1. Despues de haber ejecutado la API localmente prcederemos hacer la prueba de forma ordenado, para la autenticacion:

En POST /login login deslogamos la flecha derecha y observaremos que hay una opcion llamada Try out, que es donde haremos clic y nos aparecera un sectro donde colocaremos el REQUEST BODY, alli colocaremos este Request:
 {
  "username": "usuario1",
  "password": "password1"
}

y en la parte inferior hay una opcion llamada Execute (ejecutar) y le haremos clic.

2. Luego de ejecutar , observaremos que se mostrar un sector llamado Response body donde tiene un CODE 200 que quiere decir que el Api respondio correctamente y alli veremos la respuesta que es el user y el token pero considerar que el tiempo de valor del token es de 5 min por lo que se recomienda que se coloque en un bloc de nota, la respuesta tiene esta forma:

{
  "access_token": "eyJhbGciOiJI.......",
  "token_type": "bearer"
}

de este sector solo nos interesara el Token.

3. En la parte superior hay una opcion que dice Authorize acompañada de un candado como ícono. haremos clic y se mostrará una ventana que tiene como titulo 
Available authorizations:

en la seccion  Value: colocaremos el token obtenido en el Paso 2.

*con esto ya estamos autenticado, cerramos la ventana Available authorizations:

4. Nos iremos  la seccion  POST
/pokemon
Get Pokemons

Desplegando este sector haremos clic en la opcion Try Out de Get Pokemon y pegaremos este Json debajo de Request Body

{
  "pokemons": ["pikachu", "bulbasaur", "xyz"]
}

Luego le daremos Execute (ejecutar).

5. Finalmente obtendremos la siguiente informacion en la sección

	
Response body

[
  {
    "nombre": "pikachu",
    "altura": 4,
    "peso": 60,
    "tipo": [
      "electric"
    ],
    "cadena evolutiva": [
      "pichu",
      "pikachu",
      "raichu"
    ]
  },
  {
    "nombre": "bulbasaur",
    "altura": 7,
    "peso": 69,
    "tipo": [
      "grass",
      "poison"
    ],
    "cadena evolutiva": [
      "bulbasaur",
      "ivysaur",
      "venusaur"
    ]
  },
  {
    "name": "xyz",
    "error": "Pokémon no encontrado"
  }
]

si observamos al agregar un valor que no existe, nos traera que este pokemon no se encuentra.

############################################################################################################################################

### Docker ###

1. Creamos el archivo Dockerfile, que para este caso ya lo tenemos listo y contiene esta informacion

# Imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia solo requirements.txt primero (mejor para caché)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente al contenedor
COPY . .

# Expone el puerto 8000 para acceder desde el navegador
EXPOSE 8000

# Comando para iniciar FastAPI con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

2. Validemos que tengamos instalado Docker y que sus servicios esten correctamentes iniciados, asi como el servicio de virtualizacion, que va a requerir que entremos a la bios para validar que esta opcion esta instalado.

3. Seguidamente haremos construir la imagen:

>>> docker build -t pokeapi .

4. Ejecutaremos el contenedor:
 >>>docker run -d -p 8000:8000 pokeapi 
o podemos ejecutar
 >>>docker run -d -p 8000:8000 --name pokeapi_container pokeapi

 esto nos dara la ruta de accesso, cabe recalcar que nos dara esta ruta  http://127.0.0.1:8000, el cual tendremos que agregarlo el /docs y con ello accederemos al API

 **Desde la aplicacion Docker.Desktop tambien podemos ver nuestros contenerdores creados por comando, abrimos Docker Desktop, registrado con nuestra cuenta, e inicilizando los servicio, demorara un poco, pero al final observaremos en la seccion conteiners, alli podemos entrar en nuestro desde columna  PORTS pero debemos agregar /docs porque de alli probaremos de la misma manera como lo ejecutamos ejecutando el servicio de FASTAPI.

 ##################################################################################################################################

 ### Pruebas con POSTMAN ####

  Desde Postman se puede importar el archivo pokeapi_postman_collection.json que contiene la coleccion para poder autenticarse y para poder buscar un pokemon.

1. Hacer clic en Import que se ubica en la parte izquierda y arrastrar el archivo.
2. Para las pruebas nos dirigiremos a Login ejecutaremos y obtendremos el token.
3. Con el token nos dirigimos a Get Pokemon with token y nos dirigiremos a Authorization y lo que acompaña a Bearer  es e token, este ultimo lo reemplazamos por el token generado y como resultado veremos los que se solicita, los datos del pokemon asi como su cadena evolutiva.

############################################################

### tests con pytest o unittest ###
1. Nos ubicamos en la ruta donde esta descomprimido el proyecto , por ejemplo:  C:\Users\DELL\Desktop\POKEAPI>
2. Ejecutamos el siguiente comando:
>>>pytest test_main.py


 