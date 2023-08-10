# MangaDownloader

Este es un proyecto para descargar mangas de mangadex.org en formato PDF.

Los ficheros de configuración involucrados son:
1. config/config.yaml
2. config/credentials.yaml
3. config/mangalist.yaml

Sólo es necesario rellenar el tercero con los mangas que queramos descargar y ejecutar el archivo main.py a mano o desde el archivo run.bat (sólo Windows). Más abajo se explica cómo deben rellenarse.

## config/config.yaml

La estructura es:

```
language: <idioma>
login: <true|false>
delete_images: <true|false>
temp_path: <ruta_descargas>
save_path: <ruta_mangas>
```

Puede elegirse el idioma para los archivos de entre los siguientes:
- Español: "es"
- Portugués: "pt"
- Inglés: "en"
- Alemán: "de"
- Italiano: "it"
- Francés: "fr"

Por defecto está en español.

Se puede elegir si iniciar sesión o no, por defecto es false.

Después de la ejecución, las imágenes temporales pueden borrarse. Por defecto es true.

También se puede elegir la ruta donde se descargan las imágenes temporalmente y la ruta donde se guardarán los mangas. Si se dejan vacías se usarán las rutas por defecto, que son las carpetas temp y mangas en el directorio raíz del programa.

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
El nombre elegido es el que se usará para crear la carpeta donde se descargará el manga, y la url es el enlace a la lectura de una página del manga (no al manga en sí).

Para los capítulos inicial y final puede escribirse "first" y "last" respectivamente, o el número del capítulo que se quiera.
