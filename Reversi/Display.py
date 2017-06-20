import pygame, time

class Display:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Reversi")
        self.background = pygame.image.load("Pictures/Background.bmp")
        self.menuButtons = [pygame.image.load("Pictures/Menu_Buttons0.png"), pygame.image.load("Pictures/Menu_Buttons1.png"), pygame.image.load("Pictures/Menu_Buttons2.png")]
        self.checkbox = [pygame.image.load("Pictures/Checkbox0.png"), pygame.image.load("Pictures/Checkbox1.png")]
        self.arrowButtons = [pygame.image.load("Pictures/ArrowButtons0.png"), pygame.image.load("Pictures/ArrowButtons1.png"), pygame.image.load("Pictures/ArrowButtons2.png")]
        self.settingButtons = [pygame.image.load("Pictures/Setting_Buttons0.png"), pygame.image.load("Pictures/Setting_Buttons1.png")]
        self.gameButtons = [pygame.image.load("Pictures/Game_Buttons0.png"), pygame.image.load("Pictures/Game_Buttons1.png"), pygame.image.load("Pictures/Game_Buttons2.png"), pygame.image.load("Pictures/Game_Buttons3.png")]

    def displayPageMenu(self, mbIndex):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.menuButtons[mbIndex], (400, 300))
        self.displayText("Reversi", x=50, y=50, size=120)
        self.displayText("Yu Sheng", x=20, y=550, size=30)

    def displayPageSetting(self, cbIndex, abIndex1, abIndex2, sbIndex, level, p1Color):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.checkbox[cbIndex], (100, 50))
        self.screen.blit(self.settingButtons[sbIndex], (485, 457))
        self.displayText("Player vs. AI", x=200, y=60, size=60)
        self.displayText("Player vs. Player", x=200, y=210, size=60)
        # Level
        if cbIndex == 0:
            self.screen.blit(self.arrowButtons[abIndex1], (90, 340))
            self.displayText("Lv. {0}".format(level), x=200, y=345, size=60)
        # P1顏色
        self.screen.blit(self.arrowButtons[abIndex2], (90, 460))
        self.displayText("P1:", x=200, y=465, size=60)
        if p1Color is True:
            pygame.draw.circle(self.screen, (0, 0, 0), (325, 492), 25, 0)
        else:
            pygame.draw.circle(self.screen, (255, 255, 255), (325, 492), 25, 0)

    def displayPageGame(self, gbIndex, occupiedGrids, nextPlayer, displayText, score, hints, prevPlay, isOver):
        self.screen.blit(self.background, (0, 0))
        # 按鈕
        self.screen.blit(self.gameButtons[gbIndex], (580, 500))
        # 棋盤
        pygame.draw.rect(self.screen, (0, 150, 0), (60, 60, 480, 480), 0)
        for i in range(1, 10):
            pygame.draw.line(self.screen, (0, 0, 0), (60, i * 60), (540, i * 60), 5)
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 60), (i * 60, 540), 5)
        # 數字
        for i in range(0, 8):
            self.displayText(str(i), x=80+i*60, y=20, size=30)
            self.displayText(str(i), x=20, y=80+i*60, size=30)
        # 棋子
        for pos, status in occupiedGrids.items():
            if status is True:
                pygame.draw.circle(self.screen, (0, 0, 0), (90 + pos[0] * 60, 90 + pos[1] * 60), 25, 0)
            else:
                pygame.draw.circle(self.screen, (255, 255, 255), (90 + pos[0] * 60, 90 + pos[1] * 60), 25, 0)
            pass
        # 訊息欄
        if nextPlayer is True:
            pygame.draw.rect(self.screen, (0, 0, 255), (575, 80, 190, 140), 5)
        else:
            pygame.draw.rect(self.screen, (0, 0, 255), (575, 230, 190, 140), 5)
        self.displayText(displayText[0], x=600, y=100, size=30)
        self.displayText(displayText[1], x=600, y=250, size=30)
        if displayText[2] is True:  # player 1 is black
            self.displayText("x{0}".format(score[0]), x=660, y=155, size=30)
            self.displayText("x{0}".format(score[1]), x=660, y=305, size=30)
            pygame.draw.circle(self.screen, (0, 0, 0), (620, 170), 25, 0)
            pygame.draw.circle(self.screen, (255, 255, 255), (620, 320), 25, 0)
        else:   # player 1 is white
            self.displayText("x{0}".format(score[1]), x=660, y=155, size=30)
            self.displayText("x{0}".format(score[0]), x=660, y=305, size=30)
            pygame.draw.circle(self.screen, (255, 255, 255), (620, 170), 25, 0)
            pygame.draw.circle(self.screen, (0, 0, 0), (620, 320), 25, 0)
        # 提示點
        for h in hints:
            pygame.draw.circle(self.screen, (0, 0, 255), (90 + h[0] * 60, 90 + h[1] * 60), 5, 0)
        # 上次的落子
        if prevPlay is not None:
            pygame.draw.rect(self.screen, (0, 0, 255), (60 + prevPlay[0] * 60, 60 + prevPlay[1] * 60, 60, 60), 5)
        # 勝負
        if isOver is True:
            if score[0] == score[1]:
                self.displayText("Draw!!", x=620, y=420, size=30, color=(255, 0, 0))
            elif score[0] > score[1] and displayText[2] is True or score[0] < score[1] and displayText[2] is False:
                self.displayText("{0} Win!!".format(displayText[0]), x=570, y=420, size=30, color=(255, 0, 0))
            else:
                self.displayText("{0} Win!!".format(displayText[1]), x=570, y=420, size=30, color=(255, 0, 0))
            
    def displayText(self, text:str, x:int, y:int, size:int, color:tuple=(0, 0, 0), bold:bool=False, italic:bool=False):
        font = pygame.font.Font("Fonts/freesansbold.ttf", size)
        font.set_bold(bold)
        font.set_italic(italic)
        textSurf = font.render(text, True, color)
        textRect = textSurf.get_rect()
        textRect.x = x
        textRect.y = y
        self.screen.blit(textSurf, textRect)
