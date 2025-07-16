import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import sys
import meep as mp

from importer import importer
from sim_in_meep import sim_in_meep
from plotter import plotter
from redirect_text import RedirectText



class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Trial", size=(600, 600))

        # #=========== Menu ===========#
        # menubar = wx.MenuBar()

        # # File Menu
        # file_menu = wx.Menu()

        # # Open file option
        # open_file = file_menu.Append(wx.ID_OPEN, "Open File")
        
        # # appending and setting
        # menubar.Append(file_menu, '&File')
        # self.Bind(wx.EVT_MENU, self.on_open_file, open_file)
        # self.SetMenuBar(menubar)


        # === Panel ==== #                                                                                               
        self.panel = wx.Panel(self)



        #====== Left Panel =====#
        self.left_panel = wx.ScrolledWindow(self.panel, style=wx.VSCROLL)
        self.left_panel.SetScrollRate(5, 11)
        
        self.left_sizer = wx.BoxSizer(wx.HORIZONTAL)


        #=== Grid Layout ===#

        # == Cell == #

        # Size

        cell_size_label = wx.StaticText(self.left_panel, label="Cell Size:")
        cell_x_label = wx.StaticText(self.left_panel, label='X:')
        cell_y_label = wx.StaticText(self.left_panel, label='Y:')
        cell_z_label = wx.StaticText(self.left_panel, label='Z:')

        dim_X1 = wx.StaticText(self.left_panel, label='×')
        dim_X2 = wx.StaticText(self.left_panel, label='×')


        self.cell_x_input = wx.TextCtrl(self.left_panel, size=(100, -1))
        self.cell_y_input = wx.TextCtrl(self.left_panel, size=(100, -1))
        self.cell_z_input = wx.TextCtrl(self.left_panel, size=(100, -1))

        # Horizontal Layout for x, y, z
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(cell_size_label, 0, wx.RIGHT, 10)

        hbox1.Add(cell_x_label, 0, wx.RIGHT, 10)
        hbox1.Add(self.cell_x_input, 0, wx.RIGHT, 15)

        hbox1.Add(dim_X1, 0, wx.RIGHT, 5)

        hbox1.Add(cell_y_label, 0, wx.RIGHT, 10)
        hbox1.Add(self.cell_y_input, 0, wx.RIGHT, 15)

        hbox1.Add(dim_X2, 0, wx.RIGHT, 5)

        hbox1.Add(cell_z_label, 0, wx.RIGHT, 10)
        hbox1.Add(self.cell_z_input, 0, wx.RIGHT, 15)



        # PML

        pml_label = wx.StaticText(self.left_panel, label='PML Layer: ')
        self.pml_input = wx.TextCtrl(self.left_panel, size=(600, -1))


        # == Source == #

        # Size

        source_size_label = wx.StaticText(self.left_panel, label="Source Size:")
        source_length_label = wx.StaticText(self.left_panel, label='Length (x-axis):')
        source_width_label = wx.StaticText(self.left_panel, label='Width (y-axis):')
        source_height_label = wx.StaticText(self.left_panel, label='Height (z-axis):')

        dim_X3 = wx.StaticText(self.left_panel, label='×')
        dim_X4 = wx.StaticText(self.left_panel, label='×')


        self.source_length_input = wx.TextCtrl(self.left_panel, size=(100, -1))
        self.source_width_input = wx.TextCtrl(self.left_panel, size=(100, -1))
        self.source_height_input = wx.TextCtrl(self.left_panel, size=(100, -1))

        # Horizontal Layout for l, b, h

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox2.Add(source_size_label, 0, wx.RIGHT, 10)
        hbox2.Add(source_length_label, 0, wx.RIGHT, 10)
        hbox2.Add(self.source_length_input, 0, wx.RIGHT, 15)

        hbox2.Add(dim_X3, 0, wx.RIGHT, 5)

        hbox2.Add(source_width_label, 0, wx.RIGHT, 10)
        hbox2.Add(self.source_width_input, 0, wx.RIGHT, 15)

        hbox2.Add(dim_X4, 0, wx.RIGHT, 5)

        hbox2.Add(source_height_label, 0, wx.RIGHT, 10)
        hbox2.Add(self.source_height_input, 0, wx.RIGHT, 15)


        # Location

        source_center_label = wx.StaticText(self.left_panel, label="Source Center:")
        source_x_label = wx.StaticText(self.left_panel, label='X:')
        source_y_label = wx.StaticText(self.left_panel, label='Y:')
        source_z_label = wx.StaticText(self.left_panel, label='Z:')

        dim_X5 = wx.StaticText(self.left_panel, label='×')
        dim_X6 = wx.StaticText(self.left_panel, label='×')


        self.source_x_input = wx.TextCtrl(self.left_panel, size=(100, -1))
        self.source_y_input = wx.TextCtrl(self.left_panel, size=(100, -1))
        self.source_z_input = wx.TextCtrl(self.left_panel, size=(100, -1))


        # Horizontal Layout for x, y, z

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        hbox3.Add(source_center_label, 0, wx.RIGHT, 10)
        hbox3.Add(source_x_label, 0, wx.RIGHT, 10)
        hbox3.Add(self.source_x_input, 0, wx.RIGHT, 15)

        hbox3.Add(dim_X5, 0, wx.RIGHT, 5)

        hbox3.Add(source_y_label, 0, wx.RIGHT, 10)
        hbox3.Add(self.source_y_input, 0, wx.RIGHT, 15)

        hbox3.Add(dim_X6, 0, wx.RIGHT, 5)

        hbox3.Add(source_z_label, 0, wx.RIGHT, 10)
        hbox3.Add(self.source_z_input, 0, wx.RIGHT, 15)


        # Frequency

        frequency_label = wx.StaticText(self.left_panel, label='Frequency:')
        self.frequency_input = wx.TextCtrl(self.left_panel, size=(600, -1))


        # Resolution

        resolution_label = wx.StaticText(self.left_panel, label='Resoution:')
        self.resolution_input = wx.TextCtrl(self.left_panel, size=(600, -1))
        


        #====== Geometry =======#

        geometry_label = wx.StaticText(self.left_panel, label = 'Geometry:')
        self.geometry_input = wx.StaticText(self.left_panel, label="", size=(550, -1))

        epsilon_label = wx.StaticText(self.left_panel, label = 'Epsilon:')
        self.epsilon_input = wx.TextCtrl(self.left_panel, size=(600, -1))

        pitch_label = wx.StaticText(self.left_panel, label='Pitch:')
        self.pitch_input = wx.TextCtrl(self.left_panel, size=(600, -1))



        # Load Button
        load_button = wx.Button(self.left_panel, label='Load Geometry')
        load_button.Bind(wx.EVT_BUTTON, self.on_open_file)



        # Hbox for loading geometry
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)

        hbox4.Add(geometry_label, 0, wx.RIGHT, 10)
        hbox4.Add(self.geometry_input, 0, wx.RIGHT, 15)     
        hbox4.Add(load_button, 0, wx.RIGHT, 15)   


        # ==== Simulation ====#
        time_label = wx.StaticText(self.left_panel, label='Time:')
        self.time_input = wx.TextCtrl(self.left_panel, size=(600, -1))


        
        
        #====== Buttons ======#
        # show_button = wx.Button(self.left_panel, label='Show')
        # show_button.Bind(wx.EVT_BUTTON, self.on_show)

        run_sim_button = wx.Button(self.left_panel, label='Run Simulation')
        run_sim_button.Bind(wx.EVT_BUTTON, self.run_sim)

        btn_row1 = wx.BoxSizer(wx.HORIZONTAL)
        # btn_row1.Add(show_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)  
        btn_row1.Add(run_sim_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)  



        # Line Graph buttons

        line_x_origin_button = wx.Button(self.left_panel, label='X-axis (origin)')
        line_x_origin_button.Bind(wx.EVT_BUTTON, self.line_x_origin)

        line_x_focus_button = wx.Button(self.left_panel, label='X-axis (focus)')
        line_x_focus_button.Bind(wx.EVT_BUTTON, self.line_x_focus)

        line_y_origin_button = wx.Button(self.left_panel, label='Y-axis (origin)')
        line_y_origin_button.Bind(wx.EVT_BUTTON, self.line_y_origin)

        line_y_focus_button = wx.Button(self.left_panel, label='Y-axis (focus)')
        line_y_focus_button.Bind(wx.EVT_BUTTON, self.line_y_focus)

        line_z_origin_button = wx.Button(self.left_panel, label='Z-axis (origin)')
        line_z_origin_button.Bind(wx.EVT_BUTTON, self.line_z_origin)

        line_z_focus_button = wx.Button(self.left_panel, label='Z-axis (focus)')
        line_z_focus_button.Bind(wx.EVT_BUTTON, self.line_z_focus)

        
        btn_row2 = wx.BoxSizer(wx.HORIZONTAL)
        btn_row3 = wx.BoxSizer(wx.HORIZONTAL)

        btn_row2.Add(line_x_origin_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row2.Add(line_x_focus_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row2.Add(line_y_origin_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row2.Add(line_y_focus_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row3.Add(line_z_origin_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row3.Add(line_z_focus_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)


        # Mag Plane Graph Buttons

        mag_plane_origin_xy_button = wx.Button(self.left_panel, label='XY Plane (origin)')
        mag_plane_origin_xy_button.Bind(wx.EVT_BUTTON, self.mag_origin_xy)

        mag_plane_focus_xy_button = wx.Button(self.left_panel, label='XY Plane (focus)')
        mag_plane_focus_xy_button.Bind(wx.EVT_BUTTON, self.mag_focus_xy)

        mag_plane_origin_yz_button = wx.Button(self.left_panel, label='YZ Plane (origin)')
        mag_plane_origin_yz_button.Bind(wx.EVT_BUTTON, self.mag_origin_yz)

        mag_plane_focus_yz_button = wx.Button(self.left_panel, label='YZ Plane (focus)')
        mag_plane_focus_yz_button.Bind(wx.EVT_BUTTON, self.mag_focus_yz)

        mag_plane_origin_xz_button = wx.Button(self.left_panel, label='XZ Plane (origin)')
        mag_plane_origin_xz_button.Bind(wx.EVT_BUTTON, self.mag_origin_xz)

        mag_plane_focus_xz_button = wx.Button(self.left_panel, label='XZ Plane (focus)')
        mag_plane_focus_xz_button.Bind(wx.EVT_BUTTON, self.mag_focus_xz)



        btn_row4 = wx.BoxSizer(wx.HORIZONTAL)
        btn_row5 = wx.BoxSizer(wx.HORIZONTAL)

        btn_row4.Add(mag_plane_origin_xy_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row4.Add(mag_plane_focus_xy_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row4.Add(mag_plane_origin_yz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row4.Add(mag_plane_focus_yz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row5.Add(mag_plane_origin_xz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row5.Add(mag_plane_focus_xz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)



        # Phase Plane Graph Buttons

        phase_plane_origin_xy_button = wx.Button(self.left_panel, label='XY Plane (origin)')
        phase_plane_origin_xy_button.Bind(wx.EVT_BUTTON, self.phase_origin_xy)

        phase_plane_focus_xy_button = wx.Button(self.left_panel, label='XY Plane (focus)')
        phase_plane_focus_xy_button.Bind(wx.EVT_BUTTON, self.phase_focus_xy)

        phase_plane_origin_yz_button = wx.Button(self.left_panel, label='YZ Plane (origin)')
        phase_plane_origin_yz_button.Bind(wx.EVT_BUTTON, self.phase_origin_yz)

        phase_plane_focus_yz_button = wx.Button(self.left_panel, label='YZ Plane (focus)')
        phase_plane_focus_yz_button.Bind(wx.EVT_BUTTON, self.phase_focus_yz)

        phase_plane_origin_xz_button = wx.Button(self.left_panel, label='XZ Plane (origin)')
        phase_plane_origin_xz_button.Bind(wx.EVT_BUTTON, self.phase_origin_xz)

        phase_plane_focus_xz_button = wx.Button(self.left_panel, label='XZ Plane (focus)')
        phase_plane_focus_xz_button.Bind(wx.EVT_BUTTON, self.phase_focus_xz)



        btn_row6 = wx.BoxSizer(wx.HORIZONTAL)
        btn_row7 = wx.BoxSizer(wx.HORIZONTAL)

        btn_row6.Add(phase_plane_origin_xy_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row6.Add(phase_plane_focus_xy_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row6.Add(phase_plane_origin_yz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row6.Add(phase_plane_focus_yz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row7.Add(phase_plane_origin_xz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row7.Add(phase_plane_focus_xz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)




        # Contour Plots

        contour_origin_xy_button = wx.Button(self.left_panel, label='XY Plane (origin)')
        contour_origin_xy_button.Bind(wx.EVT_BUTTON, self.contour_origin_xy)

        contour_focus_xy_button = wx.Button(self.left_panel, label='XY Plane (focus)')
        contour_focus_xy_button.Bind(wx.EVT_BUTTON, self.contour_focus_xy)

        contour_origin_yz_button = wx.Button(self.left_panel, label='YZ Plane (origin)')
        contour_origin_yz_button.Bind(wx.EVT_BUTTON, self.contour_origin_yz)

        contour_focus_yz_button = wx.Button(self.left_panel, label='YZ Plane (focus)')
        contour_focus_yz_button.Bind(wx.EVT_BUTTON, self.contour_focus_yz)

        contour_origin_xz_button = wx.Button(self.left_panel, label='XZ Plane (origin)')
        contour_origin_xz_button.Bind(wx.EVT_BUTTON, self.contour_origin_xz)

        contour_focus_xz_button = wx.Button(self.left_panel, label='XZ Plane (focus)')
        contour_focus_xz_button.Bind(wx.EVT_BUTTON, self.contour_focus_xz)




        btn_row8 = wx.BoxSizer(wx.HORIZONTAL)
        btn_row9 = wx.BoxSizer(wx.HORIZONTAL)

        btn_row8.Add(contour_origin_xy_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row8.Add(contour_focus_xy_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row8.Add(contour_origin_yz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row8.Add(contour_focus_yz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row9.Add(contour_origin_xz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)
        btn_row9.Add(contour_focus_xz_button, 0, wx.ALIGN_BOTTOM | wx.RIGHT, 10)



        # Adding to Grid

        grid = wx.GridBagSizer(vgap=10, hgap=10)

        grid.Add(wx.StaticText(self.left_panel, label="Cell Parameters"), pos=(0, 0), span=(1, 2))
        grid.Add(hbox1, pos=(1, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(pml_label, pos=(2, 0), span=(1, 1), flag=wx.ALL, border=5)
        grid.Add(self.pml_input, pos=(2, 1), span=(1, 1), flag=wx.ALL, border=5)

        grid.Add(wx.StaticText(self.left_panel, label="Source Parameters"), pos=(3, 0), span=(1, 2))
        grid.Add(hbox2, pos=(4, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(hbox3, pos=(5, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(frequency_label, pos=(6, 0), span=(1, 1), flag=wx.ALL, border=5)
        grid.Add(self.frequency_input, pos=(6, 1), span=(1, 1), flag=wx.ALL, border=5)

        grid.Add(resolution_label, pos=(7, 0), span=(1, 1), flag=wx.ALL, border=5)
        grid.Add(self.resolution_input, pos=(7, 1), span=(1, 1), flag=wx.ALL, border=5)  

        grid.Add(hbox4, pos=(8, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5) 

        grid.Add(epsilon_label, pos=(9, 0), span=(1, 1), flag=wx.ALL, border=5)
        grid.Add(self.epsilon_input, pos=(9, 1), span=(1, 1), flag=wx.ALL, border=5) 

        grid.Add(pitch_label, pos=(10, 0), span=(1, 1), flag=wx.ALL, border=5)
        grid.Add(self.pitch_input, pos=(10, 1), span=(1, 1), flag=wx.ALL, border=5)  

        grid.Add(time_label, pos=(11, 0), span=(1, 1), flag=wx.ALL, border=5)
        grid.Add(self.time_input, pos=(11, 1), span=(1, 1), flag=wx.ALL, border=5)      

        grid.Add(btn_row1, pos=(12, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(wx.StaticText(self.left_panel, label='Line Graphs:'), pos=(13, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row2, pos=(14, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row3, pos=(15, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(wx.StaticText(self.left_panel, label='Plane Magnitude Graphs:'), pos=(16, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row4, pos=(17, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row5, pos=(18, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(wx.StaticText(self.left_panel, label='Plane Phase Graphs:'), pos=(19, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row6, pos=(20, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row7, pos=(21, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)

        grid.Add(wx.StaticText(self.left_panel, label='Contour Plots:'), pos=(22, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row8, pos=(23, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)
        grid.Add(btn_row9, pos=(24, 0), span=(1, 2), flag=wx.EXPAND | wx.ALL, border=5)



        # ========== Setting Left Panel =========== #

        self.left_sizer.Add(grid, 0, wx.EXPAND | wx.ALL, 15)

        self.left_panel.SetSizer(self.left_sizer)
        self.left_panel.FitInside()  # important 
        self.left_panel.SetMinSize((820, -1)) # Minimum size



        # ======== Right Panel ========= #

        # Terminal 
        
        self.right_panel = wx.Panel(self.panel)
        self.right_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.output_console = wx.TextCtrl(self.right_panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.right_sizer.Add(self.output_console, 1, wx.EXPAND | wx.ALL, 5)


        # Matplotlib Plot (initially hidden)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.right_panel, -1, self.figure)
        self.canvas.Hide()  # initially hidden
        self.right_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)



        self.right_panel.SetSizer(self.right_sizer)

        redir = RedirectText(self.output_console)
        sys.stdout = redir
        sys.stderr = redir

        self.Centre()



        # === MAIN LAYOUT ===
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.left_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.main_sizer.Add(self.right_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(self.main_sizer)


        self.Show()
        




    def on_open_file(self, event):

        # Open file dialog
        dialog = wx.FileDialog(self, message="Choose a file", wildcard="All files (*.*)|*.*")
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath() 
            self.geometry_input.SetLabel(f"{self.path}")


        dialog.Destroy()


    # def on_show(self, event):
    #     x = self.cell_x_input.GetValue()
    #     y = self.cell_y_input.GetValue()
    #     z = self.cell_z_input.GetValue()

    #     print('X: ' + x + ' Y: ' + y + ' Z: ' + z)


    def run_sim(self, event):

        self.output_console.Show()
        self.canvas.Hide()
        self.right_panel.Layout()


        cell_x = float(self.cell_x_input.GetValue())
        cell_y = float(self.cell_y_input.GetValue())
        cell_z = float(self.cell_z_input.GetValue())

        source_length = float(self.source_length_input.GetValue())
        source_width = float(self.source_width_input.GetValue())
        source_height = float(self.source_height_input.GetValue())

        source_x = float(self.source_x_input.GetValue())
        source_y = float(self.source_y_input.GetValue())
        source_z = float(self.source_z_input.GetValue())

        cell_size = mp.Vector3(cell_x, cell_y, cell_z)
        source_center = mp.Vector3(source_length, source_width, source_height)
        source_size = mp.Vector3(source_x, source_y, source_z)

        resolution = float(self.resolution_input.GetValue())
        pml = float(self.pml_input.GetValue())
        frequency = float(self.frequency_input.GetValue())
        epsilon = float(self.epsilon_input.GetValue())
        pitch = float(self.pitch_input.GetValue())
        time = float(self.time_input.GetValue())


        external_geometry = importer(self.path, pitch)
        filled_vox = external_geometry.voxalization()
        sim = sim_in_meep(cell_size, resolution, pml, source_center, source_size, frequency, filled_vox, epsilon, pitch, time)

        self.eps_sim, self.ez_dft = sim.sim_run()

        self.plotter = plotter(self.eps_sim, self.ez_dft, self.figure, self.canvas, self.ax, pml, resolution)

        print(len(self.eps_sim))
        print(len(self.ez_dft))



    def line_x_origin(self, event):
        
        self.plotter.line_graph_origin_x()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()

    

    def line_x_focus(self, event):
        
        self.plotter.line_graph_focus_x()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()

    

    def line_y_origin(self, event):
        
        self.plotter.line_graph_origin_y()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()

    

    def line_y_focus(self, event):
        
        self.plotter.line_graph_focus_y()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()

    
    def line_z_origin(self, event):
        
        self.plotter.line_graph_origin_z()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def line_z_focus(self, event):
        
        self.plotter.line_graph_focus_z()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()

    
    def mag_origin_xy(self, event):
        
        self.plotter.mag_plane_origin_xy()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def mag_focus_xy(self, event):
        
        self.plotter.mag_plane_focus_xy()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def mag_origin_yz(self, event):
        
        self.plotter.mag_plane_origin_yz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def mag_focus_yz(self, event):
        
        self.plotter.mag_plane_focus_yz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def mag_origin_xz(self, event):
        
        self.plotter.mag_plane_origin_xz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def mag_focus_xz(self, event):
        
        self.plotter.mag_plane_focus_xz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def phase_origin_xy(self, event):
        
        self.plotter.phase_plane_origin_xy()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def phase_focus_xy(self, event):
        
        self.plotter.phase_plane_focus_xy()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def phase_origin_yz(self, event):
        
        self.plotter.phase_plane_origin_yz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def phase_focus_yz(self, event):
        
        self.plotter.phase_plane_focus_yz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def phase_origin_xz(self, event):
        
        self.plotter.phase_plane_origin_xz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def phase_focus_xz(self, event):
        
        self.plotter.phase_plane_focus_xz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def contour_origin_xy(self, event):
        
        self.plotter.contour_origin_xy()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def contour_focus_xy(self, event):
        
        self.plotter.contour_focus_xy()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def contour_origin_yz(self, event):
        
        self.plotter.contour_origin_yz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def contour_focus_yz(self, event):
        
        self.plotter.contour_focus_yz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def contour_origin_xz(self, event):
        
        self.plotter.contour_origin_xz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()


    def contour_focus_xz(self, event):
        
        self.plotter.contour_focus_xz()  # call Plotter method

        # Swap views
        self.output_console.Hide()
        self.canvas.Show()
        self.right_panel.Layout()