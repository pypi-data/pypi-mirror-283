from .ui_Vis_Tab import*
from .Input_Tab_tools import *
from .Output_Tab import outType_dict
from .TabTools import*
if __package__ or "." in __name__:
  import PaIRS_UniNa.PaIRS_PIV as PaIRS_lib
else:
  if platform.system() == "Darwin":
    sys.path.append('../lib/mac')
    #sys.path.append('../lib')
  else:
    #sys.path.append('PaIRS_PIV')
    sys.path.append('../lib')
    sys.path.append('TpivPython/lib')
  import PaIRS_PIV as PaIRS_lib # type: ignore

spin_tips={   
    'min':  'Minimum level',
    'mean': 'Mean level',
    'max':  'Maximum level',
    'range':  'Level range',
    'xmin':  'Minimum x coordinate',
    'xmax':  'Maximum x coordinate',
    'ymin':  'Minimum y coordinate',
    'ymax' : 'Maximum y coordinate',
    'nclev':    'Number of color levels',
    'vecsize':  'Size of velocity vectors',
    'vecspac':  'Spacing of velocity vectors',
    'streamdens':  'Density of streamlines',
    'img':      'Image number',
    'frame':    'Frame number',
    'cam':      'Camera number',
    'it':       'Iteration number',
}
check_tips={}
radio_tips={}
line_edit_tips={}
button_tips={
    'tool_CollapBox_PlotTools': 'Open/close plot tools box',
    'CollapBox_PlotTools':  'Open/close plot tools box',
    'ShowIW':   'Show/hide interrogation windows',
    'SubMIN':   'Subtract minimum',
    'Contourf': 'Contour plot mode',
    'cmap':     'Colormap',
    'automatic_levels': 'Automatic levels',
    'automatic_sizes':  'Automatic sizes',
    'restore':  'Restore levels',
    'resize':   'Resize',
    'invert_y': 'Invert y axis',
    'left':     'Change page setting',
    'right':    'Change page setting',
    'qt_toolbar_ext_button':    'Plot interaction',
    'unit': 'Type of unit',
    'cvec': 'Color of vectors/streamlines',
    'view': 'Inspect pre-existing results',
    'ShowCR': 'Show common region',
}
combo_tips={
    'map_var':      'Map variable',
    'field_rep':    'Field representation', 
}
Flag_VIS_DEBUG=False

