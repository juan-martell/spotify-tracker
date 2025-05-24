import os, time, spotipy
from songdb import append_to_db, conectar
from spotipy import SpotifyOAuth
from dotenv import load_dotenv

# FUNCIONES PARA SACAR TOKEN DE SPOTIFY
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_auth_for(scope: str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri="http://localhost:8888/callback",
            scope=scope
            ))
    return sp

# FUNCIONES QUE INTERACTUAN CON LA API DE SPOTIFY

def get_playing_track() -> list:
    sp = get_auth_for("user-read-playback-state")
    try:
        resultados = sp.current_playback()
    except Exception as e:
        print(f"[ERROR] Spotify API request failed: {e}")
        return []
    track = []
    if (resultados):
        info = resultados["item"]
        track.append(info["name"])
        track.append(info["artists"][0]["name"])
        track.append(info["album"]["name"])
        track.append(resultados["timestamp"])
        track.append(resultados["is_playing"])
        track.append(resultados["progress_ms"])
    return track


def add_to_database(track: list) -> bool:
    current_time: int = int(time.time() * 1000)
    timestamp: int = track[3]
    is_playing: bool = track[4]
    return is_playing and (current_time - timestamp >= 30000)
    

def is_same_song(current_track: list, last_track: list) -> bool:
    current_name = current_track[0]
    current_progress = current_track[5]
    if last_track == []:
        return False
    last_name = last_track[0]
    last_progress = last_track[5]
    return (current_name == last_name) and (current_progress > last_progress)
    

def player_status(track: list):
    if not track:
        print("No esta sonando nada por ahora")
    elif (track[5]):
        print(f"{track[0]} - {track[1]}")
    else:
        print("Pausa")


def main():
    db: list[list] = []
    old = [] 
    try:
        while (True):
            cur, conn = conectar()
            current = get_playing_track()
            if len(db) > 10:
                db = db[10:]
            if current == []:
                time.sleep(10)
                continue 
            if (is_same_song(current, old) and (old not in db) or not is_same_song(current, old)) and add_to_database(current):
                old = current
                db.append(current)
                append_to_db(current, cur, conn)
                print(f"{current[0]} agregada a la db")
                cur.close()
                conn.close()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Chau")


# VARIABLES GLOBALES
cur, conn = conectar()


# CODIGO LIBRE
main()
