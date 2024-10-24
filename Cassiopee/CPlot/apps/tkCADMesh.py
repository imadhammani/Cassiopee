# - generate surface mesh of CAD -
try: import tkinter as TK
except: import Tkinter as TK
import CPlot.Ttk as TTK
import Converter.PyTree as C
import CPlot.PyTree as CPlot
import CPlot.Tk as CTK
import Converter.Internal as Internal

# local widgets list
WIDGETS = {}; VARS = []
    
#==============================================================================
def meshCADEdges(event=None):
    if CTK.CADHOOK is None: return
    if CTK.t == []: return
    import OCC.PyTree as OCC
    hmax = CTK.varsFromWidget(VARS[0].get(), 1)[0]
    hausd = CTK.varsFromWidget(VARS[1].get(), 1)[0]
    OCC._meshAllEdges(CTK.CADHOOK, CTK.t, hmax=hmax, hausd=hausd)
    CTK.TXT.insert('START', 'All CAD edges remeshed.\n')

#==============================================================================
def meshCADFaces(event=None):
    if CTK.CADHOOK is None: return
    if CTK.t == []: return 
    import OCC.PyTree as OCC
    hmax = CTK.varsFromWidget(VARS[0].get(), 1)[0]
    hausd = CTK.varsFromWidget(VARS[1].get(), 1)[0]
    OCC._meshAllFacesTri(CTK.CADHOOK, CTK.t, hmax=hmax, hausd=hausd)
    CTK.TXT.insert('START', 'All CAD faces meshed.\n')

#==============================================================================
# Create app widgets
#==============================================================================
def createApp(win):
    
    # - Frame -
    Frame = TTK.LabelFrame(win, borderwidth=2, relief=CTK.FRAMESTYLE,
                           text='tkCADMesh  [ + ]  ', font=CTK.FRAMEFONT, takefocus=1)
    #BB = CTK.infoBulle(parent=Frame, text='Mesh CAD surface.\nCtrl+w to close applet.', temps=0, btype=1)
    Frame.bind('<Control-w>', hideApp)
    Frame.bind('<ButtonRelease-1>', displayFrameMenu)
    Frame.bind('<ButtonRelease-3>', displayFrameMenu)
    Frame.bind('<Enter>', lambda event : Frame.focus_set())
    Frame.columnconfigure(0, weight=1)
    Frame.columnconfigure(1, weight=1)
    WIDGETS['frame'] = Frame
    
    # - Frame menu -
    FrameMenu = TTK.Menu(Frame, tearoff=0)
    FrameMenu.add_command(label='Close', accelerator='Ctrl+w', command=hideApp)
    CTK.addPinMenu(FrameMenu, 'tkCADMesh')
    WIDGETS['frameMenu'] = FrameMenu

    #- VARS -
    # -0- hmax -
    V = TK.StringVar(win); V.set('0.1'); VARS.append(V)
    # -0- hausd -
    V = TK.StringVar(win); V.set('1.e-1'); VARS.append(V)

    # Generate CAD surface mesh    
    B = TTK.Entry(Frame, textvariable=VARS[0], background='White', width=10)
    B.grid(row=0, column=0, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='H step of surface mesh.')

    B = TTK.Entry(Frame, textvariable=VARS[1], background='White', width=10)
    B.grid(row=0, column=1, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Deviation of surface mesh.')

    B = TTK.Button(Frame, text="Mesh all CAD edges", command=meshCADEdges)
    B.grid(row=1, column=0, columnspan=2, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Mesh all CAD egdes with given h and deviation.')

    B = TTK.Button(Frame, text="Mesh all CAD faces", command=meshCADFaces)
    B.grid(row=2, column=0, columnspan=2, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Mesh the CAD faces from edges.')
    
#==============================================================================
# Called to display widgets
#==============================================================================
def showApp():
    try: CTK.WIDGETS['SurfNoteBook'].add(WIDGETS['frame'], text='tkCADMesh')
    except: pass
    CTK.WIDGETS['SurfNoteBook'].select(WIDGETS['frame'])
    
#==============================================================================
# Called to hide widgets
#==============================================================================
def hideApp(event=None):
    CTK.WIDGETS['SurfNoteBook'].hide(WIDGETS['frame'])

#==============================================================================
# Update widgets when global pyTree t changes
#==============================================================================
def updateApp(): return

#==============================================================================
def displayFrameMenu(event=None):
    WIDGETS['frameMenu'].tk_popup(event.x_root+50, event.y_root, 0)

#==============================================================================
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        CTK.FILE = sys.argv[1]
        try:
            CTK.t = C.convertFile2PyTree(CTK.FILE)
            (CTK.Nb, CTK.Nz) = CPlot.updateCPlotNumbering(CTK.t)
            CTK.display(CTK.t)
        except: pass

    # Main window
    (win, menu, file, tools) = CTK.minimal('tkCADMesh '+C.__version__)

    createApp(win); showApp()

    # - Main loop -
    win.mainloop()