FlagGenerateColormaps=False
FlagVerticalColormap=True
VIS_ColorMaps = {
    'main': ['gray','jet','viridis', 'cividis', 'inferno', 'hsv','brg'],
    'Miscellaneous': ['magma','plasma',
                      'terrain', 'ocean','twilight', 'rainbow','cubehelix', 'prism','flag'],
    'Sequential': ['binary', 'bone', 'pink', 
                   'spring', 'summer', 'autumn', 'winter', 'cool',
                      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper'],
    'Diverging': ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
    'Qualitative': ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                      'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                      'tab20c']
    }
FlagGenerateColorvectors=False
VIS_VectorColors={
    'black': (0, 0, 0),
    'red': (1, 0, 0),
    'green': (0, 1, 0),
    'blue': (0, 0, 1),
    'cyan': (0, 1, 1),
    'magenta': (1, 0, 1),
    'yellow': (1, 1, 0),
    'white': (1, 1, 1),
}
nStepsSlider=1e5
nPixelsPerVector=10 #one vector each nPixelsPerVector pixels

class NamesPIV(TABpar):

    def __init__(self,Process=ProcessTypes.null,Step=StepTypes.null):
        self.setup(Process,Step)
        super().__init__('OUTpar','Output')

    def setup(self,Process,Step):
        self.Process            = Process
        self.Step               = Step
   
        self.img='img'
        self.X='X'
        self.Y='Y'
        self.Z='Z'
        self.x='x'
        self.y='y'
        self.z='z'
        self.u='U'
        self.v='V'
        self.w='W'
        self.Mod='Mod'
        self.up='uu'
        self.vp='vv'
        self.wp='ww'
        self.uvp='uv'
        self.uwp='uw'
        self.vwp='vw'
        self.dPar='dPar'
        self.dOrt='dOrt'
        self.sn='SN'
        self.FCl='CC'
        self.Info='Info'
        allFields={}
        for f,v in self.__dict__.items():
            allFields[v]=f
        self.allFields=allFields
        self.combo_dict={
                    self.img: 'image intesity',
                    self.Mod: 'magnitude',
                    self.z:   'z',
                    self.u:   'U',
                    self.v:   'V',
                    self.w:   'W',
                    self.up:  "<u'u'>",
                    self.vp:  "<v'v'>",
                    self.vwp:  "<w'w'>",
                    self.uvp:  "<u'v'>",
                    self.uwp:  "<u'w'>",
                    self.vwp:  "<v'w'>",
                    self.dPar: "epipolar || disp.",
                    self.dOrt: "epipolar ⊥ disp.",
                    self.sn:   "S/N",
                    self.Info: "Info",
                    self.FCl:   "CC"
                    }
        self.combo_dict_keys={}
        for k,v in self.combo_dict.items(): self.combo_dict_keys[v]=k
        self.titles_dict={
                    self.img: 'intensity',
                    self.Mod: "velocity magnitude",
                    self.z: "z coordinate",
                    self.u: "x-velocity component",
                    self.v: "y-velocity component",
                    self.w: "z-velocity component",
                    self.up:  "x normal Reynolds stress",
                    self.vp:  "y normal Reynolds stress",
                    self.wp:  "z normal Reynolds stress",
                    self.uvp:  "xy tangential Reynolds stress",
                    self.uwp:  "xz tangential Reynolds stress",
                    self.vwp:  "yz tangential Reynolds stress",
                    self.dPar: "epipolar parallel displacement",
                    self.dOrt: "epipolar orthogonal displacement",
                    self.sn: "signal-to-noise ratio",
                    self.Info: "outlier info",
                    self.FCl:   "Correlation coefficient"
                    }
        self.titles_cb_dict={
                    self.img: '',
                    self.Mod: "|Vel|",
                    self.z: "z",
                    self.u: "U",
                    self.v: "V",
                    self.w: "W",
                    self.up:  "<u'u'>",
                    self.vp:  "<v'v'>",
                    self.wp:  "<w'w'>",
                    self.uvp:  "<u'v'>",
                    self.uwp:  "<u'w'>",
                    self.vwp:  "<v'w'>",
                    self.dPar: "d par.",
                    self.dOrt: "d ort.",
                    self.sn: "S/N",
                    self.Info: "i",
                    self.FCl:   "CC"
                    }

        self.fields=list(self.combo_dict)
        self.combo_list=[self.combo_dict[f] for f in self.fields]
        self.titles_list=[self.titles_dict[f] for f in self.fields]
        self.titles_cb_list=[self.titles_cb_dict[f] for f in self.fields]
        
        self.img_ind=[self.fields.index(f) for f in [self.img]]

        # should start with x, y ,u ,v
        if Step==StepTypes.disp:
            self.instVel=[self.x,self.y,self.z,self.dPar,self.dOrt] #,self.FCl]
            self.instVel_plot=[self.z,self.dPar,self.dOrt] #,self.FCl]
            self.avgVel=copy.deepcopy(self.instVel)
            self.avgVel_plot=copy.deepcopy(self.instVel_plot)
        elif Step==StepTypes.spiv:
            self.instVel=[self.x,self.y,self.z,self.u,self.v,self.w,self.FCl,self.Info,self.sn]
            self.instVel_plot=[self.Mod,self.u,self.v,self.w,self.FCl,self.Info,self.sn]
            self.avgVel=[self.x,self.y,self.z,self.u,self.v,self.w,self.up,self.vp,self.wp,self.uvp,self.uwp,self.vwp,self.FCl,self.Info,self.sn]
            self.avgVel_plot=[self.Mod,self.u,self.v,self.w,self.up,self.vp,self.wp,self.uvp,self.uwp,self.vwp,self.FCl,self.Info,self.sn]
        else: # for now should be StepTypes.piv
            self.instVel=[self.x,self.y,self.u,self.v,self.FCl,self.Info,self.sn]
            self.instVel_plot=[self.Mod,self.u,self.v,self.FCl,self.Info,self.sn]
            self.avgVel=[self.x,self.y,self.u,self.v,self.up,self.vp,self.uvp,self.FCl,self.Info,self.sn]
            self.avgVel_plot=[self.Mod,self.u,self.v,self.up,self.vp,self.uvp,self.FCl,self.Info,self.sn]
   
        self.instVelFields=[self.allFields[f] for f in self.instVel   ]
        self.instVel_plot_ind=[self.fields.index(f) for f in self.instVel_plot if f in self.fields]
        self.avgVelFields=[self.allFields[f] for f in self.avgVel  ]
        self.avgVel_plot_ind=[self.fields.index(f) for f in self.avgVel_plot if f in self.fields]

    def pick(self,lista,indici):
        return [lista[i] for i in indici]
    
class VISpar(TABpar):
    FlagVis=True
    FlagAutoLevels=True
    FlagAutoSizes=True    
    class OUT(TABpar):
        def __init__(self):
            self.x     = 0                
            self.y     = 0                 
            self.w     = None               
            self.h     = None
            self.vecop  = []  

            self.x_min = 0.0
            self.x_max = 0.0
            self.y_min = 0.0
            self.y_max = 0.0      

            self.xres = 1
            self.pixAR = 1

            super().__init__('VISpar.Out','Vis')
    
    class PRO(TABpar):
        def __init__(self):
            WSize_init=[128, 64, 32]
            WSpac_init=[ 32, 16, 8]
            self.Vect=[copy.deepcopy(WSize_init),copy.deepcopy(WSpac_init),copy.deepcopy(WSize_init),copy.deepcopy(WSpac_init)]
            self.FlagBordo=False
            super().__init__('VISpar.Pro','Vis')

    def __init__(self,Process=ProcessTypes.null,Step=StepTypes.null):
        self.setup(Process,Step)
        super().__init__('VISpar','Vis')
        self.unchecked_fields+=['FlagAutomaticLevels','FlagAutomaticSizes','setPage']

    def setup(self,Process,Step):
        self.Process = Process
        self.Step    = Step
        self.type     = 0
        self.FlagView = False

        self.img=-1
        self.nimg=0
        self.frame=1
        self.it=1 
        self.cam=0
        self.ncam=0
        
        self.path=''
        self.imList=[[[],[]]*self.ncam]
        self.image_file=''
        self.fres=[]  #lambda k: ''
        self.outPathRoot=''  #useful in procOhtName(self.VISpar)
        self.name_proc=''
        self.result_file=''
        self.FlagResult=False

        self.FlagMIN   = False
        self.FlagTR    = False
        self.LaserType = 0
        self.Nit       = 1
        self.imListMin=[[[],[]]*self.ncam]

        self.image_file_Min=''
        self.result_file_Mean=''
        self.image_file_Current=''
        self.result_file_Current=''

        self.FlagShowIW=False
        self.FlagShowCR=False
        self.FlagSubMIN=False
        self.variable=''
        self.variableKey=''
        self.field_rep=0

        self.FlagYInvert=[False,False]
        self.FlagResetLevels=True
        self.FlagResetSizes=True
        self.setPage=0

        img=NamesPIV().img
        self.vcolorMap={img: 'gray'}
        self.colorMap='gray'
        self.vvectorColor={img: 'green'}
        self.vectorColor='green'
        self.vLim={img: 1}
        self.vmin_default={img: 0}
        self.vmax_default={img: 1}
        self.vmean_default={img: 0.5}
        self.vrange_default={img: 1}
        self.vmin={img: 0}
        self.vmax={img: 1}
        self.vmean={img: 0.5}
        self.vrange={img: 1}
        self.min=0
        self.max=1
        self.mean=0.5
        self.range=1
        
        self.unit=[False,True]
        self.size_default=[[0,1,0,1,1],[0,1,0,1,1]] #xmin,xmax,ymin,ymax,max vec spacing
        self.size=[[0,1,0,1,1],[0,1,0,1,1]] #xmin,xmax,ymin,ymax,max vec spacing
        self.xmin=0
        self.xmax=1
        self.ymin=0
        self.ymax=1

        self.nclev=30
        self.vecsize=1
        self.vecspac=1
        self.streamdens=1

        self.FlagContourf=False
        
        self.Out=self.OUT()
        self.Pro=self.PRO()

        self.FlagCAL    = Process in ProcessTypes.threeCameras
        self.calList    = []
        self.calEx      = []

        self.FlagDISP   = Step==StepTypes.disp
        self.dispFile   = ''
    
    def resF(self,i):
        fres=self.fres
        if not fres: return ''
        outPathRoot=fres[0]
        ndig=fres[1]
        outExt=fres[2]
        if type(i)==str:
            return f"{outPathRoot}{i}{outExt}"
        elif type(i)==int:
             return f"{outPathRoot}{i:0{ndig:d}d}{outExt}"
        else:
            return ''

class Vis_Tab(gPaIRS_Tab):
    class VIS_Tab_Signals(gPaIRS_Tab.Tab_Signals):
        pass

    def __init__(self,parent: QWidget =None, flagInit= __name__ == "__main__"):
        super().__init__(parent,Ui_VisTab,VISpar)
        self.signals=self.VIS_Tab_Signals(self)

        #------------------------------------- Graphical interface: widgets
        self.TABname='Vis'
        self.ui: Ui_VisTab
        self.Ptoolbar=None
        self.addPlotToolBar()

        self.ui.sliders=self.findChildren(QSlider)
        for slider in (self.ui.slider_min,self.ui.slider_max,self.ui.slider_mean,self.ui.slider_range):
            slider.setMinimum(0)
            slider.setMaximum(nStepsSlider)
            slider.setSingleStep(int(nStepsSlider/100))
        
        #necessary to change the name and the order of the items
        for g in list(globals()):
            if '_items' in g or '_ord' in g or '_tips' in g:
                #pri.Info.blue(f'Adding {g} to {self.name_tab}')
                setattr(self,g,eval(g))

        if __name__ == "__main__": 
            self.app=app
            setAppGuiPalette(self)

        #------------------------------------- Graphical interface: miscellanea
        self.brush_cursor= QCursor(QPixmap(icons_path+"brush_cursor.png").scaled(24,24))
        self.FlagNormalCursor=True

        self.img=None
        self.imgshow=None
        self.cb=None
        self.orect=[]
        self.xres=self.yres=1.0

        self.map=None
        self.contour=None
        self.qui=None
        self.stream=None
        self.CR=None

        self.namesPIV=NamesPIV()

        pri.Time.magenta('Colormap generation: start')
        # Create the popup menu
        self.colorMapMenu = QMenu(self)
        # Add the colormap thumbnails to the menu
        def on_colormap_selected(name):
            self.VISpar.vcolorMap[self.VISpar.variableKey]=self.VISpar.colorMap=name
        for k, colorMapClass in enumerate(VIS_ColorMaps):
            if not k: menu=self.colorMapMenu
            else: menu=self.colorMapMenu.addMenu(colorMapClass)
            #for colormap in VIS_ColorMaps[colorMapClass]:
            for colormap in VIS_ColorMaps[colorMapClass]:
                imgMapPath=icons_path+'colormaps/'+colormap+'.png'
                if os.path.exists(imgMapPath) and not FlagGenerateColormaps:
                    pixmap = QPixmap(imgMapPath)
                else:
                    pixmap=create_colormap_image(colormap, 25, 50, FlagVerticalColormap, imgMapPath)
                action = menu.addAction(QIcon(pixmap), ' '+colormap)
                action.triggered.connect(lambda _, name=colormap: on_colormap_selected(name))   
        pri.Time.magenta('Colormap generation: end')         

        pri.Time.magenta('Vector color generation: start')
        # Create the popup menu
        self.vectorColorMenu = QMenu(self)
        # Add the colormap thumbnails to the menu
        def on_vectorcolor_selected(name):
            self.VISpar.vvectorColor[self.VISpar.variableKey]=self.VISpar.vectorColor=name
        for colorName, color in VIS_VectorColors.items():
            menu=self.vectorColorMenu
            #for colormap in VIS_ColorMaps[colorMapClass]:
            imgMapPath=icons_path+'colormaps/'+colorName+'Vector.png'
            if os.path.exists(imgMapPath) and not FlagGenerateColorvectors:
                pixmap = QPixmap(imgMapPath)
            else:
                pixmap=create_arrow_pixmap(color, 50, 50, imgMapPath)
            action = menu.addAction(QIcon(pixmap), ' '+colorName.lower())
            action.triggered.connect(lambda _, name=colorName: on_vectorcolor_selected(name))   
        pri.Time.magenta('Vector color generation: end')         
            
        #------------------------------------- Declaration of parameters 
        self.VISpar_base=VISpar()
        self.VISpar:VISpar=self.TABpar
        self.VISpar_old:VISpar=self.TABpar_old
        
        #------------------------------------- Callbacks 
        self.defineWidgets()
        self.setupWid()  #---------------- IMPORTANT

        FlagPreventAddPrev_Slider=False
        for n in ('min','max','mean','range','nclev','vecsize','vecspac','streamdens'):
            def defineSliderCallbackSet(n):
                spin:QSpinBox=getattr(self.ui,'spin_'+n)
                slider:QSlider=getattr(self.ui,'slider_'+n)

                if n in ('min','max','mean','range'):
                    changingAction=lambda: self.sliderLevels_changing(spin,slider,FlagPreventAddPrev_Slider)
                    callback=self.wrappedCallback(spin_tips[n],changingAction)
                    action=lambda: self.spinLevels_action(spin)
                elif n in ('nclev','vecsize','vecspac','streamdens'):
                    changingAction=lambda: self.sliderFieldRep_changing(spin,slider,FlagPreventAddPrev_Slider)
                    callback=self.wrappedCallback(spin_tips[n],changingAction)
                    action=lambda: self.spinFieldRep_action(spin)
                setting=lambda: self.slider_set(spin,slider)

                slider.valueChanged.connect(callback)
                
                if n in ('nclev','streamdens'):
                    def sliderMessage(s:QSlider):
                        if self.VISpar.field_rep==2:
                            tip = f"Release to repaint"
                        else: tip=""
                        QToolTip.showText(s.mapToGlobal(s.rect().topLeft()), tip)
                    slider.sliderPressed.connect(lambda: sliderMessage(slider))

                setattr(self,'slider_'+n+'_callbcak',callback)
                setattr(self,'spin_'+n+'_action',action)
                setattr(self,'spin_'+n+'_set',setting)

            defineSliderCallbackSet(n)


        for k,n in enumerate(['xmin','xmax','ymin','ymax']):
            def defineXYAction(k,n):
                spin=getattr(self.ui,'spin_'+n)
                action=lambda: self.spin_xy_action(spin,k)
                setattr(self,'spin_'+n+'_action',action)
            defineXYAction(k,n)
        
        self.plot_callback=self.wrappedCallback('Plot interaction',self.updatingPlot)
        self.ui.plot.addfuncrelease['fPlotCallback']=self.plot_callback

        self.button_left_action=lambda: self.leftrightCallback(-1)
        self.button_right_action=lambda: self.leftrightCallback(+1)

        self.QS_copy2clipboard=QShortcut(QKeySequence('Ctrl+C'), self.ui.plot)  
        self.QS_copy2clipboard.activated.connect(self.ui.plot.copy2clipboard)
        self.QS_copy2newfig=QShortcut(QKeySequence('Ctrl+D'), self.ui.plot)
        self.QS_copy2newfig.activated.connect(lambda: self.ui.plot.copy2newfig(self.ui.name_var.toolTip()))
        self.load_Img_callback=self.wrappedCallback('Loading image',self.loadImg)
        self.load_Res_callback=self.wrappedCallback('Loading result',self.loadRes)

        self.defineCallbacks()
        self.spins_valueChanged=[self.ui.spin_img,self.ui.spin_frame,self.ui.spin_cam,self.ui.spin_it]
        self.connectCallbacks()
        
        self.defineSettings()
        self.TABsettings.append(self.setMapVar)

        self.adjustTABpar=self.adjustVISpar
        self.setTABlayout=self.setVISlayout

        self.FlagReset=True
        self.FlagResetLevels=True
        self.FlagResetSizes =True

        self.image_file=''
        self.image_raw=None
        self.image=None
        self.image_file_Min=''
        self.image_Min_raw=None
        self.image_Min=None
        self.nbits=0
        self.result_file=''
        self.result=None
        self.result_file_Mean=''
        self.result_Mean=None
        self.image_file_Load=''
        self.result_file_Load=''

        self.image_Current_raw=None
        self.image_Current=None
        self.result_Current=None

        self.FlagAddPrev=False

        #------------------------------------- Initializing       
        if flagInit:
            self.initialize()
        #else:
        #    self.adjustTABpar()
        #    self.setTABpar(FlagBridge=False)

    def addPlotToolBar(self):
        if self.Ptoolbar:
            self.Ptoolbar.setParent(None)
        self.Ptoolbar = NavigationToolbar(self.ui.plot, self)
        unwanted_buttons = ['Home','Back','Forward','Customize'] #'Subplots','Save'
        for x in self.Ptoolbar.actions():
            if x.text() in unwanted_buttons:
                self.Ptoolbar.removeAction(x)
        self.ui.lay_w_Plot.addWidget(self.Ptoolbar)

    def initialize(self):
        pri.Info.yellow(f'{"*"*20}   VIS initialization   {"*"*20}')
        self.setExample()
        self.adjustVISpar()
        self.setVISlayout()
        self.setTABpar(FlagBridge=False)  #with bridge
        self.add_TABpar('initialization')

    def setExample(self):
        if not basefold_DEBUG_VIS: return
        imSet=ImageSet(path=basefold_DEBUG_VIS)

        k1=0
        k2=imSet.link[k1][0]
        self.VISpar.path=imSet.path
        self.VISpar.imList,_=imSet.genListsFromFrame([k1],[k2+1],imSet.ind_in[k1],imSet.nimg[k1],1,False)

        outPath=myStandardPath(os.path.dirname(imSet.outFiles[outExt.piv][0]))
        outSet=ImageSet(path=outPath,exts=list(outType_dict))
       
        im_min_a=findFiles_sorted(outPath+'*a_min.*')
        if im_min_a: self.VISpar.imListMin[0].append(im_min_a[0])
        im_min_b=findFiles_sorted(outPath+'*b_min.*')
        if im_min_b: self.VISpar.imListMin[0].append(im_min_b[0])
        self.VISpar.fres=[outPath+outSet.fname[0][0],outSet.fname[0][1],outSet.fname[0][2]] #lambda i: outPath+outSet.nameF(outSet.fname[0],i)
        self.VISpar.result_file_Mean=self.VISpar.resF('*').replace('_*','')
        self.VISpar.img=1
        self.VISpar.Out.FlagNone=True
        return

#*************************************************** Adjusting parameters
    def adjustVISpar(self):
        self.VISpar.ncam=len(self.VISpar.imList)
        if self.VISpar.ncam and not self.VISpar.cam: self.VISpar.cam=1
        self.VISpar.nimg=len(self.VISpar.imList[0][0]) if len(self.VISpar.imList[0]) else 0 if self.VISpar.ncam else 0
        if not self.VISpar.nimg and self.VISpar.img:
            FlagResults=self.image_file_Min!='' or self.result_file_Mean!=''
            self.VISpar.img=0 if FlagResults else -1

        FlagNewImage, FlagNewResult = self.adjustImport()

        FlagNew=(not self.VISpar.type and FlagNewImage) or (self.VISpar.type==1 and FlagNewResult)
        FlagDiff=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['img','cam','frame']) or FlagNew

        if (VISpar.FlagAutoLevels and (FlagNewImage or FlagNewResult)):
            self.resetAllLevels()
            if FlagDiff or self.FlagResetLevels:
                self.FlagResetLevels=False
                self.resetLevels()
        elif self.FlagResetLevels:
            self.FlagResetLevels=False
            self.resetLevels()

        if (VISpar.FlagAutoSizes and (FlagNewImage or FlagNewResult)):
            self.resetAllXYLims()
            if FlagDiff or self.FlagResetSizes:
                self.FlagResetSizes=False
                self.resetXYLims()  
        elif self.FlagResetSizes: 
            self.FlagResetSizes=False
            self.resetXYLims()

    def adjustImport(self):
        self.VISpar.image_file=self.VISpar.image_file_Min=''
        if self.VISpar.img%2==0 and self.VISpar.FlagTR and not self.VISpar.LaserType:
            f=[1,0][self.VISpar.frame-1]
        else: f=self.VISpar.frame-1
        if self.VISpar.FlagMIN:
            if 0<=self.VISpar.cam-1<self.VISpar.ncam:
                if 0<=f<len(self.VISpar.imListMin[self.VISpar.cam-1]):
                    self.VISpar.image_file_Min=self.VISpar.imListMin[self.VISpar.cam-1][f]
        else: self.VISpar.image_file_Min=''
        if self.VISpar.img>0:
            self.VISpar.image_file=self.VISpar.path+self.VISpar.imList[self.VISpar.cam-1][self.VISpar.frame-1][self.VISpar.img-1] if len(self.VISpar.imList[self.VISpar.cam-1][self.VISpar.frame-1]) else ''
        elif self.VISpar.img==0:
            self.VISpar.image_file=self.VISpar.image_file_Current if self.VISpar.flagRun==-2 else self.VISpar.image_file_Min
        else:
            self.VISpar.image_file=self.image_file_Load

        self.VISpar.result_file=self.VISpar.result_file_Mean=''
        if self.VISpar.img==-1:
            self.VISpar.result_file=self.result_file_Load 
        elif self.VISpar.img==0 and  self.VISpar.flagRun==-2:
            if (self.VISpar.Step==StepTypes.disp and self.VISpar.it==self.VISpar.Nit) or self.VISpar.Step!=StepTypes.disp:
                self.VISpar.result_file=self.VISpar.result_file_Current
        else:
            if self.VISpar.flagRun!=0: #and self.VISpar.isDifferentFrom(self.VISpar_old,fields=['outPathRoot']):
                if not self.VISpar.FlagView and (self.VISpar.FlagView!=self.VISpar_old.FlagView or self.VISpar.ind[:-1]!=self.VISpar_old.ind[:-1]):
                    self.VISpar.FlagResult=False
                    filename=procOutName(self.VISpar)
                    if os.path.exists(filename):
                        try:
                            from .Saving_tools import loadList
                            data=loadList(filename)
                            ind=list(data[0][0][0].children).index(self.VISpar.Step)+1
                            self.VISpar.FlagResult=data[0][0][ind].procdata.name_proc==self.window().ui.Explorer.ITEpar.procdata.name_proc
                        except:
                            pri.Error.red(f'[VIS] Error while reading the file: {filename}.')
                else: self.VISpar.FlagResult=True
            else:
                self.VISpar.FlagResult=self.VISpar.FlagView
            if self.VISpar.FlagResult:
                if self.VISpar.Step==StepTypes.disp:
                    self.VISpar.result_file_Mean=self.VISpar.resF(f'it{self.VISpar.it}')
                else:
                    self.VISpar.result_file_Mean=self.VISpar.resF('*').replace('_*','')
                if self.VISpar.img>0:
                    if self.VISpar.Step==StepTypes.disp:
                        self.VISpar.result_file=''
                    else:
                        self.VISpar.result_file=self.VISpar.resF(self.VISpar.img)
                elif self.VISpar.img==0:
                    self.VISpar.result_file=self.VISpar.result_file_Mean               
        
        FlagNewImage, FlagNewResult, _=self.importFiles()  
        return FlagNewImage, FlagNewResult
    
    def importFiles(self):
        if self.VISpar.image_file_Min!=self.image_file_Min or self.VISpar.FlagMIN!=self.VISpar_old.FlagMIN or self.FlagReset:
            self.image_file_Min,self.image_Min_raw=self.readImageFile(self.VISpar.image_file_Min)
        if self.VISpar.result_file_Mean!=self.result_file_Mean or self.VISpar.FlagResult!=self.VISpar_old.FlagResult or self.FlagReset:
            self.result_file_Mean,self.result_Mean=self.readResultFile(self.VISpar.result_file_Mean)
       
        FlagNewImage=self.VISpar.image_file!=self.image_file
        if FlagNewImage or self.FlagReset:
            self.image_file=self.VISpar.image_file
            if self.VISpar.img==0:
                if self.VISpar.flagRun==-2:
                    self.image_raw=self.image_Current_raw[self.VISpar.frame] if self.image_Current_raw else None
                else:
                    self.image_raw=self.image_Min_raw
            else:
                self.image_file,self.image_raw=self.readImageFile(self.VISpar.image_file)
        if self.image_raw is None and self.VISpar.img==0: mapVariableList=[]
        else: mapVariableList=[self.namesPIV.img]

        FlagNewResult=self.VISpar.result_file!=self.result_file
        if FlagNewResult or self.FlagReset:
            self.result_file=self.VISpar.result_file
            if self.VISpar.img==0:
                if self.VISpar.flagRun==-2:
                    self.result=self.result_Current
                else:
                    self.result=self.result_Mean
            else:
                self.result_file,self.result=self.readResultFile(self.VISpar.result_file)

        if self.image_raw is not None:
            self.image=transfIm(self.VISpar.Out,Images=[self.image_raw])[0]
            self.getImageInfo()
        else:
            self.image=None
        if self.image_Min_raw is not None:
            self.image_Min=transfIm(self.VISpar.Out,Images=[self.image_Min_raw])[0]
        else:
            self.image_Min=None
        if self.result is not None: 
            self.getResultInfo()

        if self.result: 
            [mapVariableList.append(r) for r in list(self.result)]
        self.FlagReset=False

        if self.namesPIV.img in mapVariableList: comboItemsList=[self.namesPIV.combo_dict[self.namesPIV.img]]
        else: comboItemsList=[]
        for f in list(self.namesPIV.combo_dict)[1:]:
            if f in mapVariableList: comboItemsList.append(self.namesPIV.combo_dict[f])
        if len(comboItemsList)==0: comboItemsList=[self.namesPIV.combo_dict[self.namesPIV.img]]
        if self.VISpar.variable not in comboItemsList:
            self.VISpar.variable=comboItemsList[0]
        self.VISpar.variableKey=self.namesPIV.combo_dict_keys[self.VISpar.variable]
        self.VISpar.type=int(self.VISpar.variableKey!=self.namesPIV.img)

        return FlagNewImage, FlagNewResult, comboItemsList
    
