import time
import multiprocess
from pydub import AudioSegment
from pydub.playback import play
import argparse


# Main function for a timer counting downwards
def countdown(length, remaining_length, sound_file):
    # Update the remaining length object (it is a multiprocess.Queue, so that it can be accessed by the multiprocess)
    remaining_length.put(length)

    while length > 0:
        # Get the remaining time and print it in the format MM:SS by swapping the previously printed time
        remaining_length.get()
        remaining_length.put(length)
        time_format = '{:02d}:{:02d}'.format(int(length / 60), int(length % 60))
        print(time_format, end='\r')

        length -= 1
        time.sleep(1)

    # When the timer has finished, play a sound for 3 seconds
    song = AudioSegment.from_mp3(sound_file)
    play(song[:3000])

    # Ask the user to press ENTER to start the break
    print('\nPress ENTER to start break')


# Main object - Tracker
class Tracker:
    def __init__(self, args):
        """
        Each tracker has 6 parameters:
        number of pomodoros that the user wants to work during,
        length of those pomodoros,
        length of a normal break, that follows each pomodoro,
        length of a long break, that replaces the normal1 break after 4 consecutive pomodoros,
        remaining length of the current pomodoro,
        and location of a sound file, that gets played after the end of each pomodoro and break
        """

        self.num_pomodoros = args.num_pomodoros
        self.pomodoro_length = args.pomodoro_length
        self.normal_break_length = args.normal_break_length
        self.long_break_length = args.long_break_length
        self.remaining_length = args.pomodoro_length
        self.sound_file = args.sound_file

    def convert_time_to_seconds(self):
        # Convert parameters from minutes to seconds
        self.pomodoro_length = self.pomodoro_length*60
        self.normal_break_length = self.normal_break_length*60
        self.long_break_length = self.long_break_length*60
        self.remaining_length = self.remaining_length*60

    # Function for pomodoro timer
    def start_pomodoro_timer(self):
        # Save the remaining length of the pomodoro inside a queue that can be accessed via the multiprocess
        current_length = multiprocess.Queue()

        # Define a asynchronous multiprocess for the timer
        pomodoro_process = multiprocess.Process(target=countdown, args=(self.remaining_length,
                                                                        current_length,
                                                                        self.sound_file))
        pomodoro_process.daemon = True
        pomodoro_process.start()

        while pomodoro_process.is_alive():
            # While the timer is running in the background, listen to user input
            input('Press ENTER to pause\n')

            # If the user has pressed ENTER, get the remaining length and kill the current timer process
            self.remaining_length = current_length.get()
            pomodoro_process.terminate()

            # Check if the timer has finished (reached 0 seconds)
            if self.remaining_length < 1:
                break

            # Monitor for how long the user has paused the timer
            pause_start_time = time.time()

            # Wait for the user input
            input('Press ENTER to resume\n')

            # Print for how long the timer was paused
            pause_end_time = time.time() - pause_start_time
            pause_time_format = '{:02d}:{:02d}'.format(int(pause_end_time / 60), int(pause_end_time % 60))
            print('Total pause time: ' + pause_time_format + '\n')

            """
            Start the pomodoro timer again, but counting down from 
            the remaining time we got before killing the multiprocess
            """
            self.start_pomodoro_timer()

    def start_break_timer(self, length):
        # Basically the same implementation as the timer for the pomodoro, but this one cannot be paused
        print('\nBreak started\n')
        current_length = multiprocess.Queue()
        break_process = multiprocess.Process(target=countdown, args=(length,
                                                                     current_length,
                                                                     self.sound_file))
        break_process.start()
        break_process.join()
        break_process.terminate()
        input('Press ENTER to start another pomodoro\r')

    # Main function for starting the tracker
    def start(self):
        # Run it for a given by the user number of pomodoros
        for current_pomodoro_index in range(self.num_pomodoros):
            # Start the pomodoro timer
            self.start_pomodoro_timer()

            # After every consecutive 4 pomodoros, instead of a regular break, take a longer break
            if current_pomodoro_index < 4:
                self.start_break_timer(self.normal_break_length)
            else:
                self.start_break_timer(self.long_break_length)

            # Refresh the remaining length parameter, so that the next pomodoro timer does not start from 0
            self.remaining_length = self.pomodoro_length


def main():
    # Parse Tracker arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pomodoros', type=int, default=4)
    parser.add_argument('--pomodoro_length', type=float, default=25.0)
    parser.add_argument('--normal_break_length', type=float, default=5.0)
    parser.add_argument('--long_break_length', type=float, default=25.0)
    parser.add_argument('--sound_file', type=str, default='audio/analog-watch-alarm.mp3')
    args = parser.parse_args()

    # Initialize the tracker, convert the time to seconds and start it
    tracker = Tracker(args)
    tracker.convert_time_to_seconds()
    tracker.start()


if __name__ == '__main__':
    main()
