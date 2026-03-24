- check CADNode's to_geometry function (Done will be changed according to need)

- change to_plot of CADBlock and CADPrism to add parameters like e1, e2, sideangle if needed

- remove 'w' and 's' callback in pyvista

- see if drag to select object can be changed to click

- .rebuild() clear all geometries and rebuilds -> find a way to rebuild only selected node

- has to press x,y,z,a,b,c 2 times to move an object

- when gui is finished, work to rebuild only selected nodes

- rotation not working + keyboard movements not refreshes panel (done)

- add undo/redo

- hierarchy panel is not selecting nodes on viewer (Done)

- translation depends on the object's local rotation and not on world axes  (Done but need to be checked)

# simulation 
- Replace blocking multiprocessing call with:
  - QTimer polling OR
  - multiprocessing + signals

- Add progress reporting

- Add cancel button

- On moving object with x,y,z,a,b,c update property panel also

- On moving parent, child should remain at same place like before and not move with same step size