#*************************************************** Layout
    def setVISlayout(self):
        _, _, comboItemsList=self.importFiles()

        FlagLoad=self.image_file_Load!='' or self.result_file_Load!=''
        FlagResults=self.image_file_Min!='' or self.result_file_Mean!=''
        FlagSpinsEnabled=self.VISpar.nimg or FlagLoad
        #self.ui.Plot_tools.setEnabled(FlagSpinsEnabled)

        FlagIW=self.VISpar.type==0 and self.VISpar.Step in (StepTypes.piv,StepTypes.disp,StepTypes.spiv)
        self.ui.button_ShowIW.setVisible(FlagIW)
        if FlagIW:
            tip=f"{'Hide' if self.ui.button_ShowIW.isChecked() else 'Show'} Interrogation Window scheme"
            self.ui.button_ShowIW.setToolTip(tip)
            self.ui.button_ShowIW.setStatusTip(tip)

        FlagCR=self.VISpar.type==0 and self.VISpar.Step in (StepTypes.disp,StepTypes.spiv)
        self.ui.button_ShowCR.setVisible(FlagCR)
        if FlagCR:
            tip=f"{'Hide' if self.ui.button_ShowCR.isChecked() else 'Show'} common region"
            self.ui.button_ShowCR.setToolTip(tip)
            self.ui.button_ShowCR.setStatusTip(tip)

        FlagMIN=self.VISpar.type==0 and self.image_Min is not None and self.VISpar.FlagMIN
        self.ui.button_SubMIN.setVisible(FlagMIN)
        if FlagMIN:
            tip=f"{'Add' if self.ui.button_SubMIN.isChecked() else 'Subtract'} historical minimum background"
            self.ui.button_SubMIN.setToolTip(tip)
            self.ui.button_SubMIN.setStatusTip(tip)

        self.ui.line_img.setVisible(FlagIW or FlagMIN)

        FlagUnit=self.VISpar.Process==ProcessTypes.piv and (self.VISpar.Out.xres!=1.0 or self.VISpar.Out.pixAR!=1.0)
        self.ui.button_unit.setVisible(FlagUnit)
        if FlagUnit:
            tip=f"Set {'pixel' if self.ui.button_unit.isChecked() else 'physical'} units"
            self.ui.button_unit.setToolTip(tip)
            self.ui.button_unit.setStatusTip(tip)

        self.ui.line_unit.setVisible(FlagUnit)   
        
        self.ui.button_Contourf.setVisible(self.VISpar.type)
        self.ui.line_Contourf.setVisible(self.VISpar.type==1)

        self.ui.combo_map_var.clear()
        self.ui.combo_map_var.addItems(comboItemsList)
        
        FlagResult=self.result is not None and "U" in self.result and "V" in self.result
        self.ui.button_cvec.setVisible(FlagResult and self.VISpar.field_rep!=0)
        self.ui.label_field_rep.setVisible(FlagResult)
        self.ui.combo_field_rep.setVisible(FlagResult)
        
        i=self.VISpar.setPage
        c=self.ui.image_levels.count()-1-int(not FlagResult) #or (not self.VISpar.FlagContourf and not self.VISpar.field_rep))
        if i>c: i=0
        self.ui.image_levels.setCurrentIndex(i)
        self.ui.label_title.setText(f"Settings ({i+1}/{c+1})")

        Lim=self.VISpar.vLim[self.VISpar.variableKey]
        step=Lim/nStepsSlider
        self.ui.spin_min.setMinimum(-Lim if self.VISpar.type else 0)
        self.ui.spin_min.setMaximum(Lim-2*step)
        self.ui.spin_max.setMinimum(-Lim+2*step if self.VISpar.type else 2*step)
        self.ui.spin_max.setMaximum(Lim)
        self.ui.spin_mean.setMinimum(-Lim+step if self.VISpar.type else step)
        self.ui.spin_mean.setMaximum(Lim-step)
        self.ui.spin_range.setMinimum(2*step)
        self.ui.spin_range.setMaximum(2*Lim if self.VISpar.type else step)
        self.ui.spin_vecspac.setMaximum(self.VISpar.size[1][4])

        self.ui.label_vecspac.setVisible(self.VISpar.field_rep==1)
        self.ui.slider_vecspac.setVisible(self.VISpar.field_rep==1)
        self.ui.spin_vecspac.setVisible(self.VISpar.field_rep==1)
        self.ui.label_vecsize.setVisible(self.VISpar.field_rep==1)
        self.ui.slider_vecsize.setVisible(self.VISpar.field_rep==1)
        self.ui.spin_vecsize.setVisible(self.VISpar.field_rep==1)
        self.ui.spin_vecspac.setMaximum(self.VISpar.size_default[1][-1])
        self.ui.label_streamdens.setVisible(self.VISpar.field_rep==2)
        self.ui.slider_streamdens.setVisible(self.VISpar.field_rep==2)
        self.ui.spin_streamdens.setVisible(self.VISpar.field_rep==2)

        self.ui.spin_img.setMinimum(-1)
        self.ui.spin_img.setMaximum(self.VISpar.nimg if self.VISpar.nimg else 0 if FlagResults else -1)
        #self.ui.spin_img.setEnabled(FlagSpinsEnabled)
        self.ui.spin_frame.setEnabled(FlagSpinsEnabled)
        self.ui.spin_cam.setMaximum(self.VISpar.ncam)
        self.ui.spin_cam.setEnabled(FlagSpinsEnabled and self.VISpar.ncam>1)

        FlagCamFrame=self.VISpar.img>-1 and self.VISpar.type==0
        self.ui.label_frame.setVisible(FlagCamFrame)
        self.ui.spin_frame.setVisible(FlagCamFrame)
        self.ui.label_cam.setVisible(FlagCamFrame)
        self.ui.spin_cam.setVisible(FlagCamFrame)
        FlagDispResult=self.VISpar.img==0 and self.VISpar.Step==StepTypes.disp and self.VISpar.type==1
        self.ui.label_it.setVisible(FlagDispResult)
        self.ui.spin_it.setVisible(FlagDispResult)
        self.ui.spin_it.setMinimum(1)
        self.ui.spin_it.setMaximum(self.VISpar.Nit)
        self.ui.spin_it.setEnabled(self.VISpar.flagRun!=-2)
        if self.VISpar.type==0:
            dataType='Input'
            dataName=self.image_file if self.image is not None else None
        else:
            dataType='Output'
            dataName=self.result_file if self.result is not None else None
        if dataName: 
            self.ui.name_var.setText(f'{dataType} file: {os.path.basename(dataName)}')
        else:
            self.ui.name_var.setText(f'{dataType} file not available!')
        self.ui.name_var.setToolTip(f'{dataType} file: {dataName}')
        self.ui.name_var.setStatusTip(self.ui.name_var.toolTip()) 
        
        self.VISpar.colorMap=self.VISpar.vcolorMap[self.VISpar.variableKey]
        self.VISpar.vectorColor=self.VISpar.vvectorColor[self.VISpar.variableKey]

        self.ui.button_cmap.setIcon(QIcon(icons_path+'colormaps/'+self.VISpar.colorMap+'.png'))
        self.ui.button_cvec.setIcon(QIcon(icons_path+'colormaps/'+self.VISpar.vectorColor+'Vector.png'))

        self.setLevels()
        t=self.VISpar.type
        if (t==0 and self.VISpar.unit[t]) or (t==1 and not self.VISpar.unit[t]):
            self.xres,self.yres=self.getXYRes()
        else: self.xres=self.yres=1.0
        self.VISpar.xmin=self.VISpar.size[self.VISpar.type][0]*self.xres
        self.VISpar.xmax=self.VISpar.size[self.VISpar.type][1]*self.xres
        self.VISpar.ymin=self.VISpar.size[self.VISpar.type][2]*self.yres
        self.VISpar.ymax=self.VISpar.size[self.VISpar.type][3]*self.yres   
        return
    
    def setLevels(self):
        self.VISpar.min=self.VISpar.vmin[self.VISpar.variableKey]
        self.VISpar.max=self.VISpar.vmax[self.VISpar.variableKey]
        self.VISpar.mean=self.VISpar.vmean[self.VISpar.variableKey]
        self.VISpar.range=self.VISpar.vrange[self.VISpar.variableKey]
            
    def resetLevels(self):
        self.VISpar.vmin[self.VISpar.variableKey]=self.VISpar.vmin_default[self.VISpar.variableKey]
        self.VISpar.vmax[self.VISpar.variableKey]=self.VISpar.vmax_default[self.VISpar.variableKey]
        self.VISpar.vmean[self.VISpar.variableKey]=self.VISpar.vmean_default[self.VISpar.variableKey]
        self.VISpar.vrange[self.VISpar.variableKey]=self.VISpar.vrange_default[self.VISpar.variableKey]
        self.setLevels()

    def resetAllLevels(self):
        for field in ('min','max','mean','range'):
            v=getattr(self.VISpar,'v'+field)
            w=getattr(self.VISpar,'v'+field+'_default')
            for f in list(w):
                v[f]=w[f]
        self.setLevels()
    
    def resetXYLims(self):
        self.VISpar.size[self.VISpar.type][::]=self.VISpar.size_default[self.VISpar.type][::]
    
    def resetAllXYLims(self):
        for t in (0,1):
            self.VISpar.size[t][::]=self.VISpar.size_default[t][::]

    def readImageFile(self,filename):
        I=None
        if not filename: return filename, I
        try: 
            if os.path.exists(filename):
                pri.Info.cyan(f'Opening: {filename}  [<--{self.image_file}]')
                img=Image.open(filename)
                I=np.ascontiguousarray(img)
                self.nbits=img.getextrema()[1].bit_length()
                #I=transfIm(self.VISpar.Out,Images=[I])[0]
        except Exception as inst:
            pri.Error.red(f'Error opening image file: {filename}\n{traceback.print_exc()}\n{inst}')
            I=None
        return filename, I
    
    def getImageInfo(self):
        I=self.image
        mean=np.mean(I).item()
        std=np.std(I).item()
        #self.VISpar.vLim[self.namesPIV.img]=2**self.nbits
        self.VISpar.vLim[self.namesPIV.img]=min([2*I.max().item(),2**(self.nbits+1)])
        self.VISpar.vmin_default[self.namesPIV.img]=np.round(max([mean-2*std,0])).item()
        self.VISpar.vmax_default[self.namesPIV.img]=np.round(min([mean+2*std,self.VISpar.vLim[self.namesPIV.img]])).item()
        self.VISpar.vmean_default[self.namesPIV.img]=0.5*(self.VISpar.vmin_default[self.namesPIV.img]+self.VISpar.vmax_default[self.namesPIV.img])
        self.VISpar.vrange_default[self.namesPIV.img]=self.VISpar.vmax_default[self.namesPIV.img]-self.VISpar.vmin_default[self.namesPIV.img]
        self.VISpar.size_default[0]=[0,np.size(I,1),0,np.size(I,0),1]
        if self.namesPIV.img not in self.VISpar.vcolorMap:
            self.VISpar.vcolorMap[self.namesPIV.img]='gray'
        if self.namesPIV.img not in self.VISpar.vvectorColor:
            self.VISpar.vvectorColor[self.namesPIV.img]='green'

    def readResultFile(self,filename):
        res=None
        if not filename: return filename, res
        try: 
            if os.path.exists(filename):
                pri.Info.cyan(f'Opening: {filename} [<--{self.result_file}]')
                ext=os.path.splitext(filename)[-1]
                if ext=='.mat':
                    res = scipy.io.loadmat(filename)
                elif ext=='.plt':
                    tres = readPlt(filename)
                    res={}                                
                    for j, n in enumerate(tres[1]):
                        res[n]=tres[0][:,:,j]
                if "U" in res and "V" in res:
                    if "W" in res:
                        res["Mod"]=np.sqrt(res["U"]**2+res["V"]**2++res["W"]**2)
                    else:
                        res["Mod"]=np.sqrt(res["U"]**2+res["V"]**2)
                for f in list(res):
                    if not f in self.namesPIV.allFields: del res[f]
        except Exception as inst:
            pri.Error.red(f'Error opening image file: {filename}\n{traceback.print_exc()}\n{inst}')
            res=None
        return filename, res

    def getResultInfo(self):
        res=self.result
        for i in list(self.VISpar.vmin_default):
            if i!=self.namesPIV.img:
                del self.VISpar.vmin_default[i]
                del self.VISpar.vmax_default[i]
                del self.VISpar.vmean_default[i]
                del self.VISpar.vrange_default[i]
                del self.VISpar.vLim[i]

        for f in list(res):
            V:np=res[f]
            m=np.mean(V).item()
            r=np.std(V).item()
            self.VISpar.vLim[f]=max([m+5*r,abs(m-5*r)])
            if self.VISpar.vLim[f]<0.1: self.VISpar.vLim[f]=1
            self.VISpar.vmin_default[f]=np.round(m-2*r).item()
            self.VISpar.vmax_default[f]=np.round(m+2*r).item()
            self.VISpar.vmean_default[f]=0.5*(self.VISpar.vmin_default[f]+self.VISpar.vmax_default[f])
            self.VISpar.vrange_default[f]=self.VISpar.vmax_default[f]-self.VISpar.vmin_default[f]
            if f not in self.VISpar.vcolorMap:
                self.VISpar.vcolorMap[f]='jet'
            if f not in self.VISpar.vvectorColor:
                self.VISpar.vvectorColor[f]='black'
            pass
            
        FlagSize=False
        if "X" in list(res) and "Y" in list(res): 
            X=res["X"]
            Y=res["Y"]
            FlagSize=True
        elif "x" in list(res) and "y" in list(res): 
            X=res["x"]
            Y=res["y"]
            FlagSize=True
        if FlagSize:
            if np.size(X) and np.size(Y):
                self.VISpar.size_default[1]=[X.min().item(),X.max().item(),Y.min().item(),Y.max().item(),int(max([np.size(X,0),np.size(X,1)])/4)]
        else:
            self.VISpar.size_default[1]=[0,1,0,1,1]
       
        
