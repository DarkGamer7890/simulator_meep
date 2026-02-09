from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel
from PyQt5.QtCore import Qt


class HierarchyPanel(QWidget):
    def __init__(self, controller, viewer):
        super().__init__()
        self.controller = controller
        self.viewer = viewer
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Hierarchy"))
        
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree)
        
        self.tree.itemClicked.connect(self.on_item_clicked)
    


    def rebuild(self):
        """Rebuild tree from CAD scene"""
        self.tree.clear()
        root = self.controller.builder.root_node
        root_item = self._add_node_recursive(root, None)
        self.tree.expandAll()
    


    def _add_node_recursive(self, node, parent_item):
        item = QTreeWidgetItem([node.name])
        item.setData(0, Qt.UserRole, node)

        # Make root node non-selectable
        if parent_item is None:  # This is the root
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            item.setForeground(0, Qt.gray)  # Visual indicator
        
        if parent_item is None:
            self.tree.addTopLevelItem(item)
        else:
            parent_item.addChild(item)
        
        for child in node.children:
            self._add_node_recursive(child, item)
        
        return item
    


    def on_item_clicked(self, item, column):
        """Handle user clicking on tree item"""
        node = item.data(0, Qt.UserRole)
        if node:
            self.controller.on_node_selected(node, source="hierarchy")
    

    
    def select_node(self, node):
        """Programmatically select a node in the tree. NO callbacks."""
        # Block signals to prevent triggering on_item_clicked
        self.tree.blockSignals(True)
        
        if node is None:
            self.tree.clearSelection()
        else:
            self._select_node_recursive(node)
        
        # Restore signals
        self.tree.blockSignals(False)
    
    def _select_node_recursive(self, node):
        """Recursively search for and select a node"""
        def recurse(item):
            if item.data(0, Qt.UserRole) is node:
                self.tree.setCurrentItem(item)
                self.tree.scrollToItem(item)  # Ensure it's visible
                return True
            
            for i in range(item.childCount()):
                if recurse(item.child(i)):
                    return True
            
            return False
        
        # Search through all top-level items
        for i in range(self.tree.topLevelItemCount()):
            if recurse(self.tree.topLevelItem(i)):
                return