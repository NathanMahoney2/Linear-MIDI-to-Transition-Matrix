#midi to matrix
import mido
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


mid = mido.MidiFile('todos.mid', clip=True)
res = mid.tracks
#print(res)

arr = []
for message in res[0]:
    if message.type == 'note_on':
        arr.append(message.note)



# Dictionary mapping MIDI note numbers to their corresponding note names
note_map = {
    35: "B1", 36: "C2", 37: "C#2", 38: "D2", 39: "D#2", 40: "E2",
    41: "F2", 42: "F#2", 43: "G2", 44: "G#2",
    45: "A2", 46: "A#2", 47: "B2", 48: "C3", 49: "C#3", 50: "D3",
    51: "D#3", 52: "E3", 53: "F3", 54: "F#3", 
    55: "G3", 56: "G#3", 57: "A3", 58: "A#3", 59: "B3",
    60: "C4", 61: "C#4", 62: "D4", 63: "D#4", 64: "E4", 
    65: "F4", 66: "F#4", 67: "G4", 68: "G#4", 69: "A4", 
    70: "A#4", 71: "B4", 72: "C5", 73: "C#5"
}

note_mapy = {
    35: "B0", 36: "C1", 37: "C#1", 38: "D1", 39: "D#1", 40: "E1",
    41: "F1", 42: "F#1", 43: "G1", 44: "G#1",
    45: "A1", 46: "A#1", 47: "B1", 48: "C2", 49: "C#2", 50: "D2",
    51: "D#2", 52: "E2", 53: "F2", 54: "F#2", 
    55: "G2", 56: "G#2", 57: "A2", 58: "A#2", 59: "B2",
    60: "C3", 61: "C#3", 62: "D3", 63: "D#3", 64: "E3", 
    65: "F3", 66: "F#3", 67: "G3", 68: "G#3", 69: "A3", 
    70: "A#3", 71: "B3", 72: "C4", 73: "C#4"
}

notes = []
# Iterate through each key in the note_map dictionary in ascending order
for key in sorted(note_map.keys()):
    occurrences = {}  # Reset occurrences dictionary for each iteration
    # Iterate through each element in the array 'arr'
    for i in range(len(arr) - 1):
        # Check if the current element in 'arr' matches the current MIDI note number
        if arr[i] == key:
            next_num = arr[i + 1]  # Get the next number in the array
            # Update the occurrences dictionary with the count of the next number
            if next_num not in occurrences:
                occurrences[next_num] = 1
            else:
                occurrences[next_num] += 1
    # Check if there are any occurrences for the current note
    #if occurrences:
    current_note = note_map[key]  # Get the corresponding note name for the MIDI note number
    #print(f"Occurrences of each number following: {current_note}")  # Print the current note name
    
    # Sort occurrences by key (next number)
    sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[0])
    
    # Iterate through each item in sorted_occurrences and print the note and its count
    #for num, count in sorted_occurrences:
    #    print(f"{note_map[num]}: {count}")  # Print the note and its count
    
    # Calculate the total count of occurrences
    count_array = list(occurrences.values())
    summed = sum(count_array)
    

   # Normalize the count_array to get probabilities
    probabilities = []  # List to hold the probabilities for each note
    for note_num in range(35, 74):  # Range for notes C4 to A4
        if note_num in occurrences:
            probabilities.append(occurrences[note_num] / summed)
        else:
            probabilities.append(0)  # Assign zero probability if no occurrences
    
    # Ensure that the final array contains 30 values
    while len(probabilities) < 30:
        probabilities.append(0)

    print(end="")
    note_names = []
    note_prob = []

    for note_num in range(35, 74):  # Range for notes B1 to D5
        if note_num in note_map:
            note_names.append(note_map[note_num])
            note_prob.append(probabilities[note_num - 35])  # Adjust index to start from 0

    #print(note_names2)
    data = {'Note': note_names, 'Probability': note_prob}
    df = pd.DataFrame(data)
    #df.to_excel('output.xlsx', index=False)
    #print(df)
    notes.append(note_prob)
print(notes)
#df = pd.DataFrame(notes)

#note_names_x = [note_map[i] for i in range(35, 73)] 
#note_names_y = [note_mapy[i] for i in range(35, 73)] 
#df

import numpy as np

# initialize your markov chain matrix
P = np.array(notes)
# Find the indices of rows with all zeros
zero_rows = np.all(P == 0, axis=1)

# Replace the rows with all zeros with the desired value (0.25)
P[zero_rows] = (1/len(P))
#df = pd.DataFrame(P)
#df.to_excel('output.xlsx', index=False)
#print(df)
# initialize your states
meep = [0]

# select a random state to begin with
states = len(P)

state_now = np.random.choice(meep,1)

#print(state_now)
# initialize the previos state
state_prev = None
# number of travels in your markov chain diagram
iter = 10

for i in range(iter):
  # get the vector of probabilities to go from the current state to all other states
  prob = P[state_now]
  #print(prob)
  # select the next satet based on the probability vector of above
  #print(prob[0])
  
  next_state = np.random.choice(states,1, p=prob[0])

  # update the current state and the previous state
  state_prev = state_now
  state_now = next_state
  # print the transition
  print(state_prev, ' -> ', state_now)
