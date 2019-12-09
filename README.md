# RabbitExperimentScoring

## ./utils
存放阶段功能程序：
* Detector.py
* GiveMark.py
* StageEstimate.py
* time_clock.py

## ./detecting_files

存放权重文件:

* no_bn.caffemodel
* no_bn.prototxt

## ./model_params

存放阶段检测模型文件：

* inception/
* b1.txt
* b2.txt
* mean.txt
* neural.py
* PCA.txt
* W1.txt
* W2.txt

Detector.py 主要文件 目标检测类（包含测试）

GiveMark.py 评分模块

ScoresLine.json 评分模块配置文件
