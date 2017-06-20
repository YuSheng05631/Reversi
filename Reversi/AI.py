import pygame
from Grid import GridsProcessing

class AI:
    def __init__(self, level:int, aiColor:bool):
        self.gridsProcessing = GridsProcessing()
        self.level = level      # 難度，決定AI預測level層
        self.aiColor = aiColor  # True: black, False: white
        self.weightsList = [[300,-90, 10, 10, 10, 10,-90,300],  # 權重
                            [-90,-90,  1,  1,  1,  1,-90,-90], 
                            [ 10,  1,  1,  1,  1,  1,  1, 10], 
                            [ 10,  1,  1, 10, 10,  1,  1, 10], 
                            [ 10,  1,  1, 10, 10,  1,  1, 10], 
                            [ 10,  1,  1,  1,  1,  1,  1, 10], 
                            [-90,-90,  1,  1,  1,  1,-90,-90], 
                            [300,-90, 10, 10, 10, 10,-90,300]]
        self.sideAndCorner = {(0, 1): (0, 0), (1, 0): (0, 0), (1, 1): (0, 0),   # { 角位邊: 角位 }
                              (0, 6): (0, 7), (1, 6): (0, 7), (1, 7): (0, 7), 
                              (6, 0): (7, 0), (6, 1): (7, 0), (7, 1): (7, 0), 
                              (6, 6): (7, 7), (6, 7): (7, 7), (7, 6): (7, 7)}
        self.sideAndEdge = {(1, 0): [(2, 0), (3, 0), (4, 0), (5, 0)],   # { 角位邊(除星位): 邊(除角位及角位邊)}
                            (6, 0): [(2, 0), (3, 0), (4, 0), (5, 0)], 
                            (0, 1): [(0, 2), (0, 3), (0, 4), (0, 5)], 
                            (0, 6): [(0, 2), (0, 3), (0, 4), (0, 5)], 
                            (1, 7): [(2, 7), (3, 7), (4, 7), (5, 7)], 
                            (6, 7): [(2, 7), (3, 7), (4, 7), (5, 7)],
                            (7, 1): [(7, 2), (7, 3), (7, 4), (7, 5)],
                            (7, 6): [(7, 2), (7, 3), (7, 4), (7, 5)]}

    def predict(self, occupiedGrids:dict):
        # print("\n====================\n")
        return self.predictR(occupiedGrids, True, self.aiColor, 0)[0]

    # chooseMax: 極大or極小。 nextColor: 下一步的顏色。 ct: 用來計數挖掘的層數。
    # point: 當前分數。 pointPruning: 判斷是否剪枝的分數(uncle)。
    def predictR(self, occupiedGrids:dict, chooseMax:bool, nextColor:bool, ct:int, point:int=None, pointPruning:int=None):
        # 挖到最後一層，return
        if ct >= self.level: return None, 0
        ct += 1
        # 取得提示(未確定能否吃子)
        hints = self.gridsProcessing.getNoCheckedHints(occupiedGrids, nextColor)
        # 遞迴
        cm = chooseMax ^ True
        nc = nextColor ^ True
        posM = None
        pointM = None
        hasCapture = False
        for h in hints:
            newGrids = dict(occupiedGrids)
            # 可以吃子
            if self.gridsProcessing.capture(newGrids, h, nextColor) is True:
                hasCapture = True
                posH, pointH = self.predictR(newGrids, cm, nc, ct, pointPruning=pointM)
                # print("{0}{1}: {2}".format("\t"*ct, h, pointH))
                # 判斷剪枝
                if pointPruning is not None:
                    if chooseMax is True and pointPruning < pointH: 
                        return None, 999999
                    elif chooseMax is False and pointPruning > pointH:
                        return None, -999999
                # 極大 or 極小
                if posM is None or\
                    chooseMax is True and pointH > pointM or\
                    chooseMax is False and pointH < pointM:
                    posM = h
                    pointM = pointH
        # 有下一步，return
        if hasCapture is True:
            # 計算當前分數 (第一層不需計算)
            if point is None:
                if ct != 1: point = self.getAIPoint(occupiedGrids)
                else : point = 0
            # print("{0} v {1}: {2}+{3}".format("\t"*ct, posM, point, pointM))
            return posM, point + pointM
        # 沒有下一步，當前分數改為無限，再進行遞迴
        else:
            if chooseMax is True: point = -999999
            else: point = 999999
            cm = chooseMax ^ True
            nc = nextColor ^ True
            posH, pointH = self.predictR(occupiedGrids, cm, nc, ct, point=point)
            # print("{0} v {1}: {2}+{3}".format("\t"*ct, posM, point, pointM))
            return posH, point + pointH

    def getAIPoint(self, occupiedGrids:dict):
        # p += AI 棋子總數 - Player 棋子總數
        # p += AI 權重分數 - Player 權重分數
        # p += AI 行動能力 - Player 行動能力
        point = 0
        for pos, status in occupiedGrids.items():
            # 若角位被佔，則角位邊的權重改為10
            if (pos in self.sideAndCorner and self.sideAndCorner[pos] in occupiedGrids):
                w = 10
            # 每一個邊(除角位及角位邊)被佔，同一邊的角位邊(除星位)權重+20
            elif (pos in self.sideAndEdge):
                w = self.weightsList[pos[0]][pos[1]]
                for edge in self.sideAndEdge[pos]:
                    if edge in occupiedGrids:
                        w += 20
            else:
                w = self.weightsList[pos[0]][pos[1]]
            if status is self.aiColor:
                point += 1 + w  # 棋子數 & 權重
            else:
                point -= 1 + w  # 棋子數 & 權重
        return point
