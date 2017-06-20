import time

class GridsProcessing:
    def __init__(self):
        self.directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    # 取得比分
    def getScore(self, occupiedGrids:dict):
        score = [0, 0]
        for status in occupiedGrids.values():
            if status is True:
                score[0] += 1
            else:
                score[1] += 1
        return score

    # 吃子 (Return has captures or not)
    def capture(self, occupiedGrids:dict, pos:tuple, nextColor:bool):
        if pos in occupiedGrids.keys():
            return False
        ct = 0
        for d in self.directions:
            # 找出d方向可以造成包夾的棋子
            now = [pos[0] + d[0], pos[1]+ d[1]]
            while now[0] >= 0 and now[0] <= 7 and now[1] >= 0 and now[1] <= 7:
                if (now[0], now[1]) not in occupiedGrids:   # 是空的
                    break
                if occupiedGrids[(now[0], now[1])] == nextColor:    # 找到了
                    # 取得d方向可以吃掉的棋子
                    now[0] -= d[0]
                    now[1] -= d[1]
                    while now[0] != pos[0] or now[1] != pos[1]:
                        ct += 1
                        occupiedGrids[(now[0], now[1])] = nextColor
                        now[0] -= d[0]
                        now[1] -= d[1]
                    now[0] = -9 # break
                now[0] += d[0]
                now[1] += d[1]
        if ct == 0: return False
        occupiedGrids[pos] = nextColor
        return True

    # 取得提示(Return list of pos)
    def getHints(self, occupiedGrids:dict, nextColor:bool):
        hints = list()
        for pos, status in occupiedGrids.items():
            if status is nextColor:
                continue
            for d in self.directions:
                # 確定d的反方向一格是空的、沒有在hints裡、沒有超出邊界
                r = (pos[0] - d[0], pos[1] - d[1])
                if r in occupiedGrids or r in hints or r[0] == -1 or r[0] == 8 or r[1] == -1 or r[1] == 8:
                    continue
                # 找出d方向可以造成包夾的棋子
                times = 0
                now = [pos[0], pos[1]]
                while now[0] >= 0 and now[0] <= 7 and now[1] >= 0 and now[1] <= 7:
                    if (now[0], now[1]) not in occupiedGrids:   # 是空的
                        break
                    if occupiedGrids[(now[0], now[1])] == nextColor:    # 找到了
                        if times >= 1:
                            hints.append(r)
                        break
                    now[0] += d[0]
                    now[1] += d[1]
                    times += 1
        return hints

    # 取得提示(未確定能否吃子)
    def getNoCheckedHints(self, occupiedGrids:dict, nextColor:bool):
        hints = list()
        for pos, status in occupiedGrids.items():
            if status is nextColor:
                continue
            # 取得所有周邊位置
            for d in self.directions:
                a = (pos[0] + d[0], pos[1] + d[1])
                # 沒有在 occupiedGrids 和 hints 裡、沒有超出邊界
                if a in occupiedGrids or a in hints or a[0] == -1 or a[0] == 8 or a[1] == -1 or a[1] == 8:
                    continue
                hints.append(a)
        return hints
