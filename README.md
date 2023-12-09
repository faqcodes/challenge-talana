# Talana Kombat JRPG

Talana Kombat es un juego donde 2 personajes se enfrentan hasta la muerte. Cada personaje tiene 2
golpes especiales que se ejecutan con una combinación de movimientos + 1 botón de golpe.

## Intrucciones de uso

### Uso de Docker

pre-requito: tener Docker instalado

La aplicación se encuentra se ha disponibilizada en el siguiente [REPOSITORIO](https://hub.docker.com/repository/docker/faqcodes/talanakombat) en Docker Hub

Para utilizar la aplicación se deben seguir los siguientes pasos:

1. Obtener la imagen desde el repositorio:

```
docker pull faqcodes/talanakombat:latest
```

2. Una vez obtenida la imagen, se debe ejecutar:

```
docker run -it faqcodes/talanakombat:latest
```

3. Una vez ejecutado el contenedor, se ecnuentra listo para ejecutar la aplicación.
Para ejecutar la aplicación se debe utilizar Python como sigue:

```
python kombat.py data/{archivo_json}
```

donde:
- <b>archivo_json</b>: es un archivo json con los movimientos y golpes de los jugadores

Ejemplo de archivo:

**kombat_data_1.json**:
```
{
  "player1": {"movimientos":["D","DSD","S","DSD","SD"], "golpes":["K","P","","K","P"]},
  "player2": {"movimientos":["SA","SA","SA","ASA","SA"], "golpes":["K","","K","P","P"]}
}
```

Ejemplo de ejecución:

```
python kombat.py data/kombat_data_1.json
```

Lo que dará como resultado:

```
TALANA KOMBAT: comienza y Tonyn ataca primero

Tonyn se mueve ágilmente y le pega su Patada
Arnaldor le pega su buen Remuyuken al pobre Tonyn
Tonyn le pega tremendo Taladoken al pobre Arnaldor
Arnaldor hace algunos movimientos exóticos sin ningún daño... (Tonyn se ríe)
Tonyn hace algunos movimientos exóticos sin ningún daño... (Arnaldor se ríe)
Fatality! Arnaldor le pega su buen Remuyuken al pobre Tonyn

Arnaldor gana la pelea y aún le queda(n) 2 de energía
```

Por defecto, dentro del contenedor se encuentran 4 archvios con datos de peleas dentro de la carpeta 'data':

kombat_data_1.json
kombat_data_2.json
kombat_data_3.json
kombat_data_4.json

Si se desea agregar más archivos, se puede ejecutar el contenedor agregando un volumen con los datos. Por ejemplo, en la ruta del equipo local <b>'/Users/felipe.quiroz/challenge-talana/data'</b> se encuentran más archivos de peleas.
Para dejarlos disponibles en el contenedor se debe correr con la siguiente línea de comando:

```
docker run -v /Users/felipe.quiroz/challenge-talana/data:/app/data -it faqcodes/talanakombat:latest
```

Y luego ejecutar normalmente:

```
python kombat.py data/nuevos_datos_de_pelea.json
```
