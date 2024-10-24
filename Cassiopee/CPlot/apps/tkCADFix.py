# - fix CAD app -
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
def readCAD(event=None):
    import OCC.PyTree as OCC
    fileName = VARS[0].get()
    fileFmt = VARS[1].get()
    if CTK.CADHOOK is not None:
        hook = CTK.CADHOOK
        OCC.freeHook(hook)
        # free the previous hook
        edges = Internal.getNodeFromName1(CTK.t, 'EDGES')
        edges[2] = []
        faces = Internal.getNodeFromName1(CTK.t, 'FACES')
        faces[2] = []
    hook = OCC.readCAD(fileName, fileFmt)
    # Previous hmax, hausd?
    [hmax, hausd] = OCC.getCADcontainer(CTK.t)
    if hmax is None or (hmax < 0 and hausd < 0):
        (hmax,hmin,hausd) = OCC.occ.analyseEdges(hook)
    OCC._setCADcontainer(CTK.t, fileName, fileFmt, hmax, hausd)
    CTK.CADHOOK = hook
    # remesh and redisplay
    CTK.setCursor(2, WIDGETS['frame'])
    OCC._meshAllEdges(hook, CTK.t, hmax=hmax, hausd=hausd)
    OCC._meshAllFacesTri(hook, CTK.t, hmax=hmax, hausd=hausd)
    CTK.setCursor(0, WIDGETS['frame'])
    CTK.display(CTK.t)
    CTK.TXT.insert('START', 'CAD loaded from %s.\n'%fileName)

#==============================================================================
def writeCAD(event=None):
    import OCC.PyTree as OCC
    if CTK.CADHOOK is None: return 
    hook = CTK.CADHOOK
    fileName = VARS[0].get()
    fileFmt = VARS[1].get()
    OCC.writeCAD(hook, fileName, fileFmt)
    CTK.TXT.insert('START', 'CAD written in %s.\n'%fileName)

#==============================================================================
def sewCAD(event=None):
    import OCC.PyTree as OCC
    if CTK.CADHOOK is None: return
    tol = CTK.varsFromWidget(VARS[2].get(), 1)[0]
    hook = CTK.CADHOOK
    [hmax, hausd] = OCC.getCADcontainer(CTK.t)
    faces = []
    nzs = CPlot.getSelectedZones()
    for nz in nzs:
        nob = CTK.Nb[nz]+1
        noz = CTK.Nz[nz]
        z = CTK.t[2][nob][2][noz]
        CAD = Internal.getNodeFromName1(z, 'CAD')
        if CAD is not None:
            no = Internal.getNodeFromName1(CAD, 'no')
            no = Internal.getValue(no)
            faces.append(no)
    OCC._sewing(hook, faces, tol)
    # remesh CAD and redisplay
    edges = Internal.getNodeFromName1(CTK.t, 'EDGES')
    edges[2] = []
    faces = Internal.getNodeFromName1(CTK.t, 'FACES')
    faces[2] = []
    CTK.setCursor(2, WIDGETS['frame'])
    OCC._meshAllEdges(hook, CTK.t, hmax=hmax, hausd=hausd) # loose manual remeshing
    OCC._meshAllFacesTri(hook, CTK.t, hmax=hmax, hausd=hausd)
    CTK.setCursor(0, WIDGETS['frame'])
    CTK.display(CTK.t)
    CTK.TXT.insert('START', 'CAD sewed with %g.\n'%tol)

