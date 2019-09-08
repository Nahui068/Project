import face_recognition
import cv2
import numpy as np
import os
import time

def face_register(name):
    start_time=time.time()
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_name = name
    process_this_frame = True
    face_yn=None
    while (True):
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            for face_encoding in face_encodings:
                np.save('face/'+face_name+'.npy', face_encoding)
                face_yn=face_name
                print(face_yn)     
        process_this_frame = not process_this_frame
        if face_yn!=None:
            break
        if time.time()-start_time>15:
            face_yn='timeout'
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return face_yn
def face_regonize():
    start_time=time.time()
    known_face_encodings = []
    known_face_names = []
    files = os.listdir('face')
    for filename in files:
        name, ext = os.path.splitext(filename)
        if ext == '.npy':
            known_face_names.append(name)
            known_face_encodings.append(np.load('face/'+filename))
    video_capture = cv2.VideoCapture(0)
    face_locations = []
    face_encodings = []
    face_name = None 
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            for face_encoding in face_encodings:
                distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                min_value=min(distances)
                print(min_value)
                if min_value<0.6:
                    index = np.argmin(distances)
                    face_name = known_face_names[index]
        process_this_frame = not process_this_frame
        if face_name!=None:
            print(face_name)
            break
        if time.time()-start_time>15:
            face_name='timeout'
            break
    video_capture.release()
    cv2.destroyAllWindows()
    return face_name