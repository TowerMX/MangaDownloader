# MangaDownloader

Este es un proyecto para descargar mangas de mangadex.org en formato PDF, divididos por capítulos y agrupados por volúmenes.

Los ficheros de configuración involucrados son:
1. config/config.yaml
2. config/credentials.yaml
3. config/mangalist.yaml

## config/config.yaml

La estructura es:

```
login: <true|false>
```

Por ahora, sólo se puede elegir si iniciar sesión o no. Por defecto es false.

## config/credentials.yaml

La estructura es:

```
username: <usuario>
password: <contraseña>
```

Puede dejarse en blanco si no se quiere iniciar sesión.

## config/mangalist.yaml

La estructura es:

```
- name: <nombre_manga_1>
  url: <url_manga_1>
- name: <nombre_manga_2>
  url: <url_manga_2>
- name: <nombre_manga_3>
  url: <url_manga_3>
...
```

Se pueden añadir tantos mangas como se quiera, poniendo un guión (-) al principio de cada manga.
El nombre elegido es el que se usará para crear la carpeta donde se descargará el manga, y la url es el enlace a la primera página del primer capítulo del manga.