#*************************************************** Plot tools
#******************** Actions
    def button_view_action(self):
        self.VISpar.FlagView=self.ui.button_view.isChecked()

    def button_ShowIW_action(self):
        self.VISpar.FlagShowIW=self.ui.button_ShowIW.isChecked()
        self.resetXYLims()
    
    def button_SubMIN_action(self):
        self.VISpar.FlagSubMIN=self.ui.button_SubMIN.isChecked()
    
    def button_ShowCR_action(self):
        self.VISpar.FlagShowCR=self.ui.button_ShowCR.isChecked()

    def button_unit_action(self):
        self.VISpar.unit[self.VISpar.type]=self.ui.button_unit.isChecked()

    def button_Contourf_action(self):
        self.VISpar.FlagContourf=self.ui.button_Contourf.isChecked()
    
    def button_cmap_action(self):
        # Show the popup menu
        self.colorMapMenu.exec(self.ui.button_cmap.mapToGlobal(self.ui.button_cmap.rect().bottomLeft()))

    def button_cvec_action(self):
        # Show the popup menu
        self.vectorColorMenu.exec(self.ui.button_cvec.mapToGlobal(self.ui.button_cvec.rect().bottomLeft()))

    def combo_map_var_action(self):
        self.VISpar.variable=self.ui.combo_map_var.currentText()
        self.VISpar.variableKey=self.namesPIV.combo_dict_keys[self.VISpar.variable]
        self.VISpar.type=int(self.VISpar.variable!=self.namesPIV.combo_dict[self.namesPIV.img])
        self.setLevels()
    
    def button_automatic_levels_action(self):
        VISpar.FlagAutoLevels=self.ui.button_automatic_levels.isChecked()
        return True
    
    def button_automatic_sizes_action(self):
        VISpar.FlagAutoSizes=self.ui.button_automatic_sizes.isChecked()
        return True
    
    def button_restore_action(self):
        self.resetLevels()

    def button_resize_action(self):
        self.resetXYLims()

    def button_invert_y_action(self):
        self.VISpar.FlagYInvert[self.VISpar.type]=self.ui.button_invert_y.isChecked()

    def spinLevels_action(self,spin:MyQDoubleSpin):
        n=spin.objectName().replace('spin_','')
        spin_value=getattr(self.VISpar,n)

        v=getattr(self.VISpar,'v'+n)
        v[self.VISpar.variableKey]=spin_value
        self.adjustSpins(spin)

    def adjustSpins(self,spin:MyQDoubleSpin):
        nspin=spin.objectName().replace('spin_','')
        if spin in (self.ui.spin_min,self.ui.spin_max):            
            if spin==self.ui.spin_min and spin.value()>=self.ui.spin_max.value():
                self.VISpar.max=self.VISpar.min+self.ui.spin_range.minimum()
            elif spin==self.ui.spin_max and spin.value()<=self.ui.spin_min.value():
                self.VISpar.min=self.VISpar.max-self.ui.spin_range.minimum()
            self.VISpar.mean=0.5*(self.VISpar.min+self.VISpar.max)
            self.VISpar.range=self.VISpar.max-self.VISpar.min
        elif spin in (self.ui.spin_mean,self.ui.spin_range):
            m=self.ui.spin_mean.value()
            r=self.ui.spin_range.value()
            if m-r*0.5<self.ui.spin_min.minimum():
                self.VISpar.min=self.ui.spin_min.minimum()
                if spin==self.ui.spin_mean:
                    self.VISpar.range=2*(m-self.VISpar.min)
                    self.VISpar.max=m+0.5*self.VISpar.range
                else:
                    self.VISpar.max=self.VISpar.min+r
                    self.VISpar.mean=0.5*(self.VISpar.min+self.VISpar.max)
            elif m+r*0.5>self.ui.spin_max.maximum():
                self.VISpar.max=self.ui.spin_max.maximum()
                if spin==self.ui.spin_mean:
                    self.VISpar.range=2*(self.VISpar.max-m)
                    self.VISpar.min=m-0.5*self.VISpar.range
                else:
                    self.VISpar.min=self.VISpar.max-r
                    self.VISpar.mean=0.5*(self.VISpar.min+self.VISpar.max)
            else:
                self.VISpar.max=m+0.5*r
                self.VISpar.min=m-0.5*r
                if spin==self.ui.spin_mean: self.VISpar.range=(self.VISpar.max-self.VISpar.min)
                else:  self.VISpar.mean=0.5*(self.VISpar.min+self.VISpar.max)

        for n in ['min','max','mean','range']:
            if n!=nspin:
                spin=getattr(self.ui,'spin_'+n)
                slider=getattr(self.ui,'slider_'+n)
                val=getattr(self.VISpar,n)
                spin.setValue(val)
                self.slider_set(spin,slider)
    
    def sliderLevels_changing(self,spin:MyQDoubleSpin,slider:QSlider,Flag=False):
        self.setSpinFromSlider(spin,slider)
        self.adjustSpins(spin)
        self.sliderLevels_action()
        return Flag

    def setSpinFromSlider(self,spin:MyQDoubleSpin,slider:QSlider):
        slider_value=slider.value()
        spin_value=spin.minimum()+(spin.maximum()-spin.minimum())/slider.maximum()*slider_value
        spin.setValue(spin_value)
        n=spin.objectName().replace('spin_','')
        if n in ('nclev','vecspac'): 
            spin_value=int(spin_value)
        setattr(self.VISpar,n,spin_value)
        return spin_value

    def sliderLevels_action(self):
        for n in ('min','max','mean','range'):
            spin_value=getattr(self.VISpar,n)
            v=getattr(self.VISpar,'v'+n)
            v[self.VISpar.variableKey]=spin_value
                      
    def spinFieldRep_action(self,spin:MyQDoubleSpin):
        n=spin.objectName().replace('spin_','')
        spin_value=getattr(self.VISpar,n)
        if n in ('nclev','vecspac'): spin_value=int(spin_value)
        setattr(self.VISpar,n,spin_value)
    
    def sliderFieldRep_changing(self,spin:MyQDoubleSpin,slider:QSlider,Flag=False):
        self.setSpinFromSlider(spin,slider)
        self.sliderFieldRep_action()
        return Flag
    
    def sliderFieldRep_action(self):
        return
    
    def spin_xy_action(self,spin,k):
        n=spin.objectName().replace('spin_','')
        spin_value=getattr(self.VISpar,n)
        res=self.xres if k<2 else self.yres
        self.VISpar.size[self.VISpar.type][k]=spin_value/res
        
 #******************** Settings
    def button_view_set(self):
        self.ui.button_view.setChecked(self.VISpar.FlagView)

    def button_ShowIW_set(self):
        self.ui.button_ShowIW.setChecked(self.VISpar.FlagShowIW)

    def button_ShowCR_set(self):
        self.ui.button_ShowCR.setChecked(self.VISpar.FlagShowCR)

    def button_SubMIN_set(self):
        self.ui.button_SubMIN.setChecked(self.VISpar.FlagSubMIN)
    
    def button_unit_set(self):
        self.ui.button_unit.setChecked(self.VISpar.unit[self.VISpar.type])

    def button_Contourf_set(self):
        self.ui.button_Contourf.setChecked(self.VISpar.FlagContourf)
    
    def button_automatic_levels_set(self):
        self.ui.button_automatic_levels.setChecked(VISpar.FlagAutoLevels)

    def button_automatic_sizes_set(self):
        self.ui.button_automatic_sizes.setChecked(VISpar.FlagAutoSizes)

    def button_invert_y_set(self):
        self.ui.button_invert_y.setChecked(self.VISpar.FlagYInvert[self.VISpar.type])

    def combo_map_var_set(self):
        self.ui.combo_map_var.setCurrentText(self.VISpar.variable)

    def slider_set(self,spin:MyQDoubleSpin,slider:QSlider):
        spin_value=getattr(self.VISpar,spin.objectName().replace('spin_',''))
        if spin.maximum()>spin.minimum():
            slider_value=int((spin_value-spin.minimum())/(spin.maximum()-spin.minimum())*slider.maximum())
        else: slider_value=0
        slider.setValue(slider_value)

 #******************** Layout
    def leftrightCallback(self,di):
        i=self.ui.image_levels.currentIndex()
        i=i+di
        c=self.ui.image_levels.count()-1-int(self.result is None)
        if i<0: i=c
        elif i>c: i=0
        self.VISpar.setPage=i
 
 #*************************************************** Plot
    def updatingPlot(self):
        xmin,xmax=list(self.ui.plot.axes.get_xlim())
        ymin,ymax=list(self.ui.plot.axes.get_ylim())
        self.VISpar.size[self.VISpar.type][:2]=[xmin/self.xres,xmax/self.xres]
        self.VISpar.size[self.VISpar.type][2:4]=[ymin/self.yres,ymax/self.yres]
        
    def brushCursor(self):
        if self.FlagNormalCursor:
            self.FlagNormalCursor=False
            QApplication.setOverrideCursor(self.brush_cursor) 
            def restoreCursor():
                QApplication.restoreOverrideCursor()
                self.FlagNormalCursor=True
            QTimer.singleShot(250,lambda: restoreCursor())

    def setMapVar(self):    
        pri.PlotTime.magenta(f'{"/"*25} Plotting image - start')
        self.brushCursor()
        try:
            if self.VISpar.type==0:
                fields=['image_file','variable','unit','FlagSubMIN','Out','colorMap']
                img=self.image
                if self.VISpar.img and self.VISpar.FlagSubMIN and self.image_Min is not None:
                    img=img-self.image_Min
                self.img=img
                FlagDraw=self.showImg(fields)

                FlagIW=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['FlagShowIW','Pro'])
                if FlagIW or FlagDraw: self.showRect()
                FlagDraw=FlagDraw or FlagIW
            else:
                if self.orect: self.cleanRect()
                fields=['result_file','variable','unit','min','max','nclev','FlagContourf','colorMap']
                if not self.VISpar.FlagContourf:    
                    self.img=self.calcMap(self.result[self.VISpar.variableKey])
                    FlagDraw=self.showImg(fields)
                else:
                    FlagDraw=self.showMap(fields)
            fields=['result_file','variable','FlagContourf','field_rep','unit','vectorColor']
            if self.VISpar.field_rep==1: fields+=['vecsize','vecspac']
            elif self.VISpar.field_rep==2: fields+=['streamdens']
            FlagVecField=self.VISpar.isDifferentFrom(self.VISpar_old,fields=fields)
            if FlagVecField and self.result: 
                self.showVecField()
            FlagDraw=FlagDraw or FlagVecField
            
            if self.image is not None and self.VISpar.FlagShowCR:
                self.showCommonRegion()
                FlagDraw=FlagDraw or self.CR is not None
            if FlagDraw: 
                #self.ui.plot.draw()  
                self.ui.plot.draw_idle() 
        except:
            printException()
        #self.exitVISerr(False)  
        pri.PlotTime.magenta(f'{"%"*25} Plotting image - end')

    def showImg(self,fields):
        img=self.img
        if img is None: 
            self.cleanAxes(FlagAxis=False)
            return True #raise Exception('Invalid input image!')
        
        FlagNewPlot=self.VISpar.isDifferentFrom(self.VISpar_old,fields=fields)
        FlagOut=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['Out'])
        FlagXLim=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['xmin','xmax','ymin','ymax','unit','FlagYInvert','Out'])
        FlagCMap=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['colorMap','nclev'])
        FlagCLim=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['min','max','nclev','colorMap'] if self.VISpar.type else ['min','max'])
        FlagExtent=False
        
        if FlagNewPlot:
            FlagVariable=self.VISpar_old.variable!=self.VISpar.variable    

            if self.imgshow is None or self.VISpar_old.FlagContourf!=self.VISpar.FlagContourf or FlagOut:
                self.cleanAxes()
                self.imgshow=self.ui.plot.axes.imshow(img,extent=self.imgExtent(), origin='lower', vmin=self.VISpar.min,vmax=self.VISpar.max,zorder=0)
                cmap,_=self.colorMap()
                self.imgshow.set_cmap(cmap)
                divider = make_axes_locatable(self.ui.plot.axes)
                cax = divider.append_axes("right", size="5%", pad=0.05) 
                self.cb=self.ui.plot.fig.colorbar(self.imgshow,cax=cax) 
                self.setTitleLabels()
            else: 
                self.imgshow.set_data(img)
                extent=self.imgExtent()
                if extent!=self.imgshow.get_extent():
                    self.imgshow.set_extent(extent)
                    FlagExtent=True
                if FlagCMap:
                    cmap,_=self.colorMap()
                    self.imgshow.set_cmap(cmap)
                if FlagCLim:
                    self.imgshow.set_clim(self.VISpar.min,self.VISpar.max)
                if FlagVariable:
                    self.setTitleLabels()
        else:
            if FlagCMap:
                cmap,_=self.colorMap()
                self.imgshow.set_cmap(cmap)
            if FlagCLim:
                self.imgshow.set_clim(self.VISpar.min,self.VISpar.max)
        if FlagXLim:
            self.setAxisLim()
        self.Ptoolbar.update()

        FlagDraw=FlagNewPlot or FlagOut or FlagXLim or FlagCMap or FlagCLim or FlagExtent
        return FlagDraw

    def colorMap(self):
        if self.VISpar.type==0:
            cmap=mpl.colormaps[self.VISpar.colorMap]
            levs=np.linspace(self.VISpar.min,self.VISpar.max,int(self.VISpar.max-self.VISpar.min))
        else:
            if self.VISpar.min<self.VISpar.max:
                levs=np.linspace(self.VISpar.min,self.VISpar.max,self.VISpar.nclev)
            else:
                levs=np.linspace(self.VISpar.max-self.ui.spin_min.singleStep(),\
                    self.VISpar.max,self.VISpar.nclev) 
            colormap = pyplt.get_cmap(self.VISpar.colorMap)
            colors=colormap(np.linspace(0, 1, len(levs)))
            cmap = mpl.colors.ListedColormap(colors)   
        return cmap, levs
    
    def getXYRes(self,type=None):
        if not type: type=self.VISpar.type
        xres=yres=1.0 
        if self.VISpar.Process==ProcessTypes.piv and not self.VISpar.Out.FlagNone:
            if type==0: #mm/pixels
                xres     =1.0/self.VISpar.Out.xres
                yres=1.0/(self.VISpar.Out.xres*self.VISpar.Out.pixAR)
            elif type==1: #pixels/mm
                xres=self.VISpar.Out.xres
                yres=self.VISpar.Out.xres*self.VISpar.Out.pixAR
        return xres, yres
    
    def imgExtent(self):
        size=self.VISpar.size_default[self.VISpar.type]
        return [k*self.xres for k in size[:2]]+[k*self.yres for k in size[2:4]]
    
    def setAxisLim(self):
        self.ui.plot.axes.set_xlim(self.VISpar.xmin,self.VISpar.xmax)
        ylim=[self.VISpar.ymin,self.VISpar.ymax]
        if self.VISpar.FlagYInvert[self.VISpar.type]: 
            self.ui.plot.axes.set_ylim(max(ylim),min(ylim))
        else:
            self.ui.plot.axes.set_ylim(min(ylim),max(ylim))
        self.ui.plot.axes.set_aspect('equal', adjustable='box')
    
    def setTitleLabels(self):
        self.ui.plot.axes.set_title(self.namesPIV.titles_dict[self.VISpar.variableKey])
        self.cb.ax.set_title(self.namesPIV.titles_cb_dict[self.VISpar.variableKey])
        self.ui.plot.axes.set_xlabel("x" if self.VISpar.type else "")
        self.ui.plot.axes.set_ylabel("y" if self.VISpar.type else "")
        
    def showMap(self,fields):
        result=self.result
        if result is None:
            self.cleanAxes(FlagAxis=False)
            return True #raise Exception('Invalid output image!')
        
        FlagNewPlot=self.VISpar.isDifferentFrom(self.VISpar_old,fields=fields)
        FlagXLim=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['xmin','xmax','ymin','ymax','unit','FlagYInvert','Out'])
        FlagCMap=self.VISpar_old.colorMap!=self.VISpar.colorMap
        FlagCLim=self.VISpar.isDifferentFrom(self.VISpar_old,fields=['min','max'])

        if FlagNewPlot or self.VISpar_old.nclev!=self.VISpar.nclev:
            if not self.VISpar.unit[self.VISpar.type]:
                xres,yres=self.getXYRes(type=1)
            else: xres=yres=1.0
            X=result[self.namesPIV.x]*xres
            Y=result[self.namesPIV.y]*yres
            V=result[self.VISpar.variableKey]
            self.map=V
           
            
            if self.contour: 
                for coll in self.contour.collections:
                    coll.remove()
            cmap,levs=self.colorMap()
            self.contour=self.ui.plot.axes.contourf(X, Y, V, levs, \
                cmap=cmap, origin='lower', extend='both', zorder=0)
            self.contour.set_clim(levs[0],levs[-1])
            if self.cb is None:
                divider = make_axes_locatable(self.ui.plot.axes)
                cax = divider.append_axes("right", size="5%", pad=0.05) 
                self.cb=self.ui.plot.fig.colorbar(self.contour,cax=cax) 
            self.setTitleLabels()
        else:
            if FlagCMap:
                cmap,_=self.colorMap()
                self.contour.set_cmap(cmap)
            if FlagCLim:
                self.contour.set_clim(self.VISpar.min,self.VISpar.max)
            if FlagXLim:
                self.setAxisLim()
            self.Ptoolbar.update()

        FlagDraw=FlagNewPlot or FlagXLim or FlagCMap or FlagCLim
        return FlagDraw
    
    def calcMap(self,V):
        #size_pixels=self.ui.plot.fig.get_size_inches()*self.ui.plot.fig.get_dpi()
        #size_pixels=np.minimum(np.round(0.5*size_pixels).astype(int),1000)
        size_pixels=[1000]*2
        FlagSize=False
        if "X" in list(self.result) and "Y" in list(self.result):
            X=self.result["X"]
            Y=self.result["Y"]
            FlagSize=True
        elif "x" in list(self.result) and "y" in list(self.result):
            X=self.result["x"]
            Y=self.result["y"]
            FlagSize=True
        if FlagSize:
            xmin,xmax,ymin,ymax=[X.min(),X.max(),Y.min(),Y.max()]
        else:
            xmin,xmax,ymin,ymax=[0,np.size(V,1),0,np.size(V,0)]
        x = np.linspace(xmin,xmax, np.size(V,1))  
        y = np.linspace(ymin,ymax, np.size(V,0))
        if np.size(V,1)<size_pixels[1] or np.size(V,0)<size_pixels[0]:
            f = scipy.interpolate.RectBivariateSpline(y, x, V)
            x_new = np.linspace(xmin,xmax, size_pixels[0]) 
            y_new = np.linspace(ymin,ymax, size_pixels[1])
            V = f(y_new, x_new)
        return V

    def showVecField(self):
        ind=self.VISpar.field_rep
        if self.qui!=None:
            self.qui.remove()  
            self.qui=None
        if self.stream is not None:
            self.stream.lines.remove()
            for ax in self.ui.plot.axes.get_children():
                if isinstance(ax, mpl.patches.FancyArrowPatch):
                    ax.remove()      
            self.stream=None 
        if ind in (1,2):
            if not self.VISpar.unit[self.VISpar.type]:
                xres,yres=self.getXYRes(type=1)
            else: xres=yres=1.0
            if self.namesPIV.x in self.result and self.namesPIV.y in self.result:
                X=self.result[self.namesPIV.x]*xres
                Y=self.result[self.namesPIV.y]*yres
            elif self.namesPIV.X in self.result and self.namesPIV.Y in self.result:
                X=self.result[self.namesPIV.X]*xres
                Y=self.result[self.namesPIV.Y]*yres
            U=self.result[self.namesPIV.u]
            V=self.result[self.namesPIV.v]
            Mod=np.sqrt(U**2+V**2)
            if ind==1:
                dX=np.sqrt((X[0,1]-X[0,0])**2+(Y[1,0]-Y[0,0])**2)   
                dW=[X.max()-X.min(),Y.max()-Y.min()]          
                if self.VISpar_old.field_rep!=self.VISpar.field_rep:
                    size_pixels=self.ui.plot.fig.get_size_inches()*self.ui.plot.fig.get_dpi()*self.ui.plot.axes.get_position().bounds[2:]
                    spaPixels=dX*size_pixels/dW
                    fac_spa=np.max(nPixelsPerVector/spaPixels).astype(int).item()
                    spa=self.VISpar.vecspac=max([1,fac_spa])
                    vecsize=self.VISpar.vecsize=1.5
                    self.ui.spin_vecspac.setValue(spa)
                    self.ui.spin_vecsize.setValue(vecsize)
                else:           
                    spa=self.VISpar.vecspac
                    vecsize=self.VISpar.vecsize
                fac=dX*vecsize*spa
                Modq= Mod[::spa,::spa]
                Uq=np.divide(U[::spa,::spa], Modq, where=Modq!=0)*fac
                Vq=np.divide(V[::spa,::spa], Modq, where=Modq!=0)*fac
                w=0.15*fac
                wmax=0.02*min([X.max()-X.min(),Y.max()-Y.min()])
                qwidth=min([w,wmax])
                hwidth=4 if vecsize<4 else vecsize
                self.qui=self.ui.plot.axes.quiver(
                    X[::spa,::spa],Y[::spa,::spa],Uq,Vq, color=VIS_VectorColors[self.VISpar.vectorColor], clip_on=True,
                    angles='xy',scale_units='xy',scale=1.0,
                    units='xy',width=qwidth,headwidth=hwidth,headlength=1.25*hwidth,headaxislength=0.75*hwidth,zorder=10)
            elif ind==2:
                self.stream=self.ui.plot.axes.streamplot(X,Y,U,V,color=VIS_VectorColors[self.VISpar.vectorColor],density=self.VISpar.streamdens,zorder=10)

    def cleanAxes(self,FlagAxis=True):
        self.imgshow=self.contour=None 
        self.ui.plot.axes.cla()
        if self.cb: 
            try:
                self.cb.remove()
            except:
                pass
            self.cb=None
        self.ui.plot.axes.axis('on' if FlagAxis else 'off')
        #self.ui.Plot_tools.setEnabled(FlagAxis)

    def cleanRect(self):
        if len(self.orect):
            for r in self.orect: 
                if type(r)==list:
                    for s in r:
                        try: s.remove()
                        except:  pass
                else:
                    try: r.remove()
                    except: pass

    def showRect(self):
        if not len(self.VISpar.Pro.Vect): return
        self.cleanRect()
        if not self.VISpar.FlagShowIW: return
        colors='rgbymc'
        lwidth=1
        nov_hor=3
        nov_vert=3

        H=self.VISpar.size[self.VISpar.type][1]
        ve=self.VISpar.Pro.Vect if isinstance(self.VISpar.Pro.Vect[0],list) else [[v] for v in self.VISpar.Pro.Vect] 
        Vect = [[val for val in v] for v  in ve]
        dxin=dyin=5
        if self.VISpar.unit[self.VISpar.type]:
            xres,yres=self.getXYRes(type=0)
            for k in range(2): Vect[k]=[val*xres for val in Vect[k]]
            for k in range(2,4): Vect[k]=[val*yres for val in Vect[k]]
            dxin=dxin*xres
            dyin=dyin*yres
        nw=len(Vect[0])
        xin0=yin0=0
        xmax=ymax=0
        xlim_min=ylim_min=float('inf')
        xlim_max=ylim_max=-float('inf')
        self.orect=[]
        for k in range(nw):
            if self.VISpar.Pro.FlagBordo:
                if not xin0: dx=-Vect[0][k]/2+Vect[1][k]
                else: dx=0
                if not yin0: dy=-Vect[2][k]/2+Vect[3][k]
                else: dy=0
            else:
                dx=dy=0
            for i in range(nov_vert):
                yin=yin0+i*Vect[3][k]+dy
                ylim_min=min([ylim_min,yin])
                for j in range(nov_hor):
                    xin=xin0+j*Vect[1][k]+dx
                    xlim_min=min([xlim_min,xin])
                    kk=i+j*nov_vert
                    if kk%2: lst=':'
                    else: lst='-'
                    kc=k%len(colors)
                    rect = mpl.patches.Rectangle((xin, yin), Vect[0][k], Vect[2][k],\
                        linewidth=lwidth, edgecolor=colors[kc], facecolor=colors[kc],\
                            alpha=0.25,linestyle=lst)
                    self.ui.plot.axes.add_patch(rect)
                    rect2 = mpl.patches.Rectangle((xin, yin), Vect[0][k], Vect[2][k],\
                        linewidth=lwidth, edgecolor=colors[kc], facecolor='none',\
                            alpha=1,linestyle=lst)
                    self.ui.plot.axes.add_patch(rect2)
                    points=self.ui.plot.axes.plot(xin+ Vect[0][k]/2,yin+ Vect[2][k]/2,\
                        'o',color=colors[kc])
                    if not kk: 
                        if self.VISpar.FlagYInvert[self.VISpar.type]: va='top'
                        else: va='bottom'
                        text=self.ui.plot.axes.text(xin+dxin,yin+dyin,str(k),\
                        horizontalalignment='left',verticalalignment=va,\
                        fontsize='large',color='w',fontweight='bold')
                    self.orect=self.orect+[rect,rect2,points,text]
            xmaxk=xin+Vect[0][k]
            ymaxk=yin+Vect[2][k]
            xlim_max=max([xlim_max,xmaxk])
            ylim_max=max([ylim_max,ymaxk])
            if xmaxk>xmax: xmax=xmaxk
            if ymaxk>ymax: ymax=ymaxk
            if k==nw-1: continue
            if ymaxk+Vect[2][k+1]+(nov_vert-1)*Vect[3][k+1]<H:
                yin0=ymaxk
            else:
                yin0=0
                xin0=xmax
        xlim=self.ui.plot.axes.get_xlim()
        xlim_min=min([xlim[0],xlim_min])
        xlim_max=max([xlim[1],xlim_max])
        self.ui.plot.axes.set_xlim(xlim_min,xlim_max)
        if self.VISpar.FlagYInvert[self.VISpar.type]: 
            ylim=self.ui.plot.axes.get_ylim()
            ylim_max=min([ylim[1],ylim_min])
            ylim_min=max([ylim[0],ylim_max])
        else:
            ylim=self.ui.plot.axes.get_ylim()
            ylim_min=min([ylim[0],ylim_min])
            ylim_max=max([ylim[1],ylim_max])
        self.ui.plot.axes.set_ylim(ylim_min,ylim_max)
        self.VISpar.xmin,self.VISpar.xmax=list(self.ui.plot.axes.get_xlim())
        self.VISpar.ymin,self.VISpar.ymax=list(self.ui.plot.axes.get_ylim())

    def showCommonRegion(self):
        if self.CR:
            self.CR.remove()
            self.CR=None

        try:
            mapFun=PaIRS_lib.MappingFunction() 
            mapFun.readCal(self.VISpar.calList)
            if self.VISpar.Step==StepTypes.spiv:
                planeConst=self.readLaserPlaneConst(self.VISpar.dispFile)
            else:
                planeConst=[0.0,0.0,0.0]
            o=self.VISpar.Out
            points=[ [o.x_min, o.y_min], [o.x_max, o.y_min], [o.x_max, o.y_max], [o.x_min, o.y_max]]
            zLaser=lambda xy: self.zLaser(xy[0],xy[1],planeConst)
            for p in points: p.append(zLaser(p))
            points_array=np.array(points,dtype=np.float64,order='C')
            cam=self.VISpar.cam-1
            X=mapFun.worldToImg(points_array,cam,None)# In output X1 is equal to X if correctly allocated
            
            x_values = [Xp[0] for Xp in X]+[X[0][0]]
            y_values = [Xp[1] for Xp in X]+[X[0][1]]
            self.CR,=self.ui.plot.axes.plot(x_values, y_values, 'b-',clip_on=False)
        except Exception as exc:
            pri.Error.red(f"[VIS] Error while plotting common zone!\n{traceback.format_exc()}\n")
        return

    def zLaser(self,x,y,planeConst):
        return planeConst[0]+planeConst[1]*x+planeConst[2]*y
    
    def readLaserPlaneConst(self, filename: str):
        try:
            with open(filename, "r") as cfg:
                lines = cfg.readlines()
                if len(lines) < 6:
                    raise ValueError("Il file non contiene abbastanza righe per essere valido")
                planeConst = [
                    float(lines[3].strip().rstrip(',')),
                    float(lines[4].strip().rstrip(',')),
                    float(lines[5].strip().rstrip(','))
                ]
                return planeConst
        
        except Exception as inst:
            errorPrint = f"\n!!!!!!!!!! Error while reading the file:\n{str(inst)}\n"
            return [0.0,0.0,0.0]
        
    """
    def getZonaCom(self,c:int):
        return (min (self.disp.vect.Xinf[c],self.disp.vect.Xsup[c]),
                min (self.disp.vect.Yinf[c],self.disp.vect.Ysup[c]),
                max (self.disp.vect.Xinf[c],self.disp.vect.Xsup[c]),
                max (self.disp.vect.Yinf[c],self.disp.vect.Ysup[c]))  
    """

