import tkinter as tk
from tkinter import font, ttk
import sys
from PIL import Image, ImageTk
from threading import Timer
from time import sleep
import os.path
from sScraperMaster import generalScrape

bgLightColor = '#a8b5e9'
bgColor = '#8895c9'
darkGrey = '#262626'
mediumGrey = '#303030'
lightGrey = '#a0a0a0'
scrapeClight = '#76e070'
scrapeC = '#1abd11'
scrapeCdark = '#0f7d09'
maxColumns = 12
wwidth, wheight = 640, 800

scwindow = tk.Tk()
scwindow.title('CS:GO Skin Scraper')
scwindow.geometry(str(wwidth)+'x' + str(wheight) + '+2000+100')
scwindow.configure(bg=bgColor)
scwindow.resizable(width=False, height=False)

scwindow.iconbitmap('C:/Users/Jakob/OneDrive/Desktop/Programming/Python/myenv38progs/WebAutomation/SeleniumSkinScraper/Crap/cs.ico')
downArrowPNG = ImageTk.PhotoImage(Image.open('C:/Users/Jakob/Desktop/PyEnvs/myenv38progs/WebAutomation/SeleniumSkinScraper/Crap/Arrow-Down-icon (1).png'))
# unused
guiSettingsFile = ('C:/Users/Jakob/Desktop/PyEnvs/myenv38progs/WebAutomation/SeleniumSkinScraper/guiSettings.txt')


gunTypes = {'AK-47': 'weapon_ak47', 'AUG': 'weapon_aug', 'AWP': 'weapon_awp', 'CZ75-Auto': 'weapon_cz75a', 'Desert Eagle': 'weapon_deagle', 'Dual Berettas': 'weapon_elite', 'FAMAS': 'weapon_famas', 'Five-Seven': 'weapon_fiveseven', 'G3SG1': 'weapon_g3sg1', 'Galil AR': 'weapon_galilar', 'Glock-18': 'weapon_glock', 'M249': 'weapon_m249', 'M4A1-S': 'weapon_m4a1_silencer', 'M4A4': 'weapon_m4a4', 'MAC-10': 'weapon_mac10',
            'MAG-7': 'weapon_mag7', 'MP7': 'weapon_mp7', 'MP9': 'weapon_mp9', 'Negev': 'weapon_negev', 'Nova': 'weapon_nova', 'P2000': 'weapon_hkp2000', 'P250': 'weapon_p250', 'P90': 'weapon_p90', 'PP-Bizon': 'weapon_bizon', 'R8 Revolver': 'weapon_revolver', 'SCAR-20': 'weapon_scar20', 'SG 553': 'weapon_ssg556', 'SSG 08': 'weapon_ssg08', 'Sawed-Off': 'weapon_sawedoff', 'Tec-9': 'weapon_tec9', 'UMP-45': 'weapon_ump45', 'USP-S': 'weapon_usp_silencer', 'XM1014': 'weapon_xm1014'}
knifeTypes = {'Bayonet': 'weapon_bayonet', 'Bowie Knife':	'weapon_knife_survival_bowie', 'Butterfly Knife':	'weapon_knife_butterfly', 'Falchion Knife':	'weapon_knife_falchion', 'Flip Knife':	'weapon_knife_flip', 'Gut Knife':	'weapon_knife_gut', 'Huntsman Knife':	'weapon_knife_tactical',
              'Karambit':	'weapon_knife_karambit', 'M9 Bayonet':	'weapon_knife_m9_bayonet', 'Navaja Knife':	'weapon_knife_gypsy_jackknife', 'Shadow Daggers':	'weapon_knife_push', 'Stiletto Knife':	'weapon_knife_stiletto', 'Talon Knife':	'weapon_knife_widowmaker', 'Ursus Knife':	'weapon_knife_ursus'}
wearTypes = {'Factory New': ('FN', 0), 'Minimal Wear': ('MW', 1), 'Field-Tested': ('FT', 2), 'Well-Worn': ('WW', 3), 'Battle-Scarred': ('BS', 4), 'Not Painted': ('NP', 5)}


