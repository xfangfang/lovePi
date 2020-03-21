from activity.activity import Activity
from activity.cat import CatGame
from var import *



class MainActivity(Activity):
    def __init__(self, app):
        Activity.__init__(self, app)

    def update(self):
        self.surf.fill(RED)

    def onKeyDown(self, key, e):
        self.app.openActivity(CatGame)