#*************************************************** Menus
    def contextMenuEvent(self, event):   
        contextMenu = QMenu(self)
        copy2clipboard = contextMenu.addAction("Copy to clipboard ("+self.QS_copy2clipboard.key().toString(QKeySequence.NativeText)+")")
        copy2newfig = contextMenu.addAction("Open in new figure ("+self.QS_copy2newfig.key().toString(QKeySequence.NativeText)+")")
        contextMenu.addSeparator()
        if len(self.ui.plot.fig2)>1:
            showAll = contextMenu.addAction("Show all")
            closeAll = contextMenu.addAction("Close all")
            alignAll = contextMenu.addAction("Align all")
            contextMenu.addSeparator()
        else:
            showAll = None 
            closeAll= None
            alignAll= None
        loadImg = contextMenu.addAction("Load image")
        loadRes = contextMenu.addAction("Load result")

        action = contextMenu.exec(self.mapToGlobal(event.pos()))
        if action == copy2clipboard:
            self.ui.plot.copy2clipboard()
        elif action == copy2newfig:
            self.ui.plot.copy2newfig(self.ui.name_var.toolTip())
        elif action == showAll:
            self.ui.plot.showAll()
        elif action == closeAll:
            self.ui.plot.closeAll()
        elif action == alignAll:
            self.ui.plot.alignAll()
        elif action == loadImg:
            self.load_Img_callback()
        elif action == loadRes:
            self.load_Res_callback()

    def loadImg(self,filename=None):
        if filename is None:
            filename, _ = QFileDialog.getOpenFileName(self,\
                "Select an image file of the sequence", filter=text_filter,\
                    options=optionNativeDialog)
        else:
            if os.path.exists(filename): filename=None
        if filename:
            self.image_file_Load=filename
            self.image_raw=None
            self.image=None

            self.ui.spin_img.setMinimum(-1)
            self.VISpar.img=-1
            self.VISpar.type=0
            self.VISpar.variable=self.namesPIV.combo_dict[self.namesPIV.img]
            self.VISpar.variableKey=self.namesPIV.combo_dict_keys[self.VISpar.variable]

            self.FlagResetLevels=self.FlagResetSizes=True
            self.cleanAxes()
    
    def loadRes(self):
        filename, _ = QFileDialog.getOpenFileName(self,\
            "Select an image file of the sequence", filter="All files (*.mat *.plt);; .mat (*.mat);; .plt (*.plt)",\
                options=optionNativeDialog)
        if filename:
            self.result_file_Load=filename
            self.result=None
            self.ui.spin_img.setMinimum(-1)
            self.VISpar.img=-1
            self.VISpar.variable=self.namesPIV.combo_dict[self.namesPIV.Mod]
            self.VISpar.variableKey=self.namesPIV.combo_dict_keys[self.VISpar.variable]
            self.FlagResetLevels=self.FlagResetSizes=True
            self.VISpar.type=1
            self.cleanAxes()

