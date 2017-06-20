import pygame
from Display import Display
from Page_Menu import Page_Menu
from Page_Setting import Page_Setting
from Page_Game import Page_Game

pygame.init()
pygame.mixer.init()

class main:
    def __init__(self):
        self.display = Display()
        self.pageMenu = None
        self.pageSetting = None
        self.pageGame = None
        self.mbIndex = 0
        self.level = 0
        self.p1Color = True
        self.start()

    def start(self):
        while True:
            if self.mbIndex == 0:
                self.pageMenu = Page_Menu(self.display)         # 主畫面
                self.mbIndex = self.pageMenu.start()
            if self.mbIndex == 1:
                self.pageSetting = Page_Setting(self.display)   # 設置畫面
                self.level, self.p1Color = self.pageSetting.start()
                self.pageGame = Page_Game(self.display)         # 遊戲畫面
                self.pageGame.start(self.level, self.p1Color)
                self.mbIndex = 0
            elif self.mbIndex == 2:
                break   # 離開
        pygame.quit()
        quit()

if __name__ == '__main__':
    main()