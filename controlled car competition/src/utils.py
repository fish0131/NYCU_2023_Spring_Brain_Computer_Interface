from screeninfo import get_monitors
import pygame
from pygame.locals import *
import os
import sys
from flick import Flick
import time
from record_data import RecordData
from live_recorder import LiveRecorder
import joblib
import numpy as np
from preprocess import preprocess_recordings
from subprocess import Popen
import matplotlib.pyplot as plt
import serial
import argparse

pygame.init()


def get_display_resolution():
    """
    | Returns half of width and height of screen in pixels
    """
    h_str = str(get_monitors()[0])
    for char in ['+', '(', ')', 'x']:
        h_str = h_str.replace(char, '|')
    w, h = (h_str.split('|')[1], h_str.split('|')[2])
    #print(h)
    return (1920, 1080)


def time_str():
    return time.strftime("%H_%M_%d_%m_%Y", time.gmtime())


def render_waiting_screen(text_string=None, time_black = 0.):
    pygame.font.init()
    display_x, display_y = get_display_resolution()
    display_x, display_y = (2 * display_x, 2 * display_y)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    window = pygame.display.set_mode((display_x, display_y), pygame.NOFRAME, 32)
    pygame.display.set_caption("SSVEP")
    if time_black > 0:
        window.fill((0., 0., 0.))
        timer_event = USEREVENT + 1
        pygame.time.set_timer(timer_event, int(time_black)*1000)
    else:
        myfont = pygame.font.SysFont("arial", 50)
        press_string = "Please press the Any-Key to continue..."
        textsurface1 = myfont.render(press_string, False, (0, 0, 0))
        text_rect1 = textsurface1.get_rect(center=(display_x/2, display_y/2+100))
        if text_string:
            textsurface2 = myfont.render(text_string, False, (0, 0, 0))
            text_rect2 = textsurface2.get_rect(center=(display_x/2, display_y/2-100))
        window.fill((100, 100, 150))
        window.blit(textsurface1, text_rect1)
        if text_string:
            window.blit(textsurface2, text_rect2)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                else:
                    pygame.quit()
                    return False
            if not (time_black > 0.):
                window.blit(textsurface1, text_rect1)
                if text_string:
                    window.blit(textsurface2, text_rect2)
            else:
                if event.type == timer_event:
                    pygame.quit()
                    return False
            pygame.display.update()


def begin_experiment_1(freq, savename, trials=1):
    if not os.path.isdir("REC"):
        os.mkdir("REC")
    render_waiting_screen("Welcome to this experiment")
    render_waiting_screen("The experiment will start now... there will be breaks between the flickering tiles!")
    recorder = RecordData(1000., 20., freq)
    recorder.start_recording()

    for i in range(0, int(trials)):
        recorder.add_trial(int(freq))
        Flick(float(freq)).flicker(15.)
        recorder.add_trial(0.)
        render_waiting_screen(text_string=None, time_black=5.)

    filename = "REC/%s_%s_freq_%s.mat" % (savename, time_str(), freq)
    recorder.stop_recording_and_dump(filename)
    recorder.killswitch.terminate = True
    recorder = None

    render_waiting_screen("That was the last one, thank you for participation!")


def begin_experiment_2(str_list):
    display_x, display_y = get_display_resolution()
    display_x, display_y = (2 * display_x, 2 * display_y)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    window = pygame.display.set_mode((display_x, display_y), pygame.NOFRAME, 32)
    pygame.display.set_caption("SSVEP")
    window.fill((0, 0, 0))
    pygame.display.update()

    if os.name == 'nt':
    	for command in str_list:
            command_parts = command.split(" ")
            Popen(command_parts)
    elif os.name == 'posix':
        os.system("|".join(str_list))
    else:
        print("Could not get OS-name!")


