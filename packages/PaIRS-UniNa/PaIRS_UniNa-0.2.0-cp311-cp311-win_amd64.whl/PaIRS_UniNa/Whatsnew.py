from .PaIRS_pypacks import*
from .ui_Whatsnew import Ui_Whatsnew
from .__init__ import __version__

#from TabTools import setupWid,setFontPixelSize,setFontSizeText
class Whatsnew(QMainWindow):
    def __init__(self,gui,Message='',title='',dfontPixelSize=0):
        super().__init__()
        ui=Ui_Whatsnew()
        ui.setupUi(self)
        self.ui=ui
        
        if Message:
            self.ui.info.setText(Message)
            self.ui.info.setWordWrap(True)
        if title:
            self.setWindowTitle(title)
        
        self.gui=gui
        fontPixelSize=self.gui.TABpar.fontPixelSize
        font=gui.font()
        font.setPixelSize(fontPixelSize+dfontPixelSize)
        header=Message.split('>')[1].split('<')[0]
        textSize0=QtGui.QFontMetrics(font).size(QtCore.Qt.TextFlag.TextSingleLine,header)
        w0=int(textSize0.width()*1.5)
        w=w0+self.ui.icon_label.width()+self.ui.mainLay.horizontalSpacing()+self.ui.mainLay.contentsMargins().left()+self.ui.mainLay.contentsMargins().right()

        font=gui.font()
        font.setPixelSize(fontPixelSize)
        for c in self.findChildren(QObject):
            if hasattr(c,'setFont'):
                c.setFont(font)
    
        self.show()
        self.resize(QSize(w,self.gui.maximumGeometry.height()))
        self.update()
        hinfo=self.ui.info.height()
        h=hinfo+self.ui.w_Ok.height()+self.ui.mainLay.verticalSpacing()+self.ui.mainLay.contentsMargins().bottom()*2+self.ui.mainLay.contentsMargins().top()*2
        self.setFixedSize(QSize(w,h))

        qr = self.frameGeometry()
        cp = self.gui.maximumGeometry.center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        self.ui.button_changes.clicked.connect(self.close)
        self.ui.button_changes.clicked.connect(self.gui.showChanges)
        self.ui.button_Ok.clicked.connect(self.close)

def whatsNew(self):
    if os.path.exists(fileWhatsNew[0]): 
        filename=fileWhatsNew[0]
    elif os.path.exists(fileWhatsNew[1]): 
        filename=fileWhatsNew[1]
    else: 
        pri.Info.blue('No information about the updates of the current version is available!\n')
        return
    try:
        file = open(filename, "rb")
        content = file.read().decode("utf-8")
        file.close()
    except Exception as inst:
        pri.Error.red(f'There was a problem while reading the file {filename}:\n{inst}')
    try:
        splittedContent=content.replace('\r','').replace('\n','').split('*')[1:]
        star='<span style="font-size:100%;color:#e2b112;">&#9733;</span>'  #⭐,&#9733;
        news='<br/><br/>'.join([star+'   '+c for c in splittedContent])
        dfontPixelSize=6
        fontPixelSize=self.TABpar.fontPixelSize-2+dfontPixelSize
        Message=f'<span style=" font-size: {fontPixelSize+dfontPixelSize}px; font-weight:600;">'+f"What's new in PaIRS-UniNa {__version__}"+'</span><br/><br/>'+news+'<br/><br/>Go to the menu "? -> Changes" for further information.'
        self.whatsnew=Whatsnew(self,Message,f'Updates of version {__version__}',dfontPixelSize)
        #warningDialog(self,Message,pixmap=''+ icons_path +'news.png',title=f'Updates of version {__version__}',flagRichText=True)
    except Exception as inst:
        pri.Error.red(f"There was a problem while launching the What's new dialog box:\n{inst}")
    if os.path.exists(fileWhatsNew[0]):
        try:
            if os.path.exists(fileWhatsNew[1]): os.remove(fileWhatsNew[1])
            os.rename(fileWhatsNew[0],fileWhatsNew[1])
        except Exception as inst:
            pri.Error.red(f'There was a problem while renaming the file {fileWhatsNew[0]}:\n{inst}')
    return
