# IMPORTS
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# WEB ENGINE( pip install PyQtWebEngine)
from PyQt5.QtWebEngineWidgets import *

# MAIN WINDOW
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # ADD WINDOW ELEMENTOS

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # ADD CLICAR 2 VEZES
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        # ADD fechar a aba atual
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # ADD mudar a aba atual para outra
        self.tabs.currentChanged.connect(self.current_tab_changed)


        # ADD ferramentas de navegação
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(20, 20))
        self.addToolBar(navtb)

        # ADD botoes para navegação
        back_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        # NAVIGAR PARA PAGINA ANTERIOR
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())




        # PROXIMA PAGINA BOTÃO
        next_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        # IR PARA PROXIMA PAGINA
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())




        # RECARREGAR
        reload_btn = QAction(QIcon(os.path.join('icons', 'cil-reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)
        # RELOAD
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())




        #BOTAO DA HOME PAGE
        home_btn = QAction(QIcon(os.path.join('icons', 'cil-home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)
        # NAVEGAR PARA HOME PAGE
        home_btn.triggered.connect(self.navigate_home)



        # ADD SEPARADOR
        navtb.addSeparator()

        # ADD MOSTRAR A SEGURANÇA DO SITE
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        # ADD LINE EDIT PARA MOSTRAR E EDITAR URLS
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        # CARREGAR URL QUANDO ENTER FOR APERTADO
        self.urlbar.returnPressed.connect(self.navigate_to_url)



        # ADD BOTAO PARA PARAR DE CARREGAR
        stop_btn = QAction(QIcon(os.path.join('icons', 'cil-media-stop.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)
        # PARAR DE CARREGAR URL
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())


        # ADD TOP MENU
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        # ADD FILE MENU ACTIONS
        new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        # ADD NOVA ABA
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())


        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        # ADD HELP MENU AÇÕES
        navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')),
                                            "Homepage", self)
        navigate_home_action.setStatusTip("Go to Macaw Browser Homepage")
        help_menu.addAction(navigate_home_action)
        # NAVIGATE TO DEVELOPER WEBSITE
        navigate_home_action.triggered.connect(self.navigate_home)



        # SET WINDOW TITTLE AND ICON
        self.setWindowTitle("Macaw Browser")
        self.setWindowIcon(QIcon(os.path.join('icons', 'macaw5.png')))


        # ADD STYLESHEET PARA CUSTOMIZAR AS JANELAS
        # STYLESHEET (DARK MODE)
        self.setStyleSheet("""QWidget{
           background-color: rgb(48, 48, 48);
           color: rgb(255, 255, 255);
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid rgb(90, 90, 90);
            position: absolute;
            top: -0.5em;
            color: rgb(255, 255, 255);
            padding: 2px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QLabel, QToolButton, QTabBar::tab {
            background: rgb(90, 90, 90);
            border: 2px solid rgb(90, 90, 90);
            /*border-bottom-color: #C2C7CB; /* same as the pane color */
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(255, 255, 255);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
        }

        QLineEdit {
            border: 2px solid rgb(0, 36, 36);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(0, 36, 36);
            color: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 2px solid rgb(0, 66, 124);
        }
        QLineEdit:focus{
            border: 2px solid rgb(0, 136, 255);
            color: rgb(200, 200, 200);
        }
        QPushButton{
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")



        # CARREGAR DEFAULT HOME PAGE (DUCKDUCKGO)
        #url = https://start.duckduckgo.com/,
        #label = Homepage
        self.add_new_tab(QUrl('https://duckduckgo.com/'), 'Homepage')

        # MOSTRAR JANELA PRINCIPAL
        self.show()

    # ############################################
    # FUNCOES
    ##############################################
    # ADD NOVA ABA
    def add_new_tab(self, qurl=None, label="Blank"):
        # Checar se o url esta branco
        if qurl is None:
            qurl = QUrl('https://duckduckgo.com/')

        # CARREGAR O URL ESCRITO
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # ADD O SITE
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))


    # ADD NOVA ABA QUANDO CLICAR 2 VEZES
    def tab_open_doubleclick(self, i):
        if i == -1:  # nenhuma aba sem clicar
            self.add_new_tab()

    # FECHAR ABAS
    def close_current_tab(self, i):
        if self.tabs.count() < 2: #so fechar se tiver mais de uma aba aberta
            return

        self.tabs.removeTab(i)


    # UPDATE TEXTO DA URL QUANDO ABA ATIVA E MUDADA
    def update_urlbar(self, q, browser=None):
        #q = QURL
        if browser != self.tabs.currentWidget():
            # SE O SINAL NAO FOR DA ABA ATUAL, IGNORE
            return
        # URL Schema
        if q.scheme() == 'https':
            # SE O CADEADO ESTIVER FECHADO SIGINIFICA QUE O SITE E SEGURO
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-locked.png')))

        else:
            # SE O CADEADO ESTIVER ABERTO SIGINIFICA QUE O SITE E PERIGOSO
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)



    # ABA ATIVA MUDANÇA DE ACOES
    def current_tab_changed(self, i):
        # i = tab index
        # PEGAR O URL DA ABA ATUAL
        qurl = self.tabs.currentWidget().url()
        # UPDATE O TEXTO DA URL
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # UPDATE TITULO DA JANELA
        self.update_title(self.tabs.currentWidget())


    # UPDATE TITULO DA JANELA
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():

            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)


    # NAVEGAR PARA PAGINA ANTERIOR
    def navigate_to_url(self):  # NAO RECEBE A URL
        # PEGA O TEXTO DA URL
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            # PEGA HTTP COMO ESQUEMA PRINCIPAL
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)


    # NAVEGAR PARA HOME PAGE
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com/"))








app = QApplication(sys.argv)
# NOME
app.setApplicationName("Macaw Browser")
# COMPANIA
app.setOrganizationName("Macaw Company")
# ORGANIZAÇÃO
app.setOrganizationDomain("macaw.org")


window = MainWindow()
app.exec_()