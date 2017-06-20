import pygame

class Page_Menu:
    def __init__(self, display):
        self.display = display
        self.clock = pygame.time.Clock()
        self.mbIndex = 0

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
                    if pos[0] > 400 and pos[0] < 665:
                        if pos[1] > 300 and pos[1] < 377:
                            self.mbIndex = 1
                        elif pos[1] > 413 and pos[1] < 490:
                            self.mbIndex = 2
                        else:
                            self.mbIndex = 0
                    else:
                        self.mbIndex = 0
                # 滑鼠點擊
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[0] > 400 and pos[0] < 665:
                        if pos[1] > 300 and pos[1] < 377:
                            return self.mbIndex 
                        elif pos[1] > 413 and pos[1] < 490:
                            return self.mbIndex 
            # 顯示
            self.display.displayPageMenu(self.mbIndex)
            pygame.display.update()
            self.clock.tick(60)
