import os
import pickle

import mediapipe as mp
import cv2
import numpy as np


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'
DATASIZE = 100

data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    processed = -1
    if (not os.path.isdir(os.path.join(DATA_DIR, dir_))):
        continue

    print("reading")
    for img_path in os.listdir(os.path.join(DATA_DIR, dir_)):
        processed += 1
        data_aux = []

        x_ = []
        y_ = []

        img = cv2.imread(os.path.join(DATA_DIR, dir_, img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))
            
                if (len(x_) > 21):
                    print(dir_)
            if (processed < DATASIZE):
                data.append(data_aux)
                labels.append(dir_)
            else:
                data[processed - DATASIZE] = np.subtract(data[processed - DATASIZE], data_aux)
        else:
            print("exception")

f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels': labels}, f)
f.close()
