from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLineEdit,
    QPushButton, QVBoxLayout, QDoubleSpinBox
)

class PropertyPanel(QWidget):
    def __init__(self, controller, model):
        super().__init__()
        self.controller = controller
        self.model = model
        
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.main_layout.addLayout(self.form_layout)
        
        # --- Buttons ---
        self.btn_add_child = QPushButton("Add Child")
        self.btn_delete = QPushButton("Delete Object")
        self.btn_duplicate = QPushButton("Duplicate Object")
        
        self.main_layout.addWidget(self.btn_add_child)
        self.main_layout.addWidget(self.btn_delete)
        self.main_layout.addWidget(self.btn_duplicate)
        
        # Connect signals
        self.btn_add_child.clicked.connect(self.on_add_child)
        self.btn_delete.clicked.connect(self.on_delete)
        self.btn_duplicate.clicked.connect(self.on_duplicate_node)
        
        self.fields = {}
        
        # Hide everything
        self.hide_all()
    
    def refresh(self):
        if self.model.node is None:
            self.clear()
            return
        
        # Don't show properties for root node
        if hasattr(self.controller, 'builder') and self.model.node == self.controller.builder.root_node:
            self.clear()
            return
        
        self.blockSignals(True)
        
        # Clear existing fields
        for field in self.fields.values():
            field.deleteLater()
        self.fields.clear()
        
        # Clear all rows from layout
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        print("refresh called")
        print("model: ", self.model)
        
        # Show buttons when selected
        self.show_all()
        
        for name, value in self.model.get_properties().items():
            edit = QLineEdit(str(value))
            edit.editingFinished.connect(
                lambda n=name, e=edit: self.on_edit(n, e)
            )
            self.form_layout.addRow(name, edit)
            self.fields[name] = edit
        
        self.blockSignals(False)
        self.setEnabled(True)
    
    def on_edit(self, name, edit):
        try:
            value = float(edit.text())
        except ValueError:
            return
        if self.model and self.model.node:
            self.controller.update_property(self.model.node, name, value)
    
    def on_add_child(self):
        if not self.model or not self.model.node:
            return
        self.controller.add_child(self.model.node)
    
    def on_delete(self):
        if not self.model or not self.model.node:
            return
        self.controller.delete_selected()
    
    def on_duplicate_node(self):
        if not self.model or not self.model.node:
            return
        self.controller.duplicate_node(self.model.node)
    
    def show_all(self):
        """Show buttons and enable form"""
        self.btn_add_child.show()
        self.btn_delete.show()
        self.btn_duplicate.show()
        self.setEnabled(True)
    
    def hide_all(self):
        """Hide buttons and disable form"""
        self.btn_add_child.hide()
        self.btn_delete.hide()
        self.btn_duplicate.hide()
        self.setEnabled(False)
    
    def clear(self):
        """Clear all property fields when nothing is selected"""
        # Clear existing fields
        for field in self.fields.values():
            field.deleteLater()
        self.fields.clear()
        
        # Clear all rows from layout
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Hide everything
        self.hide_all()