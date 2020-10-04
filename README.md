# pomodoro
Lightweight and simple pomodoro tracker running entirely inside the shell and written in Python 3

## Pomodoro technique
The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. The technique uses a timer to break down work into intervals, traditionally 25 minutes in length, separated by short breaks. Each interval is known as a pomodoro, from the Italian word for 'tomato', after the tomato-shaped kitchen timer that Cirillo used as a university student.

The technique has been widely popularized by dozens of apps and websites providing timers and instructions. Closely related to concepts such as timeboxing and iterative and incremental development used in software design; the method has been adopted in pair programming contexts.

Source: https://en.wikipedia.org/wiki/Pomodoro_Technique

## Installation
In order to install the pomodoro tracker, firstly clone the repository locally by running

```
git clone git@github.com:RoZvEr/pomodoro.git
```

and then install the required Python dependencies by running

```
pip install -r requirements.txt
```

after changing the directory to ``./pomodoro``

## Usage
In order to start the tracker, run

```
python tracker.py --num_pomodoros <integer>
--pomodoro_length <float> --normal_break_length <float>
--long_break_length <float> --sound_file <string>
```

Here is a list indicating what each of the given parameters is responsible for
* **num_pomodoros** - number, indicating how many pomodoros the user is planning to have 
(a pomodoro is basically a session, during which the user works)
* **pomodoro_length** - duration of the pomodoros, expressed in minutes
* **normal_break_length** - duration of a normal break, which follows each pomodoro, 
expressed in minutes
* **long_break_length** - duration of a long break, which replaces every fourth consecutive
 normal break, expressed in minutes
* **sound_file** - location of a sound file, which gets played for 3 seconds after each pomodoro or break,
in order to notify the user that it has finished (the default sound, ``analog-watch-alarm.mp3`` is located
in the ``audio`` directory)

For example, if you want to start a tracker with 4 pomodoros, each of which lasts for 25 minutes, normal break of
5 minutes, long break of 25 minutes and audio file ``analog-watch-alarm.mp3``, run

```
python tracker.py --num_pomodoros 4
--pomodoro_length 25.0 --normal_break_length 5.0
--long_break_length 25.0 --sound_file audio/analog-watch-alarm.mp3
```

## Used libraries
The main focus of this project is to implement a lightweight and minimalist pomodoro
tracker that runs entirely inside the shell. Therefore, we use only the following
Python 3 libraries

* time
* multiprocess
* pydub
* argparse
