from time import sleep, perf_counter

from pydub import AudioSegment
from pydub.playback import play
import httpx
import json

def play_sound(pathname: str) -> None:
    audio = AudioSegment.from_mp3(pathname)
    play(audio)


def init(rule=True):
    play_sound("src/assets/init.mp3")
    if rule:
        play_sound("src/assets/intro.mp3")
    sleep(0.3)


def main(folder: str, filename: str) -> None:
    # request to start recording
    response = httpx.post("http://192.168.50.171:8000/session/start", json={"filename": filename})
    if response.status_code != 200:
        return
    task_id: str = response.json()
    time_points = []
    t0 = perf_counter()

    play_sound("src/assets/relax.mp3")
    sleep(1.52)
    play_sound("src/assets/321.mp3")
    sleep(0.1)
    time_points.append(perf_counter() - t0)

    for _ in range(3):
        time_points.append(perf_counter() - t0)
        play_sound("src/assets/close.mp3")
        sleep(3)

        time_points.append(perf_counter() - t0)
        play_sound("src/assets/open.mp3")
        sleep(3)
    time_points.append(perf_counter() - t0)

    play_sound("src/assets/recording_complite.mp3")
    # request to finish recording
    response = httpx.delete(f"http://192.168.50.171:8000/session/{task_id}")
    if response.status_code != 200:
        return

    response = httpx.get(f"http://192.168.50.171:8000/static/{filename}")
    while response.status_code != 200:
        sleep(1)
        response = httpx.get(f"http://192.168.50.171:8000/static/{filename}")

    with open(f"data/orangepi/{folder}/{filename}", "wb") as f:
        f.write(response.read())

    with open(f"data/orangepi/{folder}/{filename.split('.')[0]}.json", "w") as f:
        json.dump(time_points, f)

    sleep(2)
    # response = httpx.delete(f"http://192.168.50.171:8000/file/{filename}")
    # if response.status_code != 200:
    #     return


def ecg_recording(folder: str, filename: str, period: int = 10) -> None:
    # request to start recording
    response = httpx.post("http://192.168.50.171:8000/session/start", json={"filename": filename})
    if response.status_code != 200:
        return
    task_id: str = response.json()

    sleep(period)
    # request to finish recording
    response = httpx.delete(f"http://192.168.50.171:8000/session/{task_id}")
    if response.status_code != 200:
        return

    sleep(2)
    response = httpx.get(f"http://192.168.50.171:8000/static/{filename}")
    if response.status_code != 200:
        return

    with open(f"data/orangepi/{folder}/{filename}", "wb") as f:
        f.write(response.read())

    # response = httpx.delete(f"http://192.168.50.171:8000/file/{filename}")
    # if response.status_code != 200:
    #     return


if __name__ == "__main__":
    main(
        "exo_on",
        "record_4.csv"
    )