#==============================================================================
def filletCAD(event=None):
    import OCC.PyTree as OCC
    if CTK.CADHOOK is None: return
    radius = CTK.varsFromWidget(VARS[3].get(), 1)[0]
    hook = CTK.CADHOOK
    [hmax, hausd] = OCC.getCADcontainer(CTK.t)
    # Get selected edges
    nzs = CPlot.getSelectedZones()
    edges = []
    for nz in nzs:
        nob = CTK.Nb[nz]+1
        noz = CTK.Nz[nz]
        z = CTK.t[2][nob][2][noz]
        CAD = Internal.getNodeFromName1(z, 'CAD')
        if CAD is not None:
            no = Internal.getNodeFromName1(CAD, 'no')
            no = Internal.getValue(no)
            edges.append(no)
    if edges == []: 
        CTK.TXT.insert('START', 'No valid edges in selection.\n')
        return
    OCC._addFillet(hook, edges, radius)

    # remesh CAD and redisplay
    edges = Internal.getNodeFromName1(CTK.t, 'EDGES')
    edges[2] = []
    faces = Internal.getNodeFromName1(CTK.t, 'FACES')
    faces[2] = []
    CTK.setCursor(2, WIDGETS['frame'])
    OCC._meshAllEdges(hook, CTK.t, hmax=hmax, hausd=hausd) # loose manual remeshing...
    OCC._meshAllFacesTri(hook, CTK.t, hmax=hmax, hausd=hausd)
    CTK.setCursor(0, WIDGETS['frame'])
    (CTK.Nb, CTK.Nz) = CPlot.updateCPlotNumbering(CTK.t)
    CTK.TKTREE.updateApp()
    CTK.display(CTK.t)
    CTK.TXT.insert('START', 'Fillet added.\n')

#==============================================================================
def removeFaces(event=None):
    import OCC.PyTree as OCC
    if CTK.CADHOOK is None: return
    hook = CTK.CADHOOK
    [hmax, hausd] = OCC.getCADcontainer(CTK.t)
    # Get selected edges
    nzs = CPlot.getSelectedZones()
    faces = []
    for nz in nzs:
        nob = CTK.Nb[nz]+1
        noz = CTK.Nz[nz]
        z = CTK.t[2][nob][2][noz]
        CAD = Internal.getNodeFromName1(z, 'CAD')
        if CAD is not None:
            no = Internal.getNodeFromName1(CAD, 'no')
            no = Internal.getValue(no)
            faces.append(no)
    if faces == []: 
        CTK.TXT.insert('START', 'No valid faces in selection.\n')
        return
    OCC._removeFaces(hook, faces)

    # remesh CAD and redisplay
    edges = Internal.getNodeFromName1(CTK.t, 'EDGES')
    edges[2] = []
    faces = Internal.getNodeFromName1(CTK.t, 'FACES')
    faces[2] = []
    CTK.setCursor(2, WIDGETS['frame'])
    OCC._meshAllEdges(hook, CTK.t, hmax=hmax, hausd=hausd) # loose manual remeshing...
    OCC._meshAllFacesTri(hook, CTK.t, hmax=hmax, hausd=hausd)
    CTK.setCursor(0, WIDGETS['frame'])
    (CTK.Nb, CTK.Nz) = CPlot.updateCPlotNumbering(CTK.t)
    CTK.TKTREE.updateApp()
    CTK.display(CTK.t)
    CTK.TXT.insert('START', 'Faces removed from CAD.\n')

#==============================================================================
def fillHole(event=None):
    import OCC.PyTree as OCC
    if CTK.CADHOOK is None: return
    hook = CTK.CADHOOK
    [hmax, hausd] = OCC.getCADcontainer(CTK.t)
    # Get selected edges
    nzs = CPlot.getSelectedZones()
    edges = []
    for nz in nzs:
        nob = CTK.Nb[nz]+1
        noz = CTK.Nz[nz]
        z = CTK.t[2][nob][2][noz]
        CAD = Internal.getNodeFromName1(z, 'CAD')
        if CAD is not None:
            no = Internal.getNodeFromName1(CAD, 'no')
            no = Internal.getValue(no)
            edges.append(no)
    if edges == []: 
        CTK.TXT.insert('START', 'No valid edges in selection.\n')
        return
    OCC._fillHole(hook, edges)

    # remesh CAD and redisplay
    edges = Internal.getNodeFromName1(CTK.t, 'EDGES')
    edges[2] = []
    faces = Internal.getNodeFromName1(CTK.t, 'FACES')
    faces[2] = []
    CTK.setCursor(2, WIDGETS['frame'])
    OCC._meshAllEdges(hook, CTK.t, hmax=hmax, hausd=hausd) # loose manual remeshing...
    OCC._meshAllFacesTri(hook, CTK.t, hmax=hmax, hausd=hausd)
    CTK.setCursor(0, WIDGETS['frame'])
    (CTK.Nb, CTK.Nz) = CPlot.updateCPlotNumbering(CTK.t)
    CTK.TKTREE.updateApp()
    CTK.display(CTK.t)
    CTK.TXT.insert('START', 'Fill hole in CAD.\n')

