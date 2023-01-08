import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import time

import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

import websocket
import json
import threading
import _thread
import time

from json import JSONEncoder

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
    
model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
movenet = model.signatures['serving_default']

def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    for person in keypoints_with_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)
        
def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0,255,0), -1)


EDGES = {
    (0,1): 'm',
    (0,2): 'c',
    (1,3): 'm',
    (2,4): 'c',
    (0,5): 'm',
    (0,6): 'c',
    (5,7): 'm',
    (7,9): 'm',
    (6,8): 'c',
    (8,10): 'c',
    (5,6): 'y',
    (5,11): 'm',
    (6,12): 'c',
    (11,12): 'y',
    (11,13): 'm',
    (13,15): 'm',
    (12,14): 'c',
    (14,16): 'c'
   
}

def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 4)
            
def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    #data = [x,y]
        #data = json.dumps({"sensor_type": 5, "data":x, "time" : time })
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder) 
    json_object = {
    "sensor_type":5, 
    "data":json.dumps(numpyData, cls=NumpyArrayEncoder) , 
    "time": time.time()
        }
    
    datas = json.dumps(json_object)
    ws.send(datas)

#Initiate a websocket running forever
def wsthread(numpyData):
    ws = websocket.WebSocketApp("ws://192.168.0.116:7891",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)  
    #print("Hello")
    ws.run_forever()

    
    
prev_frame_time = 0
new_frame_time = 0
#time1 = 0
cap = cv2.VideoCapture(0)

fr_count = 3
time_list=[]
fps_list =[]

while cap.isOpened():
    

    ret, frame = cap.read()
   
    new_frame_time = time.time()
    
    # Resize image
    img = frame.copy()
    
    img = tf.image.resize_with_pad(tf.expand_dims(img, axis=0), 192,256)
    height, width = img.shape[:2]
    input_img = tf.cast(img, dtype=tf.int32)
    
    # Detection section
    if fr_count%3 == 0:
            results = movenet(input_img,)
            keypoints_with_scores = results['output_0'].numpy()[:,:,0:51].reshape((6,17,3))
            ans=results['output_0'].numpy()[:,:,51:56]
            x_y_coords=keypoints_with_scores[:,:,0:2]
            numpyData = {"array": x_y_coords}
            # Render keypoints 
    loop_through_people(frame, keypoints_with_scores, EDGES, 0.4)
    #bounding box code
    x_min=ans[:,:,1:2]
    y_min=ans[:,:,0:1]
    x_max=ans[:,:,3:4]
    y_max=ans[:,:,2:3]
    c1=ans[:,:,4:5]
    #for i in range(0,6):
        
        #draw_bounding_box_on_image_array(frame,y_min[0][i][0],x_min[0][i][0],y_max[0][i][0],x_max[0][i][0],c1[0][i][0],'red',4,(),True)  
    time_list.append(new_frame_time-prev_frame_time)
    
    fps = 1/(new_frame_time-prev_frame_time)
    
    prev_frame_time = new_frame_time
    fps_list.append(1000/fps)
    fps = int(fps)
    fps = str(fps)
    gray = frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.imshow('Movenet Multipose', frame)
    
    
    
    fr_count+=1
    t = threading.Thread(target=wsthread, args=(numpyData))
    t.start() 
    if cv2.waitKey(5) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

#time_diff=np.diff(time_list)
fps_list=fps_list[1:]
