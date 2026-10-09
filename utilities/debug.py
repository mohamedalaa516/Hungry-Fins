import pygame_gui
import pygame



class DebugPanel:
    def __init__(self, game):
        self.flags={
            'show_colliders':False,
            'show_fps':False
        }
        self.game = game
        self.panel = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(30, 20, 300, 300),
            manager=self.game.ui_manager,
            window_display_title='Debug Panel',
            #     anchors={
            #     'centerx': 'centerx',
            #     'centery': 'centery'
            # }
        )
        #--page 1 contanier
        self.page1_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(10, 40, 280, 240),
            manager=self.game.ui_manager,
            container=self.panel,
            )

        self.flag_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 10, 100, 20),
            text='Flags',
            manager=self.game.ui_manager,
            container=self.page1_panel
        )
        self.monitor_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(120, 10, 100, 20),
            text='monitor',
            manager=self.game.ui_manager,
            container=self.page1_panel
        )
        #--page 2 contanier
        self.page2_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(10, 40, 280, 240),
            manager=self.game.ui_manager,
            container=self.panel,

            )
        self.collider_checkbox = pygame_gui.elements.UICheckBox(
            relative_rect=pygame.Rect(10, 40, 50, 20),
            text='show colliders',
            manager=self.game.ui_manager,
            container=self.page2_panel,
        )
        self.fps_checkbox = pygame_gui.elements.UICheckBox(
            relative_rect=pygame.Rect(10, 100, 50, 20),
            text='show fps',
            manager=self.game.ui_manager,
            container=self.page2_panel,
        )

        #page 3

        self.page3_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(10, 40, 280, 240),
            manager=self.game.ui_manager,
            container=self.panel,

            )
        self.darkness_input = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect(10, 10, 100, 30),
        manager=self.game.ui_manager,
        container=self.page3_panel,
    )

        self.red_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 50, 100, 30),
            manager=self.game.ui_manager,
            container=self.page3_panel
        )

        self.green_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 90, 100, 30),
            manager=self.game.ui_manager,
            container=self.page3_panel
        )

        self.blue_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(10, 130, 100, 30),
            manager=self.game.ui_manager,
            container=self.page3_panel,
        )
        self.darkness_input.set_text("1.05")
        self.red_input.set_text("1.02")
        self.green_input.set_text("0.98")
        self.blue_input.set_text("0.92")
        self.current_page=1
        self.page3_panel.hide()
        self.page2_panel.hide()
        self.show_panel=False


    def change_page(self,page):
        self.current_page=page
        if page==1:
            self.page1_panel.show()
            self.page2_panel.hide()
            self.page3_panel.hide()
        if page==2:
            self.page1_panel.hide()
            self.page2_panel.show()
        if page==3:
            self.page1_panel.hide()
            self.page3_panel.show()

    def update(self, event):
        if self.show_panel:
            self.panel.show()
            self.change_page(self.current_page)  # re-sync page visibility
        else:
            self.panel.hide()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.show_panel=True
            if event.key == pygame.K_ESCAPE:
                if self.current_page>1:
                    self.change_page(1)
                else:
                    self.show_panel= False


        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.flag_button:
                self.change_page(2)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element ==self.monitor_button:
                self.change_page(3)

        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == self.collider_checkbox:
                self.flags['show_colliders']=True
        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == self.fps_checkbox:
                self.flags['show_fps']=True

        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
          if event.ui_element == self.collider_checkbox:
              self.flags['show_colliders']=False
        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
          if event.ui_element == self.fps_checkbox:
              self.flags['show_fps']=False
            