def start_live_classifier():
    window_metrics = (200, 200)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    window = pygame.display.set_mode(window_metrics, pygame.NOFRAME, 0)
    pygame.display.set_caption("classifier window")
    pygame.mouse.set_visible(False)
    arrow = pygame.transform.scale(pygame.image.load("src/res/arrow.png"), window_metrics)
    stop = pygame.transform.scale(pygame.image.load("src/res/stop.png"), window_metrics)
    arrow_metrics = window_metrics
    window.blit(stop, (0, 0))
    pygame.display.update()
    # Start Recording
    recorder = LiveRecorder(sampling_frequency = 1000)
    recorder.start_recording()
    time.sleep(1)

    do_run = True
    model_file_QDA, model_file_LDA, model_file_MLP = ('src/QDA.pkl', 'src/LDA.pkl', 'src/MLP.pkl')

    QDA = joblib.load(model_file_QDA)
    LDA = joblib.load(model_file_LDA)
    MLP = joblib.load(model_file_MLP)

    label = None
    time.sleep(5)

    label_list = []

    while do_run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN or label:
                try:
                    a = event.key
                    label = None
                except AttributeError:
                    event.key = None
                if event.key == K_ESCAPE:
                    do_run = False
                elif event.key == K_UP or label == 13.0:    # UP is 13 Hz
                    window.fill((0., 0., 0.))
                    window.blit(rot_center(arrow, 180), (0, 0))
                    # TODO move robot up
                elif event.key == K_DOWN or label == 17.0:  # DOWN is 17 Hz
                    window.fill((0., 0., 0.))
                    window.blit(arrow, (0, 0))
                    # TODO move robot down
                elif event.key == K_RIGHT or label == 15.0:    # RIGHT is 15 Hz
                    window.fill((0., 0., 0.))
                    window.blit(rot_center(arrow, 90), (0, 0))
                    # TODO move robot right
                elif event.key == K_LEFT or label == 19.0:   # LEFT is 19 Hz:
                    window.fill((0., 0., 0.))
                    window.blit(rot_center(arrow, 270), (0, 0))
                    # TODO move robot left
                elif event.key == K_SPACE or label == 0.0:  # No frequency
                    window.fill((0., 0., 0.))
                    window.blit(stop, (0, 0))
                    # TODO stop robot
                label = None

            elif event.type == KEYUP:
                window.fill((0., 0., 0.))
                window.blit(stop, (0, 0))
                # TODO stop robot

            pygame.display.flip()

        features = recorder.get_features()
        label_LDA = LDA.predict([features])[0]
        label_QDA = QDA.predict([features])[0]
        label_MLP = MLP.predict([features])[0]
        print("LDA: %s QDA: %s MLP: %s" %(label_LDA, label_QDA, label_MLP))
        for tmp_label in [label_LDA, label_QDA, label_MLP]:
            label_list.append(tmp_label)

        if len(label_list) >= 10*3:
            count_list = [label_list.count(13.), label_list.count(15.)]
            count_list.append(label_list.count(17.))
            count_list.append(label_list.count(19.))
            index = np.argmax(count_list)
            label = [13., 15., 17., 19.][index]
            print("Mayor Label: %s" % label)
            label_list = []

        time.sleep(1.)

    #   May dump labeled data after recording?
    filename = "REC/live_%s_freq_%s.mat" % (time_str(), freq)


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def begin_car(code, freq, savename='', trials=1):
    if not os.path.isdir("REC"):
        os.mkdir("REC")
    render_waiting_screen("Welcome to this experiment")
    render_waiting_screen("Code "+str(code), time_black=2.)
    recorder = RecordData(1000., 10., freq)
    recorder.start_recording()

    for i in range(0, int(trials)):
        recorder.add_trial(int(freq))
        Flick(float(freq)).flicker(8.)
        recorder.add_trial(0.)
        render_waiting_screen(text_string=None, time_black=2.)

    filename = "REC/%s_%s_freq_%s.mat" % (savename, time_str(), freq)
    data = recorder.stop_recording_and_dump(filename) #get record X
    recorder.killswitch.terminate = True
    recorder = None

    fft_data = np.fft.fft(np.array(data)[:, 4])
    plt.plot(np.abs(fft_data)[int(len(fft_data)/1000*5):int(len(fft_data)/1000*15),])
    plt.savefig("REC/%s_%s_freq_%s.png" % (savename, time_str(), freq))
    alpha_max = np.max(np.abs(fft_data)[int(len(fft_data)/1000*5):int(len(fft_data)/1000*15),])
    peak_alpha = np.sum(np.abs(fft_data)[int(len(fft_data)/1000*5):int(len(fft_data)/1000*15),])
    peak_normal = np.sum(np.abs(fft_data)[int(len(fft_data)/1000*3):int(len(fft_data)/1000*30),])

    print("alpha max: ", alpha_max)
    print("alpha value:", (peak_alpha))
    print("normal value:", (peak_normal))
    print("peak value:", (peak_alpha / peak_normal))
    if (peak_alpha / peak_normal) < 0.5:
        pred = 0    
    else:
        pred = 1   
    print("pred: ", pred)
    return pred
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CECNL BCI 2023 Car Demo")
    parser.add_argument("port_num", type=str, help="Arduino bluetooth serial port")
    args = parser.parse_args()

    ser = serial.Serial(args.port_num, 9600, timeout=1, write_timeout=1)

    code =[]
    for i in range(2):
         code.append(begin_car(i, 1, i))
    #code = [1,0]
    # forward 開閉 
    # right 開開
    # left 閉開
    if code == [0,1]: 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1')
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1')
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
    elif code == [0, 0]:
        ser.write(b'4') 
        ser.write(b'0')
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1')
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1')
        ser.write(b'1')
        ser.write(b'1')
    elif code == [1, 0]:
        ser.write(b'3') 
        ser.write(b'0')
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1')
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1') 
        ser.write(b'1')
    
    # if code == [0,1]:   # forward 開閉
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    #     ser.write(b'1')  
    #     ser.write(b'3')  
    #     ser.write(b'3')  
    #     ser.write(b'3') 
    #     ser.write(b'3')
    #     ser.write(b'3') 
    #     ser.write(b'3') 
    #     ser.write(b'1')  
    #     ser.write(b'1') 
    #     ser.write(b'3')  
    #     ser.write(b'1')  
    #     ser.write(b'1')  
    #     ser.write(b'1') 
    #     ser.write(b'3') 
    #     ser.write(b'3') 
    #     ser.write(b'3')  
    #     ser.write(b'3') 
    #     ser.write(b'3')  
    #     ser.write(b'3')  
    #     ser.write(b'1')  
    #     ser.write(b'3') 
    #     ser.write(b'3') 
    #     ser.write(b'1')  
    #     ser.write(b'1') 
    # elif code == [0,0]:   # right 開開
    #     ser.write(b'4') 
    #     ser.write(b'1') 
    #     ser.write(b'0') 
    #     ser.write(b'3')  
    #     ser.write(b'1')  
    #     ser.write(b'0') 
    #     ser.write(b'4') 
    #     ser.write(b'0') 
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    #     ser.write(b'0') 
    #     ser.write(b'3') 
    #     ser.write(b'0') 
    #     ser.write(b'4') 
    #     ser.write(b'0') 
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    #     ser.write(b'0') 
    #     ser.write(b'1') 
    # elif code == [1,0]:   # left 閉開
    #     ser.write(b'3')  
    #     ser.write(b'4') 
    #     time.sleep(0.01)
    #     ser.write(b'1') 
    #     ser.write(b'3')  
    #     ser.write(b'3')  
    #     ser.write(b'0') 
    #     ser.write(b'0') 
    #     ser.write(b'3') 
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    #     ser.write(b'1') 
    

    ser.write(b'0')  