class sClassChoiceButton:  # row 2
    def __init__(self, knifeOrGun, correspondingDropDown, otherDropDown):
        if knifeOrGun == 'knife' or knifeOrGun == 'gun':
            self.stype = knifeOrGun
        else:
            sys.exit("WRONG TYPE REQUEST FOR DROP DOWN MENU")
        self.corresDropDown = correspondingDropDown
        self.otherDropDown = otherDropDown
        self.createChoiceButton(self.otherDropDown)

    def createChoiceButton(self, otherDropDown):
        self.button = tk.Button(scwindow, text='>> ' + self.stype.capitalize() + ' <<', font=("Bahnschrift Light", 18, 'bold'), bd=6, padx=10)
        self.button.config(command=lambda: self.buttonPressed(), bg=darkGrey, activebackground=lightGrey, fg=lightGrey)
        self.choiceBsnapToGrid()

    def choiceBsnapToGrid(self):
        if self.stype == 'gun':
            self.button.grid(row=2, column=1, columnspan=maxColumns-2, sticky='e', padx=45)
            # self.button.grid(row=2, column=0, columnspan=maxColumns//2, sticky='e', padx=45)
        elif self.stype == 'knife':
            self.button.grid(row=2, column=1, columnspan=maxColumns-2, sticky='w', padx=45)
            # self.button.grid(row=2, column=5, columnspan=maxColumns//2, sticky='w', padx=45)

    def buttonPressed(self):
        self.corresDropDown.showDropDown(self.otherDropDown)
        global lastButtonPressed
        lastButtonPressed = self.stype  # -------------------------------
        for b in wearButtonsArr:
            b.wearCsnapToGrid()
        specSrchInput.showSearchQuery()
        csvPathInput.showFileInputBox()
        scrapeInfotext.updateText()


