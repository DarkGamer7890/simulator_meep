from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit

class PropertyPanel(QWidget):
    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model = model
        self.layout = QFormLayout(self)
        self.fields = {}
        
    def refresh(self):
        if self.model is None:
            return
        
        # Clear existing fields
        for field in self.fields.values():
            field.deleteLater()
        self.fields.clear()
        
        # Clear all rows from layout
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        print("refresh called")
        print("model: ", self.model)
        

        if not self.model.node:
            return
        
        
        for name, value in self.model.get_properties().items():
            edit = QLineEdit(str(value))
            
            edit.editingFinished.connect(
                lambda n=name, e=edit: self.on_edit(n, e)
            )
            self.layout.addRow(name, edit)
            self.fields[name] = edit
    
    def on_edit(self, name, edit):
        try:
            value = float(edit.text())
        except ValueError:
            return
        
        if self.model and self.model.node:
            self.controller.update_property(self.model.node, name, value)