
"""test file."""
import cv2
import glob
import time
from utils.GiveMark import GradeSYS
from utils.Detector import Detector

video_path = ''

jason_file_path = './ScoresLine.json'
deploy_path = './detecting_files/no_bn.prototxt'
model_path = './detecting_files/no_bn.caffemodel'

detector = Detector(deploy_path, model_path, jason_file_path)
grade_sys = GradeSYS(jason_file_path)

video_cap = cv2.VideoCapture(video_path)

while video_cap.isOpened():
    ret, img = video_cap.read()
    img = detector.check_img(img)
    detector.print_checked_objects()
    grade_sys.begin_mark_line(detector.checkedObjects)
    grade_sys.print_transcript()
    cv2.imshow('Rabbit Experiments & Now scoring:',
               img)
    time.sleep(0.02)

print('Now experiment ends.')
print('Your final scoring is: ')
grade_sys.print_transcript()
