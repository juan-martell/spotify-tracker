# 2025-05-23
# SPOTIFY-TRACKER
Escribi este script motivado por mi odio y desconfianza hacia spotify y como manejan los datos del usuario.
La idea es tener un demonio que guarde todas las canciones que escuchas en una base de datos y asi tener informacion
exacta de tus artistas, canciones y generos mas escuchados.

# INSTALACION
Para que el script funcione es necesario 
    - tener una base de datos llamada spotify_db en mysql
    - poner tu spotify client id y client secret en un archivo dotenv en la carpeta del script
    - los modulos dotenv, spotipy, python3-dev instalados con pip
el script se puede correr dentro de una terminal pero es preferible correrlo como servicio en systemctl

# TO DO LIST
- algun instalador para crear la base de datos y el usuario de mysql y que instale los modulos si no los tenes
- una opcion en ese script que si sos sudo te cree el archivo /etc/systemd/spotify-tracker.service 
- una columna de genero en la db (esto requiere hacer otra request al sv de spotify pq solo me da el genero si pregunto x artista)


