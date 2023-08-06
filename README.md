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
remember_me: <true|false>
temp_path: <ruta_descargas>
save_path: <ruta_mangas>
```

Se puede elegir si iniciar sesión o no, y si se quiere que se recuerde la sesión. Por defecto son false.

También se puede elegir la ruta donde se descargan las imágenes temporalmente y la ruta donde se guardarán los mangas. Si se dejan vacías se usarán las rutas por defecto.

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
  first_chapter: <"first"|capítulo_inicial>
  last_chapter: <"last"|capítulo_final>
- name: <nombre_manga_2>
  url: <url_manga_2>
  first_chapter: <"first"|capítulo_inicial>
  last_chapter: <"last"|capítulo_final>
- name: <nombre_manga_3>
  url: <url_manga_3>
  first_chapter: <"first"|capítulo_inicial>
  last_chapter: <"last"|capítulo_final>
...
```

Se pueden añadir tantos mangas como se quiera, poniendo un guión (-) al principio de cada manga.
El nombre elegido es el que se usará para crear la carpeta donde se descargará el manga, y la url es el enlace a la primera página del primer capítulo del manga.

Para los capítulos inicial y final puede escribirse "first" y "last" respectivamente, o el número del capítulo que se quiera.