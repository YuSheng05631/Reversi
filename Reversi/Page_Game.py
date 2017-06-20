import pygame, time
from AI import AI
from Grid import GridsProcessing

class Page_Game:
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()
        self.AI = None
        self.gridsProcessing = GridsProcessing()
        self.occupiedGrids = dict()                     # {(x, y): status} # status = True: black, False: white
        self.level = 0
        self.gbIndex = 0
        self.nextColor = False                          # True: black, False: white
        self.nextPlayer = False                         # True: player1, False: player2 / AI
        self.score = [2, 2]                             # black: white
        self.hints = list()
        self.prevPlay = None
        self.displayText = []                           # [P1_Name:str, P2_Name:str, P1_Color:bool]
        self.isOver = False
        self.startTime = 0
        self.timingOver = False

    # 初始化 occupiedGrids
    def initOccupiedGrids(self):
        self.occupiedGrids[(3, 3)] = False
        self.occupiedGrids[(3, 4)] = True
        self.occupiedGrids[(4, 3)] = True
        self.occupiedGrids[(4, 4)] = False

    # 更新nextPlayer、nextColor、hints
    def updateStatus(self, isTwoTimes:bool=False):
        self.nextPlayer = self.nextPlayer ^ True
        self.nextColor = self.nextColor ^ True
        # 更新hints
        self.hints = self.gridsProcessing.getHints(self.occupiedGrids, self.nextColor)
        # 沒有地方下
        if len(self.hints) == 0 and isTwoTimes is False:    # 換另一方
            self.updateStatus(True)
        if len(self.hints) == 0:    # 兩方都沒有地方下
            self.isOver = True

    # 產生顯示文字
    def generateDisplayText(self):
        self.displayText.append("Player 1")
        if self.level != 0: self.displayText.append("AI (Lv.{0})".format(self.level))
        else: self.displayText.append("Player 2")
        self.displayText.append(self.nextPlayer)

    # 玩家下棋
    def moveByPlayer(self, pos):
        if pos[0] > 60 and pos[0] < 540 and pos[1] > 60 and pos[1] < 540:
            x = int((pos[0] - 60) / 60)
            y = int((pos[1] - 60) / 60)
            if self.gridsProcessing.capture(self.occupiedGrids, (x, y), self.nextColor):
                if self.nextColor is True: print("B: {0}".format((x, y)))
                else: print("W: {0}".format((x, y)))
                self.score = self.gridsProcessing.getScore(self.occupiedGrids)
                self.updateStatus()
                self.prevPlay = (x, y)

    # AI下棋
    def moveByAI(self):
        pos = self.AI.predict(self.occupiedGrids)
        if self.nextColor is True: print("B: {0}".format(pos))
        else: print("W: {0}".format(pos))
        self.gridsProcessing.capture(self.occupiedGrids, pos, self.nextColor)
        self.score = self.gridsProcessing.getScore(self.occupiedGrids)
        self.updateStatus()
        self.prevPlay = pos

    def start(self, level, p1Color):
        print("\nNew Game\n")
        self.level = level
        self.nextPlayer = p1Color ^ True    # 下面的 updateStatus() 會更新一次，因此現在先 ^ True
        self.initOccupiedGrids()
        self.updateStatus()
        self.generateDisplayText()
        if level != 0:
            self.AI = AI(self.level + 1, self.nextPlayer ^ True)    # 若玩家先手，AI就後手
        while True:
            # AI下棋
            if level != 0 and self.nextPlayer is False and self.isOver is False:
                # 開始計時
                if self.timingOver is False:
                    self.startTime = time.time()
                    self.timingOver = True
                # 結束計時
                elif time.time() - self.startTime > 0.25:
                    self.timingOver = False
                    self.moveByAI()
            # 操作事件
            for event in pygame.event.get():
                # 離開
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # 滑鼠移動
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 580 and pos[0] < 758 and pos[1] > 500 and pos[1] < 557:
                        if self.isOver is False:
                            self.gbIndex = 1
                        else:
                            self.gbIndex = 3
                    else:
                        if self.isOver is False:
                            self.gbIndex = 0
                        else:
                            self.gbIndex = 2
                # 滑鼠點擊
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # 按鈕
                    if pos[0] > 580 and pos[0] < 758 and pos[1] > 500 and pos[1] < 557:
                        if self.isOver is False:
                            # Give up
                            return
                        else:
                            # Restart
                            self.__init__(self.display)
                            self.start(level, p1Color)
                            return
                    # 棋盤
                    if level == 0 or self.nextPlayer is True:
                        self.moveByPlayer(pos)
            # 顯示
            self.display.displayPageGame(self.gbIndex, self.occupiedGrids, self.nextPlayer, self.displayText, self.score, self.hints, self.prevPlay, self.isOver)
            pygame.display.update()
            self.clock.tick(60)
