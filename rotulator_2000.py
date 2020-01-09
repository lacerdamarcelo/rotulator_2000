import os
import glob
from pygame import mixer
import pandas as pd
import numpy as np

f = open('title_screen.txt', 'r')
title_screen = f.read()
f.close()
mixer.init()
mixer.music.load('y2mate.com - doom_ost_e1m1_at_dooms_gate_BSsfjHCFosw.mp3')
mixer.music.play()
os.system('cls' if os.name == 'nt' else 'clear')
print(title_screen)
correct_path = False
while correct_path is False:
    path = input('Insert the path to the csv files (leave it blank if you want to use your current path): ')
    path = './' if path == '' else path
    if os.path.exists(path) is False:
        print("ERROR: Path does not exist. Please, type another one.")
    else:
        correct_path = True
label = input('Type the label of your task: ')
mixer.music.stop()
mixer.music.load('y2mate.com - ak47_shoot_csgo_sound_effect_DYWi8qdvWCk.mp3')
mixer.music.play()
try:
    f = open('verified_files.txt', 'x')
    f.close()
except Exception:
    pass
f = open('verified_files.txt', 'r')
complete = f.readlines()
f.close()
for i in range(len(complete)):
    complete[i] = complete[i].split('\n')[0]
for filename in glob.glob(os.path.join(path, '*.csv')):
    if filename not in complete:
        current_process = pd.read_csv(filename)
        current_process = current_process[current_process['label'] != np.NAN]
        if current_process.shape[0] != 0:
            current_process = current_process[current_process['label'] == label]
            label_index = current_process.columns.tolist().index('label')
            at_least_one_valid = False
            index = 0
            invalid_command = False
            expand = False
            while index < current_process.shape[0]:
                os.system('cls' if os.name == 'nt' else 'clear')
                if expand is False:
                    print(current_process.iloc[[index]]['text'].values[0][:1000])
                else:
                    print(current_process.iloc[[index]]['text'].values[0])
                print('=========================================')
                if invalid_command is True:
                    print('Invalid command!')
                print('You have %d complete processes.' % len(complete))
                print('Process number:', current_process.iloc[[index]]['process'].values[0])
                print('Type \'d\' to confirm the label and go next, \'s\' to go next and reject the label, and \'a\' to go back.')
                print('Hint : type \'e\' to expand text.')
                command = input()
                if command == 'd':
                    current_process.iloc[index,label_index] = label
                    index += 1
                    invalid_command = False
                    expand = False
                elif command == 's':
                    current_process.iloc[index,label_index] = np.NAN
                    index += 1
                    invalid_command = False
                    expand = False
                elif command == 'a':
                    index -= 1
                    invalid_command = False
                    expand = False
                elif command == 'e':
                    expand = True
                    invalid_command = False
                else:
                    invalid_command = True
                    expand = False
                index = 0 if index < 0 else index
                os.system('cls' if os.name == 'nt' else 'clear')
            current_process.to_csv(filename, index=False)
        complete.append(filename)
        f = open('verified_files.txt', 'a')
        f.write(filename + '\n')
        f.close()
