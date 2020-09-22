import threading
import time
import multiprocess
from pydub import AudioSegment
from pydub.playback import play
import argparse


def wait_for_press(key_pressed):
    input()
    key_pressed.append(True)


def countdown(length, remaining_length):
    remaining_length.put(length)
    while length > 0:
        remaining_length.get()
        remaining_length.put(length)
        time_format = '{:02d}:{:02d}'.format(int(length / 60), int(length % 60))
        print(time_format, end='\r')
        length -= 1
        time.sleep(1)


class Timer:
    def __init__(self, args):
        self.num_pomodoros = args.num_pomodoros
        self.pomodoro_length = args.pomodoro_length
        self.normal_break_length = args.normal_break_length
        self.long_break_length = args.long_break_length
        self.remaining_length = args.pomodoro_length

    def convert_time_to_seconds(self):
        self.num_pomodoros = self.num_pomodoros
        self.pomodoro_length = self.pomodoro_length*60
        self.normal_break_length = self.normal_break_length*60
        self.long_break_length = self.long_break_length*60
        self.remaining_length = self.remaining_length*60

    def start_pomodoro_timer(self):
        current_length = multiprocess.Queue()
        pomodoro_process = multiprocess.Process(target=countdown, args=(self.remaining_length, current_length))
        pomodoro_process.daemon = True
        pomodoro_process.start()

        key_pressed = []
        pause_thread = threading.Thread(target=wait_for_press, args=(key_pressed,))
        pause_thread.daemon = True
        pause_thread.start()

        while pomodoro_process.is_alive():
            if key_pressed:
                key_pressed = []
                self.remaining_length = current_length.get()
                pomodoro_process.terminate()
                x = input('Press ENTER to resume the timer\n')

                self.start_pomodoro_timer()

    def start_break_timer(self, length):
        current_length = multiprocess.Queue()
        break_process = multiprocess.Process(target=countdown, args=(length, current_length))
        break_process.start()
        break_process.join()

    def start(self):
        for current_pomodoro_index in range(self.num_pomodoros):
            self.start_pomodoro_timer()

            song = AudioSegment.from_mp3('audio/analog-watch-alarm.mp3')
            play(song[:2900])

            if current_pomodoro_index < 4:
                self.start_break_timer(self.normal_break_length)
            else:
                self.start_break_timer(self.long_break_length)

            self.remaining_length = self.pomodoro_length


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pomodoros', type=str, default=4)
    parser.add_argument('--pomodoro_length', type=str, default=25)
    parser.add_argument('--normal_break_length', type=str, default=5)
    parser.add_argument('--long_break_length', type=str, default=25)
    args = parser.parse_args()

    timer = Timer(args)
    timer.convert_time_to_seconds()
    timer.start()


if __name__ == '__main__':
    main()
