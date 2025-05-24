import mariadb, time, dotenv, os

dotenv.load_dotenv()
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWD = os.getenv("MYSQL_PASSWD")
# INTERACCION CON LA BASE DE DATOS 

# Logica de conexion a la base de datos
def conectar():
    while True: # se puede cambiar x un for mas finito
        try:
            conn = mariadb.connect(
                user=MYSQL_USER,
                password=MYSQL_PASSWD,
                host="localhost",
                port=3306,
                database="spotify_db"
            )
            cur = conn.cursor()
            return cur, conn
        except mariadb.Error as e:
            print(f"Error conectandose a mariadb: {e}")
            time.sleep(3)
    
# Agrego la cancion a la base de datos (si ya esta llamo a update_song())
def append_to_db(track: list, cur, conn):
    if song_in_db(track, cur):
       update_song(track, cur, conn) 
    else:
        db_execute( 
                "INSERT INTO songs (name, artist, album, listens) VALUES (?, ?, ?, ?)",
                (track[0], track[1], track[2], 1), cur
        )
        conn.commit()

# Si la cancion esta en la db, sumo 1 a columna listens
def update_song(track: list, cur, conn):
    db_execute(
        "SELECT listens FROM songs WHERE name = ? AND artist = ?",
        (track[0], track[1]), cur
    )
    listens = cur.fetchone()
    if not listens:
        new_listens = 0
    else:
        new_listens = int(listens[0]) + 1
    db_execute("UPDATE songs SET listens = ? WHERE name = ? AND artist = ?",
                (new_listens, track[0], track[1]), cur
                )
    conn.commit()

# devuelve True si la cancion esta en la db
def song_in_db(track: list, cur) -> bool:
    db_execute("SELECT * FROM songs WHERE name = ? AND artist = ?",
               (track[0], track[1]), cur
               )
    fetch = cur.fetchone() 
    return fetch != None

# es el comando execute de mariadb pero con fallback x si hay error
def db_execute(command: str, var: tuple, cur):
    try:
        cur.execute(
            command, var 
        )
    except mariadb.Error as e:
        print(e)

# FUNCIONES QUE MUESTRAN INFO DE LA BASE DE DATOS 

def get_last_song(cur):
    db_execute("SELECT name, artist, album FROM songs ORDER BY id DESC LIMIT 1", (), cur )
    fetch = cur.fetchone()
    return fetch

def get_most_listens(cur, cant: int) -> list[tuple]:
    db_execute("SELECT name, artist, album, listens FROM songs ORDER BY  listens DESC", (), cur)
    most_listens: list[tuple] = cur.fetchall() 
    return most_listens[:cant]

def get_most_listened_artist(cur, cant: int) -> list[tuple]:
    db_execute("SELECT artist, count(*) AS canciones, sum(listens) AS total_listens FROM songs GROUP BY artist ORDER BY total_listens DESC;", (), cur)
    most_listened_artist: list[tuple] = cur.fetchall()
    return most_listened_artist[:cant]

cur, conn = conectar()

