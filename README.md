# MangaDownloader
### Ver. 1.0.0

Este es un proyecto para descargar mangas de mangadex.org en formato PDF.

Los ficheros de configuración involucrados son:
1. config/config.yaml
2. config/credentials.yaml
3. config/mangalist.yaml

Sólo es necesario rellenar el tercero con los mangas que queramos descargar y ejecutar el archivo main.py a mano o desde el archivo run.bat o run-linux.sh, según el sistema operativo que se use. Más abajo se explica cómo deben rellenarse.

## config/config.yaml

```
language: <idioma>
login: <yes|no>
delete_images: <yes|no>
show_volumes: <yes|no>
separate_chapters: <yes|no>
volume_folders: <yes|no>
temp_path: <ruta_descargas>
save_path: <ruta_mangas>
```

**language**: Por defecto está en español.
Puede elegirse el idioma para los archivos de entre los siguientes:
- Español: es
- Portugués: pt
- Inglés: en
- Alemán: de
- Italiano: it
- Francés: fr

**login**: Se puede elegir si iniciar sesión o no. Por defecto es *no*.

**delete_images**: Después de la ejecución, las imágenes temporales pueden borrarse. Por defecto es *yes*.

**show_volumes**: Si se quiere que el nombre de los archivos PDF incluya el número del volumen. Por defecto es *yes*. Si se elige *no*, las dos opciones siguientes no tendrán efecto, ya que si no se quiere mostrar el volumen los capítulos no se agruparán en ningún volúmen ni se generarán carpetas para cada volumen.

**separate_chapters**: Si se activa, cada capítulo generará un archivo PDF independiente. Por defecto es *yes*.

**volume_folders**: Con esta opción se puede elegir si se quiere que los archivos PDF se guarden en carpetas separadas por volumen. Por defecto es *no*.

**temp_path**: Ruta donde se descargan las imágenes temporalmente. Si se deja vacía se usará la ruta por defecto, que es la carpeta temp en el directorio raíz del programa.

**save_path**: Ruta donde se guardarán los mangas. Si se deja vacía se usará la ruta por defecto, que es la carpeta mangas en el directorio raíz del programa.

## config/credentials.yaml

```
username: <usuario>
password: <contraseña>
```

Usuario y contraseña, respectivamente, de la web. Pueden dejarse en blanco si no se quiere iniciar sesión.

## config/mangalist.yaml

La estructura es:

```
- name: <nombre_manga_1>
  url: <url_manga_1>
  first_chapter: <first|número_capítulo_inicial>
  last_chapter: <last|número_capítulo_final>
  trim_first_pages: <páginas_iniciales_a_eliminar>
  trim_last_pages: <páginas_finales_a_eliminar>
- name: <nombre_manga_2>
  url: <url_manga_2>
  first_chapter: <first|número_capítulo_inicial>
  last_chapter: <last|número_capítulo_final>
  trim_first_pages: <páginas_iniciales_a_eliminar>
  trim_last_pages: <páginas_finales_a_eliminar>
- name: <nombre_manga_3>
  url: <url_manga_3>
  first_chapter: <first|número_capítulo_inicial>
  last_chapter: <last|número_capítulo_final>
  trim_first_pages: <páginas_iniciales_a_eliminar>
  trim_last_pages: <páginas_finales_a_eliminar>
...
```

Se pueden añadir tantos mangas como se quiera, poniendo un guión (-) al principio de cada manga.

**name**: Es el nombre que se usará para la carpeta del manga. Los caracteres no permitidos en Windows para nombres de carpetas serán sustituidos por otros válidos.

**url**: Una vez en la página del manga, se debe entrar en la lectura de un capítulo y copiar la url de la página. Esto se hace para elegir un idioma antes de comenzar a descargar, en la versión 1.0.1 se añadirá la opción de elegirlo sobre la marcha.

**first_chapter**: Para comenzar a descargar desde el principio se debe escribir *first*, si se quiere empezar desde un capítulo concreto se debe escribir el número del capítulo.

**last_chapter**: Para descargar hasta el último capítulo se debe escribir *last*, si se quiere descargar hasta un capítulo concreto se debe escribir el número del capítulo.

**trim_first_pages**: Si se desea eliminar páginas del principio de cada capítulo, por ejemplo, porque incluya publicidad, se puede indicar el número de páginas a eliminar. Si no se quiere eliminar ninguna página se puede introducir 0. Hay que tener en cuenta que si en algún capítulo no se incluye la publicidad, se estarían borrando páginas de forma indeseada.

**trim_last_pages**: De la misma forma que el anterior, si se quiere eliminar páginas del final de cada capítulo, se puede indicar el número o escribir 0 si no se quiere borrar ninguna.
