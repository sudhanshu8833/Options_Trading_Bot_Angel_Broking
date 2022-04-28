from PyQt5.QtWidgets import * 
import sys
  
# creating a class
# that inherits the QDialog class
class Window(QDialog):
  
    # constructor
    def __init__(self):
        super(Window, self).__init__()
  
        # setting window title
        self.setWindowTitle("Python")
  
        # setting geometry to the window
        self.setGeometry(100, 100, 800, 800)
  
        # creating a group box
        self.formGroupBox = QGroupBox("stock market")
  
        # creating spin box to select age
        self.ageSpinBar = QSpinBox()
        self.ageSpinBar.setRange(1,1000000)
  
        # creating combo box to select degree
        self.degreeComboBox = QComboBox()
  
        # adding items to the combo box
        self.degreeComboBox.addItems(['ALEMBICLTD','CHEMCON','GICRE','ANGELBRKG','NIACL','BERGEPAINT','CANFINHOME','CENTENKA','CESC','HEMIPROP','CLNINDIA','DCMSHRIRAM','ELGIEQUIP','EPL','FINCABLES','GABRIEL','GHCL','GICHSGFIN','NEWGEN','GNFC','FMGOETZE','KANSAINER','CASTROLIND','GUJALKALI','HARRMALAYA','HIMATSEIDE','INDIAGLYCO','BECTORFOOD','JAYSREETEA','JINDALPOLY','KANPRPLA','KAKATCEM','KALPATPOWR','ACRYSIL','KOPRAN','TRENT','MAHSEAMLES','STOVEKRAFT','BDL','MUNJALSHOW','HEIDELBERG','NELCO','ISEC','HERANBA','PRSMJOHNSN','RSWM','ANURAS','HITECH','SURYODAY','WONDERLA','BARBEQUE','LODHA','JTEKTINDIA','STARPAPER','SURYAROSNI','TINPLATE','TIRUMALCHM','UNIVCABLES','JUBLPHARMA','VIPIND','VLSFINANCE','WATERBASE','RITES','ZODIACLOTH','ZUARIGLOB','CAPLIPOINT','TNPL','GREENPLY','JAYAGROGN','PANACEABIO','STERTOOLS','JAGSNPHARM','CREDITACC','JMCPROJECT','AARTIDRUGS','RAMCOIND','HERITGFOOD','INDSWFTLAB','FDC','CIGNITITEC','TRIGYN','GRSE','CYIENT','KOTAKBKETF','INTELLECT','CYBERTECH','GOODLUCK','CAMLINFINE','DTIL','SONATSOFTW','SETFNIFBK','STAR','RAJESHEXPO','RAMCOSYS','GEPIL','AVANTIFEED','ARVINDFASN','STLTECH','TAJGVK','HIKAL','KPITTECH','SMARTLINK','SETFNIF50','SYNGENE','PPL','SHARDAMOTR','TCI','SHREEPUSHK','STCINDIA','RADICO','NATHBIOGEN','CREATIVE','SHK','TVTODAY','VAIBHAVGBL','DATAMATICS','NIITLTD','WESTLIFE','LINCOLN','GUFICBIO','WELENT','JBMA','INDOCO','SUPRAJIT','GOKEX','MANGALAM','NH','MANINDS','ICIL','QUICKHEAL','GSPL','INOXLEISUR','INDOTECH','JKLAKSHMI','EMAMILTD','ACE','SELAN','GESHIP','SOBHA','VENUSREM','BANCOINDIA','PLASTIBLEN','JASH','SANGHVIMOV','PITTIENG','SEQUENT','NAHARSPING','KIRLFER','NCLIND','ALPHAGEO','MOTILALOFS','KSCL','KOLTEPATIL','JYOTHYLAB','BRIGADE','ARIES','DVL','JKIL','ONMOBILE','KNRCON','DHANI','PRINCEPIPE','GET&D','UJJIVAN','CROMPTON','SUMICHEM','PARAGMILK','BLS','MHRIL','SUNTECK','POKARNA','REFEX','DBCORP','TRF','ADVENZYMES','DBL','LGBBROSLTD','VERTOZ','KSL','BLISSGVS','HISARMETAL','BOROLTD','BAJAJCON','BSE','SASTASUNDR','CAREERP','RAMKY','WABAG','CLEDUCATE','OBEROIRLTY','PRESTIGE','IOLCP','GRAVITA','KIRLOSENG','STARCEMENT','BFINVEST','ERIS','CDSL','STEL','APEX','DCAL','CAPACITE','ICICITECH','N100','ESTER','ASHIANA','APLLTD','TRITURBINE','POLYMED','RUPA','MINDACORP','SWANENERGY','KITEX','ZUARI','CARERATING','REPCOHOME','ORIENTREF','APTECHT','PREMEXPLN'])
  
        # creating a line edit
        self.nameLineEdit = QLineEdit()

  
        # calling the method that create the form
        self.createForm()
  
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
  
        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)
  
        # addding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)
    
        # creating a vertical layout
        mainLayout = QVBoxLayout()
  
        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
  
        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)
  
        # setting lay out
        self.setLayout(mainLayout)
  
    # get info method called when form is accepted
    def getInfo(self):
  
        # printing the form information
        print("name : {0}".format(self.nameLineEdit.text()))
        print("Stock : {0}".format(self.degreeComboBox.currentText()))
        print("quantity : {0}".format(self.ageSpinBar.text()))
  
        # closing the window
   
  
    # creat form method
    def createForm(self):
  
        # creating a form layout
        layout = QFormLayout()
  
        # adding rows
        # for name and adding input text
        layout.addRow(QLabel("What is Your name"), self.nameLineEdit)

        # for degree and adding combo box
        layout.addRow(QLabel("Stock"), self.degreeComboBox)
  
        # for age and adding spin box
        
        
        layout.addRow(QLabel("quantity"), self.ageSpinBar)
        
        # setting layout
        self.formGroupBox.setLayout(layout)

  
  
# main method
if __name__ == '__main__':
  
    # create pyqt5 app
    app = QApplication(sys.argv)
  
    # create the instance of our Window
    window = Window()
  
    # showing the window
    window.show()
  
    # start the app
    sys.exit(app.exec())