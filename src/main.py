from serial.tools.list_ports import comports
from time import perf_counter, sleep
import serial
import pandas as pd
import json
import threading

from pydub import AudioSegment
from pydub.playback import play

def play_sound(pathname: str) -> None:
    audio = AudioSegment.from_mp3(pathname)
    play(audio)


def init(rule=True):
    play_sound("src/assets/init.mp3")
    if rule:
        play_sound("src/assets/intro.mp3")
    sleep(0.3)

def train(filename: str):
    points = dict()
    t0 = perf_counter()
    play_sound("src/assets/relax.mp3")
    sleep(1.52)
    play_sound("src/assets/321.mp3")
    sleep(0.1)
    points["baseline"] = perf_counter() - t0

    for _ in range(3):
        points[f"close_{_}"] = perf_counter() - t0
        play_sound("src/assets/close.mp3")
        sleep(2)    
        points[f"open_{_}"] = perf_counter() - t0
        play_sound("src/assets/open.mp3")
        sleep(2)

    play_sound("src/assets/recording_complite.mp3")

    with open(f"{filename}_points.json", "w") as f:
        json.dump(points, f)

def reader(name: str):
    print("Start Recording")
    PORT = comports()[0][0]
    BAUDRATE = 115200
    data = []
    filename = f"{name}.csv"

    with serial.Serial(PORT, BAUDRATE) as board:
        t0 = perf_counter()
        try:
            while board.isOpen():
                if board.inWaiting():
                    pack = board.readline().decode("utf-8").strip().replace("\n", "")
                    try:
                        sensor = json.loads(pack)
                        data.append([perf_counter() - t0, int(sensor["emg1"]), int(sensor["emg2"]), int(sensor["emg3"])])
                    except ValueError:
                        pass
                if perf_counter() - t0 >= 24:
                    raise KeyboardInterrupt()
        except KeyboardInterrupt:
            df = pd.DataFrame(data, columns=["time", "emg1", "emg2", "emg3"])
            df.to_csv(filename, index=False)


if __name__ == "__main__":
    init(False)
    filename = "data/sitting/exp_10"

    processes = [
        threading.Thread(target=train, args=(filename,)),
        threading.Thread(target=reader, args=(filename,))
    ]

    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
