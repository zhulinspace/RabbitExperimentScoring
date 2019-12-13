import json
import sys

sys.path.append('utils/')


# 评分系统 维护一个实现了 GiveMark 接口的函数队列 用于给当前的 checkedObjects 评分
class GradeSYS:
    def __init__(self, configFile):
        self.pakage = __import__("GiveMark")  # 获取当前包的引用
        self.transcript = {}  # 维护一个成绩单字典 用于保存评分结果
        self.commandLine = []  # 维护一个评分操作的列表

        with open(configFile, "r", encoding="utf-8") as fp:  # 由 config 确定哪些评分项需要被载入
            config = json.load(fp)
            self.stageList = config['scoresLine']

        for stage in self.stageList:
            stage_func_name = getattr(self.pakage, stage)  # 获取目标类的引用
            stage_func = stage_func_name(self.transcript)  # 给入成绩单，创建一个评分对象
            self.commandLine.append(stage_func)  # 将评分对象加入执行链

    def begin_mark_line(self, checkedObjects):
        if len(self.commandLine) < 1:
            return False
        # 给入当前的目标检测情况 开始一个轮次的评分
        for stage_func in self.commandLine:
            if stage_func.give_mark(checkedObjects):
                # 如果返回值为 True 则表示该项测试已结束 将其移出评分序列
                self.commandLine.remove(stage_func)
            else:
                break

    def get_now_stage(self):
        return "{}".format(self.commandLine[0])

    def print_transcript(self):
        print('now your transcript is: ', self.transcript)

    def get_transcript(self):
        return self.transcript
    # @property
    # def transcript(self):
    #     return self.transcript
    # @transcript.setter
    # def transcript(self, name, score):
    #     self.transcript[name] = score


# 所有评分函数的接口
class GiveMark:
    def __init__(self, transcript):
        """
        目前已经检测到的目标  checkedObjects 为一个列表，下标即为对应的 Object
        0：兔子  1：剪刀  2：伤口  3：手  4：耳朵  5：针头
        列表的值:
         [0]:是否出现
         [1]: Object 到目前为止出现的次数(为了减小错误识别造成的影响，暂定出现40次时确定该物品已被检测到)
         [2]:一个标识 Object 当前位置的元组
        """
        self.transcript = transcript
        self.minTimes = 40

    def give_mark(self, transcript):
        print("You got 99 points!")



# =====================所有的评分方法在此添加============================================
class CheckCatching(GiveMark):
    def give_mark(self, checkedObjects):
        # 针头出现 阶段判0
        if checkedObjects[6][0] == 1:
            self.transcript['Catch'] = 0
            return True
        # print('now catching')
        stage = checkedObjects[6][0]
        rabbit_pos = checkedObjects[0][2]
        rabbit_center_x = (rabbit_pos[0] + rabbit_pos[2]) / 2
        rabbit_center_y = (rabbit_pos[1] + rabbit_pos[3]) / 2
        # if stage == 0 and \
        #         640 < rabbit_center_x < 1280 and \
        #         360 < rabbit_center_y < 720 :
        #         checkedObjects[0][0] > self.minTimes:
        if 640 < rabbit_center_x < 1280 and 360 < rabbit_center_y < 720 :
            # print('有效的抓拿判断帧...')
            if checkedObjects[3][0] == 1 and checkedObjects[4][0] == 1:
                hand_pos = checkedObjects[3][2]
                ear_pos = checkedObjects[4][2]
                judge = self.judge_catching(hand_pos, ear_pos)
                if judge:
                    self.transcript['Catch'] = 10
                else:
                    self.transcript['Catch'] = 0
                # print('抓拿判定结束')
                return True


    def judge_catching(self, hand_pos, ear_pos):
        if ear_pos[2] < hand_pos[0]:
            # print('错误！抓屁股')
            return False
        elif ear_pos[0] > hand_pos[0] - 30 and ear_pos[2] < hand_pos[2] + 30:
            # print('错误！抓耳朵')
            return False
        else:
            return True

class CheckNeedle(GiveMark):
    """
    TODO
    """

    def give_mark(self, checkedObjects):
        if checkedObjects[2][0] == 1:
            self.transcript['Needle'] = 0
            return True
        # print("针头检测开始...")
        needle_appearance = checkedObjects[5][1]
        if needle_appearance > self.minTimes:
            self.transcript['Needle'] = 10
            return True
        # print("针头检测结束")
        return False

class CheckFixed(GiveMark):
    # 检查是否固定
    def give_mark(self, checkedObjects):
        # print("固定检测开始...")
        if checkedObjects[2][1] > self.minTimes:
            self.transcript['fixed'] = 10
            # print("固定成功")
            return True
        # print("固定检测结束")
        return False

class CheckWound(GiveMark):
    # 检查伤口是否存在
    def give_mark(self, checkedObjects):
        # print("伤口检测开始...")
        if checkedObjects[2][1] > self.minTimes:
            self.transcript['Wound'] = 10
            # print("检测到伤口")
            return True
        # print("伤口检测结束")
        return False

class CheckNerve(GiveMark):
    """
    TODO
    """
    times = 0

    def give_mark(self, checkedObjects):
        self.times += 1
        # print("神经检测开始...")
        if self.times >= 20:
            self.transcript['Nerve'] = 10
            return True
        # print("神经检测结束")
        return False


# ======================================================================================


# 测试
if __name__ == '__main__':
    gs = GradeSYS("../ScoresLine.json")

    checkedObjects = [[] for i in range(6)]
    checkedObjects[2].append(43)
    checkedObjects[2].append((1, 1, 1, 1))
    checkedObjects.append([0, 1, 2, 3])
    print(checkedObjects)

    gs.begin_mark_line(checkedObjects)

    gs.print_transcript()
