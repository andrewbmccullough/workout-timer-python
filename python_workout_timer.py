import tkinter as tk
import csv
import sys
import time
import pyttsx3
import keyboard

# Functions -------------------------------------------------------------------

def display_exercise_examples(event):
    index = listbox_exercises.curselection()[0]
    key = listbox_exercises.get(index)
    examples = str(dict_exercises[key])
    examples = examples.replace("[","").replace("]","").replace("'","")
    label_exercise_examples.config(text = examples)

def verify_times():
    times_valid = False
    if (entry_number_of_sets.get() != '') and (entry_exercise_duration.get() != '') and (entry_rest_between_exercises.get() != '') and (entry_rest_between_sets.get() != ''):
        times_valid = True

    return times_valid

def calculate_time():
    global num_sets
    global exercise_duration
    global exercise_duration_half
    global rest_between_exercises
    global rest_between_sets
    
    times_valid = False

    workout_duration = 0
    if (verify_times() == True):
        num_sets = int(entry_number_of_sets.get())
        exercise_duration = int(entry_exercise_duration.get())
        exercise_duration_half = round(exercise_duration / 2)
        rest_between_exercises = int(entry_rest_between_exercises.get())
        rest_between_sets = int(entry_rest_between_sets.get())

        workout_duration = ((num_sets * exercise_duration * len(dict_exercises)) + (num_sets * rest_between_exercises * (len(dict_exercises) - 1)) + ((num_sets - 1) * rest_between_sets)) / 60

        times_valid = True

    label_calculate_time.config(text = (round(workout_duration, 2), "mins"))

    return times_valid

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def check_pause():
    pause = 0
    if keyboard.is_pressed('E'):
        sys.exit()
    if keyboard.is_pressed('P'):
        pause = 1
        label_status.config(text = "PAUSED", fg = 'red')
        gui.update()
    while pause == 1:
        if keyboard.is_pressed('C'):
            pause = 0 
            label_status.config(text = "RUNNING", fg = 'green')
            gui.update()
        if keyboard.is_pressed('E'):
            sys.exit()

def timer(t):
    for _ in range(t):
        check_pause()
        time.sleep(1)
        gui.update()
def countdown(t):
    for i in range(t, 0, -1):
        check_pause()
        speak(str(i))
        gui.update()

def start_workout():
    global workout
    global num_sets
    global exercise_duration
    global exercise_duration_half
    global rest_between_exercises
    global rest_between_sets

    if (calculate_time() == False):
        return None

    label_status.config(text = "RUNNING", fg = 'green')
    gui.update()

    for set in range(num_sets):
        # Say first exercise of set
        speak(workout[0] + " starting in 5 seconds.")
        countdown(5)

        # Loop of exercises
        for exercise in range(len(workout)):
            # Say exercise, countdown to half and say halfway, then countdown to the last 3 seconds and say those
            speak(workout[exercise])
            timer(exercise_duration_half)
            speak("Halfway!")
            timer(exercise_duration_half - 3)
            countdown(3)
            
            # Check if it's the last exercise in the set
            if exercise == (len(workout) - 1):
                # Check if it's the last set
                if set == (num_sets - 1):
                    speak("Done with the workout!")
                # Say the starting exercise of the next set and resting time
                else:
                    speak("Done with the set! Next up" + workout[0] + ". Rest" + str(rest_between_sets) + "seconds.")
                    timer(rest_between_sets - 5)
            # Say the next exercise and resting time
            else:
                speak("Done! Next up" + workout[exercise + 1] + ". Rest" + str(rest_between_exercises) + "seconds.")
                timer(rest_between_exercises - 3)
                countdown(3)

# -----------------------------------------------------------------------------

# Set up text to speech
tts_engine = pyttsx3.init()

# Create GUI and window
gui = tk.Tk()
gui.title("Calisthenics Workout")
gui.geometry('500x500')
gui.grid_columnconfigure(0, minsize = 200)

# Create Exercises Dictionary and Workout from CSV
workout = []
csv_exercises = csv.reader(open('exercises.csv'))
dict_exercises = {}
next(csv_exercises)
i = 0
for row in csv_exercises:
    key = row[0]
    workout.append(key)
    dict_exercises[key] = row[1:]
    i += 1          

# Create and fill Listbox with Exercises from Keys
listbox_exercises = tk.Listbox(gui)
for key in dict_exercises:
    listbox_exercises.insert('end', key)
label_exercises_title = tk.Label(gui, text = "Exercises", font = 'bold')
label_exercises_title.grid(row = 0, column = 0, sticky = 'w')
listbox_exercises.grid(row = 1, column = 0, sticky = 'w')

# Create Exercise Examples label and Listbox Select event
label_exercise_examples_title = tk.Label(gui, text = "Exercise Example(s):", font = 'bold')
label_exercise_examples_title.grid(row = 2, column = 0, sticky = 'w')
label_exercise_examples = tk.Label(gui)
label_exercise_examples.grid(row = 3, column = 0, sticky = 'w')
listbox_exercises.bind('<<ListboxSelect>>', display_exercise_examples)

# Settings entry boxes
label_settings_title = tk.Label(gui, text = "Settings:", font = 'bold')
label_settings_title.grid(row = 4, column = 0, sticky = 'w')

num_sets = 0
label_number_of_sets = tk.Label(gui, text = "Number of Sets:")
label_number_of_sets.grid(row = 5, column = 0, sticky = 'w')
entry_number_of_sets = tk.Entry(gui)
entry_number_of_sets.insert(0, 3)
entry_number_of_sets.grid(row = 5, column = 1, sticky = 'w')

exercise_duration = 0
exercise_duration_half = 0
label_exercise_duration = tk.Label(gui, text = "Exercise Length (sec):")
label_exercise_duration.grid(row = 6, column = 0, sticky = 'w')
entry_exercise_duration = tk.Entry(gui)
entry_exercise_duration.insert(0, 40)
entry_exercise_duration.grid(row = 6, column = 1, sticky = 'w')

rest_between_exercises = 0
label_rest_between_exercises = tk.Label(gui, text = "Rest Between Exercises (sec):")
label_rest_between_exercises.grid(row = 7, column = 0, sticky = 'w')
entry_rest_between_exercises = tk.Entry(gui)
entry_rest_between_exercises.insert(0, 20)
entry_rest_between_exercises.grid(row = 7, column = 1, sticky = 'w')

rest_between_sets = 0
label_rest_between_sets = tk.Label(gui, text = "Rest Between Sets (sec):")
label_rest_between_sets.grid(row = 8, column = 0, sticky = 'w')
entry_rest_between_sets = tk.Entry(gui)
entry_rest_between_sets.insert(0, 60)
entry_rest_between_sets.grid(row = 8, column = 1, sticky = 'w')

# Controls
button_calculate_time = tk.Button(gui, text = "Calculate Workout Duration", command = calculate_time)
button_calculate_time.grid(row = 10, column = 0, sticky = 'w')
label_calculate_time = tk.Label(gui, text = "")
label_calculate_time.grid(row = 10, column = 1, sticky = 'w')

button_start_workout = tk.Button(gui, text = "Start Workout", command = start_workout)
button_start_workout.grid(row = 11, column = 0, sticky = 'w')
label_workout_controls = tk.Label(gui, text = "Note: Hold P to Pause, C to Continue, or E to Exit")
label_workout_controls.grid(row = 11, column = 1, sticky = 'w')

# Status
label_status = tk.Label(gui, text = "")
label_status.grid(row = 12, column = 0, sticky = 'w')

# Start GUI loop
gui.mainloop()
