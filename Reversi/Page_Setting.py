import pygame

class Page_Setting:
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()
        self.cbIndex = 0
        self.abIndex1 = 0
        self.abIndex2 = 0
        self.sbIndex = 0
        self.level = 1
        self.p1Color = True

    def start(self):
        while True:
            # 操作事件
            for event in pygame.event.get():
                # 離開
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # 滑鼠移動
                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    # ArrowButtons 1
                    if pos[1] > 340 and pos[1] < 413:
                        if pos[0] > 90 and pos[0] < 163:
                            self.abIndex1 = 1
                        elif pos[0] > 365 and pos[0] < 438:
                            self.abIndex1 = 2
                        else:
                            self.abIndex1 = 0
                    else:
                        self.abIndex1 = 0
                    # ArrowButtons 2
                    if pos[1] > 460 and pos[1] < 533:
                        if pos[0] > 90 and pos[0] < 163:
                            self.abIndex2 = 1
                        elif pos[0] > 365 and pos[0] < 438:
                            self.abIndex2 = 2
                        else:
                            self.abIndex2 = 0
                    else:
                        self.abIndex2 = 0
                    # Play
                    if pos[0] > 485 and pos[0] < 750:
                        if pos[1] > 457 and pos[1] < 534:
                            self.sbIndex = 1
                        else:
                            self.sbIndex = 0
                    else:
                        self.sbIndex = 0
                # 滑鼠點擊
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # Checkbox
                    if pos[0] > 100 and pos[0] < 168:
                        if pos[1] > 50 and pos[1] < 118:
                            self.cbIndex = 0
                        elif pos[1] > 200 and pos[1] < 268:
                            self.cbIndex = 1
                    # ArrowButtons 1
                    if self.cbIndex == 0 and pos[1] > 340 and pos[1] < 413:
                        if pos[0] > 90 and pos[0] < 163 and self.level > 1:
                            self.level -= 1
                        elif pos[0] > 365 and pos[0] < 438 and self.level < 5:
                            self.level += 1
                    # ArrowButtons 2
                    if pos[1] > 460 and pos[1] < 533:
                        if pos[0] > 90 and pos[0] < 163:
                            self.p1Color = True
                        elif pos[0] > 365 and pos[0] < 438:
                            self.p1Color = False
                    # Play
                    if pos[0] > 485 and pos[0] < 750:
                        if pos[1] > 457 and pos[1] < 534:
                            if self.cbIndex == 1:
                                self.level = 0      # 1P vs 2P
                            return self.level, self.p1Color
            # 顯示
            self.display.displayPageSetting(self.cbIndex, self.abIndex1, self.abIndex2, self.sbIndex, self.level, self.p1Color)
            pygame.display.update()
            self.clock.tick(60)
