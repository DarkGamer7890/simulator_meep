import wx

class RedirectText:
    def __init__(self, text_ctrl):
        self.out = text_ctrl

    def write(self, string):
        wx.CallAfter(self.out.AppendText, string)

    def flush(self):  # Needed for compatibility
        pass