def create_colormap_image(colormap, width, height, FlagVerticalColormap, imgMapPath):
    # Create an empty image
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Get the Matplotlib colormap
    cmap = plt.get_cmap(colormap)
    # Calculate the colors of the colormap and assign them to the image
    for y in range(height):
        for x in range(width):
            if FlagVerticalColormap:
                normalized_y = (height-y)/ height
                color = cmap(normalized_y)
            else:
                normalized_x = x / width
                color = cmap(normalized_x)
            img[y, x] = [int(c * 255) for c in color[:3]]  # Convert colors to range 0-255
    plt.imsave(imgMapPath, img)
    pixmap=numpy_to_qpixmap(img)
    return pixmap

def numpy_to_qpixmap(img):
    height, width, channel = img.shape
    bytes_per_line = 3 * width
    qimage = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
    qpixmap = QPixmap.fromImage(qimage)
    return qpixmap

def create_arrow_pixmap(rgb_color, width, height, path):
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    ax.axis('off')

    # Calcola la posizione e la direzione della freccia
    x = width / 8
    y = height / 2
    u = width *3/4
    v = 0

    # Disegna la freccia con quiver
    ax.quiver(x, y, u, v, color=rgb_color, angles='xy', scale_units='xy', scale=1, width=0.002*width, headwidth=5, headlength=5,headaxislength=3)

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)

    # Salva l'immagine in un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig)
    buf.seek(0)

    image = Image.open(buf)
    image.save(path)
    pixmap=QPixmap(path)
    return pixmap

        
if __name__ == "__main__":
    import sys
    app=QApplication.instance()
    if not app:app = QApplication(sys.argv)
    app.setStyle('Fusion')
    object = Vis_Tab(None)
    object.show()
    app.exec()
    app.quit()
    app=None



