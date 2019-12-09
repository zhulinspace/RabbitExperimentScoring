
"""test file."""
import cv2
import glob
from utils.GiveMark import GradeSYS
from utils.Detector import Detector


jason_file_path = './ScoresLine.json'
deploy_path = './detecting_files/no_bn.prototxt'
model_path = './detecting_files/no_bn.caffemodel'

detector = Detector(deploy_path, model_path, jason_file_path)
grade_sys = GradeSYS(jason_file_path)
imgStream = glob.glob("./img_catching/*.png")  # 获取img路径下的所有 jpg 图片
for img in imgStream:
    img = cv2.imread(img)
    img = detector.check_img(img)
    detector.print_checked_objects()
    grade_sys.begin_mark_line(detector.checkedObjects)
    grade_sys.print_transcript()
    cv2.imshow("img", img)
    k = cv2.waitKey(0)
    if k == ord('q'):
        break