class skinDropDown:  # row 3
    def __init__(self, knifeOrGun):
        if knifeOrGun == 'knife' or knifeOrGun == 'gun':
            self.stype = knifeOrGun
        else:
            sys.exit("WRONG TYPE REQUEST FOR DROP DOWN MENU")
        self.createSkinMenu()

    def createSkinMenu(self):
        self.curSelection = None
        sMenuSelection = tk.StringVar()
        sMenuSelection.set('CHOOSE ' + self.stype.upper())  # + ' SKIN'
        if self.stype == 'knife':
            self.Menu = tk.OptionMenu(scwindow, sMenuSelection, *knifeTypes.keys(), command=lambda x: self.storeSelection(x))
        elif self.stype == 'gun':
            self.Menu = tk.OptionMenu(scwindow, sMenuSelection, *gunTypes.keys(), command=lambda x: self.storeSelection(x))
        self.Menu.config(indicatoron=0, image=downArrowPNG, compound='right', font=("Bahnschrift SemiLight", 16), bd=6)
        self.Menu.config(bg=darkGrey, activebackground=lightGrey, fg=lightGrey, padx=15, pady=5)
        self.Menu["menu"]["bg"] = bgColor
        self.Menu["highlightthickness"] = 0

    def showDropDown(self, otherDropDown):
        otherDropDown.Menu.grid_forget()
        self.Menu.grid(row=3, column=1, columnspan=(maxColumns-2)//2, pady=20, sticky='')

    def storeSelection(self, selection):
        self.curSelection = selection
        goScrapeB.scrapeSnapToGrid()
        scrapeInfotext.updateText()


class searchInput:  # row 3
    def __init__(self):
        self.text = tk.StringVar()
        self.text.set('Enter Custom Search')
        self.inputMaxLen = 30
        self.sEntry = tk.Entry(scwindow,  bg=bgLightColor, font=("Bahnschrift SemiLight", 16), textvariable=self.text)
        self.sEntry.bind("<1>", lambda x: self.text.set('') if self.text.get() == 'Enter Custom Search' else None)
        self.sEntry.bind("<Key>", lambda x: Timer(0.01, lambda: self.searchQueryKeyPress()).start())

    def searchQueryKeyPress(self):
        if len(self.text.get()) >= self.inputMaxLen:
            Timer(0.01, lambda: self.text.set(self.text.get()[:self.inputMaxLen+1])).start()
            Timer(0.02, lambda: scrapeInfotext.updateText()).start()
        Timer(0.01, lambda: scrapeInfotext.updateText()).start()

    def showSearchQuery(self):
        self.sEntry.grid(row=3, column=1, columnspan=maxColumns-2, sticky='e')


class wearChoiceButton:  # row 4
    def __init__(self, wear):
        if wear in wearTypes.keys():
            self.wear = wear
            self.formattedText = self.wear.replace('-', '\n').replace(' ', '\n')
            self.wearShort = wearTypes[self.wear][0]
            self.wearid = wearTypes[self.wear][1]
        else:
            sys.exit("WRONG WEAR TYPE FOR BUTTON")
        self.isToggled = False
        self.createChoiceButton()

    def createChoiceButton(self):
        self.button = tk.Button(scwindow, text=self.formattedText, font=("Bahnschrift Light", 12, 'bold', 'overstrike'), bd=6, width=7)
        self.button.config(command=lambda: self.buttonPressed(), bg=darkGrey, activebackground=lightGrey, fg=lightGrey)

    def wearCsnapToGrid(self):
        self.button.grid(row=4, column=self.wearid*2, columnspan=2, padx=5, sticky='')

    def buttonPressed(self):
        if self.isToggled:
            self.button.config(relief='raised', bg=darkGrey, activebackground=lightGrey, fg=lightGrey, font=("Bahnschrift Light", 12, 'bold', 'overstrike'))
        else:
            self.button.config(relief='sunken', bg=lightGrey, activebackground=darkGrey, fg='black', font=("Bahnschrift Light", 12, 'bold'))
        self.isToggled = not(self.isToggled)
        scrapeInfotext.updateText()


class scrapeInfoTextC:  # row 5
    def __init__(self):
        # self.label = tk.Label(scwindow, font=("Bahnschriftt", 12), background=bgLightColor, padx=5, pady=5, relief='solid', bd=1)
        self.text = tk.Label(scwindow, font=("Bahnschriftt", 12), background=bgLightColor, padx=5, pady=5)

    def infoSnapToGrid(self):
        # self.label.grid(row=5, columnspan=maxColumns, padx=20, pady=(40, 0))
        self.text.grid(row=6, columnspan=maxColumns, padx=20, pady=(40, 0))

    def updateText(self):
        if os.path.isdir(csvPathInput.fShlashText):
            # endDirStr = csvPathInput.fShlashText[-csvPathInput.fShlashText[-2::-1].find('/')-2:]
            (_, _, qLink, weaponCodeArg, wearArg, _) = formatSkinDetails()
            if not(weaponCodeArg):
                self.text.config(text='No weapon selected')
                self.infoSnapToGrid()
                return
            if not(wearArg):
                wearArg = '_all'
            # csvShort = csvPathInput.fShlashText[:3] + ' ... ' + endDirStr + weaponCodeArg + qLink + wearArg + '.csv'
            if qLink:
                qLink = '_' + qLink
            csvShort = '/' + weaponCodeArg + qLink + wearArg + '.csv'
        else:
            self.text.config(text='Invalid directory. Must Already have been created.')
            self.infoSnapToGrid()
            return

# legacy# self.text.config(text='You are about to scrape for ' + skinSelectedStr + ' ' + catSelStr + ' ' + custSearch + '. The scrape results will be stored under ' + csvShort, wraplength=round(wwidth*0.9))
        self.text.config(text='The scrape results will be stored under ' + csvShort, wraplength=round(wwidth*0.9))
        self.infoSnapToGrid()


class fileStoreInput:  # row 5
    def __init__(self):
        self.text = tk.StringVar()
        self.text.set('C:/Users/Jakob/Desktop/PyEnvs/myenv38progs/WebAutomation/SeleniumSkinScraper/CSV FILES/')
        self.fShlashText = 'C:/Users/Jakob/Desktop/PyEnvs/myenv38progs/WebAutomation/SeleniumSkinScraper/CSV FILES/'
        self.inputMaxLen = 200
        self.pathEntry = tk.Entry(scwindow,  bg=bgLightColor, font=("Bahnschrift SemiLight", 12), textvariable=self.text, width=round(wwidth/10))
        self.pathEntry.bind("<KeyPress>", lambda x: Timer(0.01, lambda: self.pathInputKeyPress()).start())

    def pathInputKeyPress(self):
        if len(self.text.get()) >= self.inputMaxLen:
            Timer(0.01, lambda: self.text.set(self.text.get()[:self.inputMaxLen+1])).start()
            Timer(0.02, lambda: scrapeInfotext.updateText()).start()
        Timer(0.01, lambda: self.updateForwardSlashText()).start()
        Timer(0.05, lambda: scrapeInfotext.updateText()).start()

    def showFileInputBox(self):
        self.pathEntry.grid(row=5, columnspan=maxColumns, sticky='', pady=(20, 0))

    def updateForwardSlashText(self):
        self.fShlashText = self.text.get()
        print('.' + self.fShlashText + '.')
        self.fShlashText.replace('\\', '/')
        if self.fShlashText[-1] != '/':
            self.fShlashText += '/'


class scrapeExecutor:  # row 7

    def __init__(self):
        self.button = tk.Button(scwindow, text='Scrape Skins!', command=self.goScrape, font=("Bahnschrift", 22, 'bold'))
        self.button.config(bd=10, padx=20, pady=10, bg=scrapeCdark, activebackground=scrapeC, fg=scrapeClight)

    def scrapeSnapToGrid(self):
        self.button.grid(row=7, column=0, columnspan=maxColumns, pady=(30, 0), sticky='n')

    def goScrape(self):
        (skinPartLink, wearPartLink, qLink, weaponCodeArg, wearArg, isKnife) = formatSkinDetails()

        skinLink = 'https://steamcommunity.com/market/search?category_730_Weapon%5B%5D=tag_' + skinPartLink+wearPartLink+'&appid=730&q=' + qLink + '#p1_price_asc'
        qfileName = '_' + qLink if qLink else qLink
        if not(wearArg):
            wearArg = '_all'
        csvFileName = csvPathInput.fShlashText + weaponCodeArg + qfileName + wearArg + '.csv'

        fullWearArgList = []
        for x in wearButtonsArr:
            if x.isToggled:
                fullWearArgList.append(x.wear)
        if not(fullWearArgList):
            for x in wearButtonsArr:
                fullWearArgList.append(x.wear)

        if lastButtonPressed == 'gun':
            weaponFullName = gunSkinDropDown.curSelection
        elif lastButtonPressed == 'knife':
            weaponFullName = knifeSkinDropDown.curSelection
        else:
            sys.exit('Can\'t retrive full skin name for scrape')
        # ========================================================================================================================================
        # ========================================================================================================================================
        nrOfSkinsScraped = generalScrape(weaponFullName, fullWearArgList, csvFileName, skinLink, isKnife, wearTypes)  # ===========================
        # ========================================================================================================================================
        # ========================================================================================================================================
        scrapeResultInfo.updateResultText(nrOfSkinsScraped)


class scrapeResultInfo:  # row 8
    def __init__(self):
        # self.label = tk.Label(scwindow, font=("Bahnschriftt", 12), background=bgLightColor, padx=5, pady=5, relief='solid', bd=1)
        self.text = tk.Label(scwindow, font=("Bahnschriftt", 18), background=bgLightColor, padx=15, pady=15)

    def infoSnapToGrid(self):
        self.text.grid(row=8, columnspan=maxColumns, padx=20, pady=(30, 0))

    def updateResultText(self, nrOfSkins):
        if not(nrOfSkins):
            self.text.config(text='Didn\'t find any skins :(')
        elif nrOfSkins == 1:
            self.text.config(text='Successfully scraped 1 Skin!')
        else:
            self.text.config(text='Successfully scraped ' + str(nrOfSkins) + ' Skins!')
        self.infoSnapToGrid()


def formatSkinDetails():
    skinPartLink = ''
    isKnife = False
    if lastButtonPressed == 'gun':
        stypes = gunTypes
        sDropDown = gunSkinDropDown
    elif lastButtonPressed == 'knife':
        isKnife = True
        stypes = knifeTypes
        sDropDown = knifeSkinDropDown
    else:
        sys.exit('goScrapeFail')
    weaponNameArg = sDropDown.curSelection
    if not(weaponNameArg):
        print('No Weapon Selected')
        return (None, None, None, None, None, None)
    weaponCodeArg = stypes[sDropDown.curSelection][7:]
    skinPartLink = stypes[sDropDown.curSelection]

    wearPartLink = wearArg = ''
    for x in wearButtonsArr:
        if x.isToggled:
            wearPartLink += '&category_730_Exterior%5B%5D=tag_WearCategory' + str(x.wearid)
            wearArg += '_' + str(x.wearShort).lower()
    if wearPartLink and wearPartLink[-1] == '5':
        wearPartLink = wearPartLink[:-1]+'NA'
    qLink = ''
    if specSrchInput.text.get() != 'Enter Custom Search' and specSrchInput.text.get() != '':
        qLink = specSrchInput.text.get()
    return(skinPartLink, wearPartLink, qLink, weaponCodeArg, wearArg, isKnife)


lastButtonPressed = None
# row -1
versionLabel = tk.Label(scwindow, text='v0.8', font=("Bahnschriftt", 8), background=bgColor, padx=0, pady=0)
versionLabel.place(rely=1, relx=0, anchor='sw')
# row 0
welcomeLabel = tk.Label(scwindow, text='Welcome to the CS:GO Skin Scraper', font=("Bahnschriftt", 24), background=bgLightColor, padx=20, pady=10, relief='ridge', bd=5)
welcomeLabel.grid(row=0, sticky='N', columnspan=maxColumns, padx=30, pady=(20, 20))

# row 1
knifeOrGunLabel = tk.Label(scwindow, text='Want to scrape a knife or a gun?', font=("Bahnschrift SemiLight", 20), background=bgLightColor, padx=20, pady=10, relief='ridge', bd=5)
knifeOrGunLabel.grid(row=1, sticky='N', columnspan=maxColumns, padx=20, pady=(0, 20))

# row3
gunSkinDropDown = skinDropDown('gun')
knifeSkinDropDown = skinDropDown('knife')
specSrchInput = searchInput()

# row 2
gunChoiceB = sClassChoiceButton('gun', gunSkinDropDown, knifeSkinDropDown)
knifeChoiceB = sClassChoiceButton('knife', knifeSkinDropDown, gunSkinDropDown)

# row 4
wearButtonsArr = []
for wear in wearTypes:
    wearButtonsArr.append(wearChoiceButton(wear))

# row 5
csvPathInput = fileStoreInput()

# row 6
scrapeInfotext = scrapeInfoTextC()

# row 7
goScrapeB = scrapeExecutor()

# row 8
scrapeResultInfo = scrapeResultInfo()

scwindow.mainloop()
