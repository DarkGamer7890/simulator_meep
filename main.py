import wx
from gui import MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()