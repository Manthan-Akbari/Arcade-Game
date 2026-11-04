from ui.home_screen import HomeScreen

class Navigation:

    def __init__(self,app):

        self.app=app
        self.current_sceen= HomeScreen(self)

    def handle_event(self,event):

        self.current_screen.handle_event(event)

    def update(self):

        self.current_screen.update()

    def draw(self,screen):

        self.current_screen.draw(screen)

    def change_screen(self,new_screen):

        self.current_screen= new_screen