#==============================================================================
# Create app widgets
#==============================================================================
def createApp(win):

    # - Frame -
    Frame = TTK.LabelFrame(win, borderwidth=2, relief=CTK.FRAMESTYLE,
                           text='tkCADFix  [ + ]  ', font=CTK.FRAMEFONT, takefocus=1)
    #BB = CTK.infoBulle(parent=Frame, text='Fix CAD.\nCtrl+w to close applet.', temps=0, btype=1)
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
    CTK.addPinMenu(FrameMenu, 'tkCADFix')
    WIDGETS['frameMenu'] = FrameMenu

    #- VARS -
    if CTK.CADHOOK is not None:
        import OCC
        fileName, fileFmt = OCC.occ.getFileAndFormat(CTK.CADHOOK)
    else: fileName = ''; fileFmt = 'fmt_step'

    # -0- CAD file name -
    V = TK.StringVar(win); V.set('file.step'); VARS.append(V)
    V.set(fileName)
    # -1- CAD file format -
    V = TK.StringVar(win); V.set('fmt_step'); VARS.append(V)
    V.set(fileFmt)
    # -2- Sewing tolerance -
    V = TK.StringVar(win); V.set('1.e-6'); VARS.append(V)
    # -3- Fillet radius -
    V = TK.StringVar(win); V.set('0.1'); VARS.append(V)

    # Read/write CAD file    
    B = TTK.Button(Frame, text="Read", command=readCAD)
    B.grid(row=1, column=0, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Read CAD in tree.')

    B = TTK.Button(Frame, text="Write", command=writeCAD)
    B.grid(row=1, column=1, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Write CAD to file.')

    B = TTK.Entry(Frame, textvariable=VARS[0], background='White', width=15)
    B.grid(row=0, column=0, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='CAD file name.')

    B = TTK.OptionMenu(Frame, VARS[1], 'fmt_step', 'fmt_iges')
    B.grid(row=0, column=1, sticky=TK.EW)

    # Sewing
    B = TTK.Button(Frame, text="Sew", command=sewCAD)
    B.grid(row=2, column=0, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Sew CAD to fix multiple edges.')

    B = TTK.Entry(Frame, textvariable=VARS[2], background='White', width=10)
    B.grid(row=2, column=1, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Sewing tolerance.')
    B.bind('<Return>', sewCAD)

    # Fillet
    B = TTK.Button(Frame, text="Fillet", command=filletCAD)
    B.grid(row=3, column=0, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Make a fillet from edges selection.')

    B = TTK.Entry(Frame, textvariable=VARS[3], background='White', width=10)
    B.grid(row=3, column=1, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Fillet radius.')
    B.bind('<Return>', filletCAD)

    # Remove faces
    B = TTK.Button(Frame, text="Remove faces", command=removeFaces)
    B.grid(row=4, column=0, columnspan=2, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Remove selected faces from CAD.')

    # Fill hole
    B = TTK.Button(Frame, text="Fill hole", command=fillHole)
    B.grid(row=5, column=0, columnspan=2, sticky=TK.EW)
    BB = CTK.infoBulle(parent=B, text='Fill hole from CAD edges.')


#==============================================================================
# Called to display widgets
#==============================================================================
def showApp():
    try: CTK.WIDGETS['TreeNoteBook'].add(WIDGETS['frame'], text='tkCADFix')
    except: pass
    CTK.WIDGETS['TreeNoteBook'].select(WIDGETS['frame'])
    
#==============================================================================
# Called to hide widgets
#==============================================================================
def hideApp(event=None):
    CTK.WIDGETS['TreeNoteBook'].hide(WIDGETS['frame'])

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
    (win, menu, file, tools) = CTK.minimal('tkCADFix '+C.__version__)

    createApp(win); showApp()

    # - Main loop -
    win.mainloop()
