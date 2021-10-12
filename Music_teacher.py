'''
this is the main function of the program,
1, it reads and formats the input from the user
2, it called corresponding applications based on user input
'''
from pitchcoach import audio_pitch, steps_diff, transpose_checker
from note_freq import note, freq, note_freq_dict 
import os

app_collection = {
  1: 'Transposition',
  2: 'Singing'
}

def get_tonic(str):
  invalid = False
  str = str.lower()
  
  note_list = ['c','d','e','f','g','a','b']
  key_note, accidental  = '', ''
  if 'sharp' in str or 'flat' in str: accidental += '#'
  
  for note in note_list:
    if ' ' + note + ' ' in str or \
       (' ' + note in str and str.index(' ' + note) == len(str) - 1) or \
         (note + ' ' in str and str.index(note + ' ') == 0):
      key_note += note
      break

  #bad user input
  if key_note == '':
    return None
  #print('debug: ',key_note)
  if len(accidental) == 1 and 'flat' in str:
    key_note = note_list[note_list.index(key_note)-1]
  
  key_note = key_note.upper()
  return key_note  + '4' + accidental # move note to the middle C part


def main():
  running = True

  while (running):
    # strip() removes the spaces at the beginning & ending of a string
    print('Hi, It\'s Music Training Time!!!')
    select_flag = 'y'
    while 'y' in select_flag.lower():
      app = input('Select the skill number u wanna improve this time: 1, Transposition  2, Singing')
      if app != '1':
        select_flag = input('Sorry!! This application is still developing. Do u wanna select another again? (y/n)')
        if 'n' in select_flag.lower(): 
          print('bye')
          return
      else: break
    org_melody = input('What is the filename of assigned melody? ').strip()
    while not os.path.exists('input_data/' + org_melody + '.wav'):
      org_melody = input('File doesn\'t exist. What is the filename of assigned melody? ').strip()
    org_melody_key = input('What is its key? ("key Major/minor") ').strip()
    org_key = get_tonic(org_melody_key)
    #print(org_key)
    while org_key == None:
      org_melody_key = input('Invalid key signature, plz enter again: ("key Major/minor") ').strip()
      org_key = get_tonic(org_melody_key)
      #print(org_key)

    trp_melody = input('What is the filename of your transposition melody? ').strip()
    while not os.path.exists('input_data/' + trp_melody + '.wav'):
      trp_melody = input('File doesn\'t exist. What is the filename of assigned melody? ').strip()
    trp_melody_key = input('What is the transposition key? ("key Major/minor") ').strip()
    trp_key = get_tonic(trp_melody_key)
    while trp_key == None:
      trp_melody_key = input('Invalid key signature, plz enter again: ("key Major/minor") ').strip()
      trp_key = get_tonic(trp_melody_key)
    # format input
    #print(trp_key)
    # get the HZ lists of two files
    # contrast and find the mistake

    print("Please wait...")
    trans_step = steps_diff(org_key, trp_key)
    #print("trans_step", trans_step)
    o_melody_freq, o_melody_notes = audio_pitch(org_melody)
    trp_melody_freq, trp_melody_notes = audio_pitch(trp_melody)
    wrong_note, score = transpose_checker (o_melody_notes, trp_melody_notes, trans_step)

    print("You scored", score)
    print("There are", len(wrong_note), "wrong notes.")
    if len(wrong_note) > 0:
      for note1, note2, correct, i in wrong_note:
        print("Note #", i+1, ", original ", note1, ", you played ", note2, ", the correct note is ", correct, sep = '')

    exit = input('exit? (y/n)')
    if 'y' in exit or 'Y' in exit: 
      print('bye')
      running = False
  

if __name__=="__main__":
  main()