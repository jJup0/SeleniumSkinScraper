import logging
import os.path
import sys
import tkinter as tk
from threading import Timer
from typing import Literal

from PIL import Image, ImageTk

from seleniumSkinScraper import generalScrape

logger = logging.getLogger(__name__)

bgLightColor = "#a8b5e9"
bgColor = "#8895c9"
darkGrey = "#262626"
mediumGrey = "#303030"
lightGrey = "#a0a0a0"
scrapeClight = "#76e070"
scrapeC = "#1abd11"
scrapeCdark = "#0f7d09"
maxColumns = 12
wwidth, wheight = 640, 800

scwindow = tk.Tk()
scwindow.title("CS:GO Skin Scraper")
scwindow.geometry(str(wwidth) + "x" + str(wheight) + "+2000+100")
scwindow.configure(bg=bgColor)
scwindow.resizable(width=False, height=False)

cwd = os.path.dirname(__file__)
scwindow.iconbitmap(os.path.join(cwd, "icons", "cs.ico"))  # type: ignore # unknown
downArrowPNG = ImageTk.PhotoImage(
    Image.open(os.path.join(cwd, "icons", "Arrow-Down-icon-small.png"))
)


gunTypes = {
    "AK-47": "weapon_ak47",
    "AUG": "weapon_aug",
    "AWP": "weapon_awp",
    "CZ75-Auto": "weapon_cz75a",
    "Desert Eagle": "weapon_deagle",
    "Dual Berettas": "weapon_elite",
    "FAMAS": "weapon_famas",
    "Five-Seven": "weapon_fiveseven",
    "G3SG1": "weapon_g3sg1",
    "Galil AR": "weapon_galilar",
    "Glock-18": "weapon_glock",
    "M249": "weapon_m249",
    "M4A1-S": "weapon_m4a1_silencer",
    "M4A4": "weapon_m4a4",
    "MAC-10": "weapon_mac10",
    "MAG-7": "weapon_mag7",
    "MP7": "weapon_mp7",
    "MP9": "weapon_mp9",
    "Negev": "weapon_negev",
    "Nova": "weapon_nova",
    "P2000": "weapon_hkp2000",
    "P250": "weapon_p250",
    "P90": "weapon_p90",
    "PP-Bizon": "weapon_bizon",
    "R8 Revolver": "weapon_revolver",
    "SCAR-20": "weapon_scar20",
    "SG 553": "weapon_ssg556",
    "SSG 08": "weapon_ssg08",
    "Sawed-Off": "weapon_sawedoff",
    "Tec-9": "weapon_tec9",
    "UMP-45": "weapon_ump45",
    "USP-S": "weapon_usp_silencer",
    "XM1014": "weapon_xm1014",
}
knifeTypes = {
    "Bayonet": "weapon_bayonet",
    "Bowie Knife": "weapon_knife_survival_bowie",
    "Butterfly Knife": "weapon_knife_butterfly",
    "Falchion Knife": "weapon_knife_falchion",
    "Flip Knife": "weapon_knife_flip",
    "Gut Knife": "weapon_knife_gut",
    "Huntsman Knife": "weapon_knife_tactical",
    "Karambit": "weapon_knife_karambit",
    "M9 Bayonet": "weapon_knife_m9_bayonet",
    "Navaja Knife": "weapon_knife_gypsy_jackknife",
    "Shadow Daggers": "weapon_knife_push",
    "Stiletto Knife": "weapon_knife_stiletto",
    "Talon Knife": "weapon_knife_widowmaker",
    "Ursus Knife": "weapon_knife_ursus",
}
wearTypes = {
    "Factory New": ("FN", 0),
    "Minimal Wear": ("MW", 1),
    "Field-Tested": ("FT", 2),
    "Well-Worn": ("WW", 3),
    "Battle-Scarred": ("BS", 4),
    "Not Painted": ("NP", 5),
}


KnifeOrGun_T = Literal["knife"] | Literal["gun"]


class SkinClassChoiceButton:  # row 2
    def __init__(
        self,
        knifeOrGun: KnifeOrGun_T,
        correspondingDropDown: "SkinDropDown",
        otherDropDown: "SkinDropDown",
    ):
        if knifeOrGun == "knife" or knifeOrGun == "gun":
            self.stype = knifeOrGun
        else:
            sys.exit("WRONG TYPE REQUEST FOR DROP DOWN MENU")
        self.corresDropDown = correspondingDropDown
        self.otherDropDown = otherDropDown
        self.createChoiceButton(self.otherDropDown)  # type: ignore #unknown

    def createChoiceButton(self, otherDropDown: "SkinDropDown"):
        self.button = tk.Button(
            scwindow,
            text=">> " + self.stype.capitalize() + " <<",
            font=("Bahnschrift Light", 18, "bold"),
            bd=6,
            padx=10,
        )
        self.button.config(
            command=lambda: self.buttonPressed(),
            bg=darkGrey,
            activebackground=lightGrey,
            fg=lightGrey,
        )
        self.choiceBsnapToGrid()

    def choiceBsnapToGrid(self):
        if self.stype == "gun":
            self.button.grid(
                row=2, column=1, columnspan=maxColumns - 2, sticky="e", padx=45
            )
            # self.button.grid(row=2, column=0, columnspan=maxColumns//2, sticky='e', padx=45)
        elif self.stype == "knife":
            self.button.grid(
                row=2, column=1, columnspan=maxColumns - 2, sticky="w", padx=45
            )
            # self.button.grid(row=2, column=5, columnspan=maxColumns//2, sticky='w', padx=45)

    def buttonPressed(self):
        self.corresDropDown.showDropDown(self.otherDropDown)  # type: ignore # unknown
        global lastButtonPressed
        lastButtonPressed = self.stype  # -------------------------------
        for b in wearButtonsArr:
            b.wearCsnapToGrid()
        specSrchInput.showSearchQuery()
        csvPathInput.showFileInputBox()
        scrapeInfotext.updateText()


class SkinDropDown:  # row 3
    def __init__(self, knifeOrGun: KnifeOrGun_T):
        if knifeOrGun == "knife" or knifeOrGun == "gun":
            self.stype = knifeOrGun
        else:
            sys.exit("WRONG TYPE REQUEST FOR DROP DOWN MENU")

        self._current_selection: str | None = None
        sMenuSelection = tk.StringVar()
        sMenuSelection.set("CHOOSE " + self.stype.upper())  # + ' SKIN'
        if self.stype == "knife":
            self.Menu = tk.OptionMenu(
                scwindow,
                sMenuSelection,
                *knifeTypes.keys(),
                command=lambda x: setattr(self, "current_selection", x),
            )
        elif self.stype == "gun":
            self.Menu = tk.OptionMenu(
                scwindow,
                sMenuSelection,
                *gunTypes.keys(),
                command=lambda x: setattr(self, "current_selection", x),
            )
        self.Menu.config(
            indicatoron=False,
            image=downArrowPNG,
            compound="right",
            font=("Bahnschrift SemiLight", 16),
            bd=6,
        )
        self.Menu.config(
            bg=darkGrey, activebackground=lightGrey, fg=lightGrey, padx=15, pady=5
        )
        self.Menu["menu"]["bg"] = bgColor
        self.Menu["highlightthickness"] = 0

    def showDropDown(self, otherDropDown: "SkinDropDown"):
        otherDropDown.Menu.grid_forget()
        self.Menu.grid(
            row=3, column=1, columnspan=(maxColumns - 2) // 2, pady=20, sticky=""
        )

    @property
    def current_selection(self) -> str | None:
        return self._current_selection

    @current_selection.setter
    def current_selection(self, selection: tk.StringVar) -> None:
        logger.critical(
            "setting selection for %s dropdown to %s", self.stype, selection
        )
        self._current_selection = str(selection)
        goScrapeB.scrapeSnapToGrid()
        scrapeInfotext.updateText()


class SearchInput:  # row 3
    def __init__(self):
        self.text = tk.StringVar()
        self.text.set("Enter Custom Search")
        self.inputMaxLen = 30
        self.sEntry = tk.Entry(
            scwindow,
            bg=bgLightColor,
            font=("Bahnschrift SemiLight", 16),
            textvariable=self.text,
        )
        self.sEntry.bind(
            "<1>",
            lambda x: self.text.set("")
            if self.text.get() == "Enter Custom Search"
            else None,
        )
        self.sEntry.bind(
            "<Key>", lambda x: Timer(0.01, lambda: self.searchQueryKeyPress()).start()
        )

    def searchQueryKeyPress(self):
        if len(self.text.get()) >= self.inputMaxLen:
            Timer(
                0.01, lambda: self.text.set(self.text.get()[: self.inputMaxLen + 1])
            ).start()
            Timer(0.02, lambda: scrapeInfotext.updateText()).start()
        Timer(0.01, lambda: scrapeInfotext.updateText()).start()

    def showSearchQuery(self):
        self.sEntry.grid(row=3, column=1, columnspan=maxColumns - 2, sticky="e")


class WearChoiceButton:  # row 4
    def __init__(self, wear: str):
        if wear not in wearTypes.keys():
            sys.exit("WRONG WEAR TYPE FOR BUTTON")

        self.wear = wear
        self.formattedText = self.wear.replace("-", "\n").replace(" ", "\n")
        self.wearShort = wearTypes[self.wear][0]
        self.wearid = wearTypes[self.wear][1]
        self.isToggled = False
        self.createChoiceButton()

    def createChoiceButton(self):
        self.button = tk.Button(
            scwindow,
            text=self.formattedText,
            font=("Bahnschrift Light", 12, "bold", "overstrike"),
            bd=6,
            width=7,
        )
        self.button.config(
            command=lambda: self.buttonPressed(),
            bg=darkGrey,
            activebackground=lightGrey,
            fg=lightGrey,
        )

    def wearCsnapToGrid(self):
        self.button.grid(row=4, column=self.wearid * 2, columnspan=2, padx=5, sticky="")

    def buttonPressed(self):
        if self.isToggled:
            self.button.config(
                relief="raised",
                bg=darkGrey,
                activebackground=lightGrey,
                fg=lightGrey,
                font=("Bahnschrift Light", 12, "bold", "overstrike"),
            )
        else:
            self.button.config(
                relief="sunken",
                bg=lightGrey,
                activebackground=darkGrey,
                fg="black",
                font=("Bahnschrift Light", 12, "bold"),
            )
        self.isToggled = not (self.isToggled)
        scrapeInfotext.updateText()


class ScrapeInfoTextC:  # row 5
    def __init__(self):
        # self.label = tk.Label(scwindow, font=("Bahnschriftt", 12), background=bgLightColor, padx=5, pady=5, relief='solid', bd=1)
        self.text = tk.Label(
            scwindow, font=("Bahnschriftt", 12), background=bgLightColor, padx=5, pady=5
        )

    def infoSnapToGrid(self):
        # self.label.grid(row=5, columnspan=maxColumns, padx=20, pady=(40, 0))
        self.text.grid(row=6, columnspan=maxColumns, padx=20, pady=(40, 0))

    def updateText(self):
        if os.path.isdir(csvPathInput.fSlashText):
            # endDirStr = csvPathInput.fShlashText[-csvPathInput.fShlashText[-2::-1].find('/')-2:]
            skin_details = formatSkinDetails()
            if skin_details is None:
                self.text.config(text="No weapon selected")
                self.infoSnapToGrid()
                return
            _, _, qLink, weaponCodeArg, wearArg, _ = skin_details
            if not (wearArg):
                wearArg = "_all"
            # csvShort = csvPathInput.fShlashText[:3] + ' ... ' + endDirStr + weaponCodeArg + qLink + wearArg + '.csv'
            if qLink:
                qLink = "_" + qLink
            csvShort = "/" + weaponCodeArg + qLink + wearArg + ".csv"
        else:
            self.text.config(text="Invalid directory. Must Already have been created.")
            self.infoSnapToGrid()
            return

        # legacy# self.text.config(text='You are about to scrape for ' + skinSelectedStr + ' ' + catSelStr + ' ' + custSearch + '. The scrape results will be stored under ' + csvShort, wraplength=round(wwidth*0.9))
        self.text.config(
            text="The scrape results will be stored under " + csvShort,
            wraplength=round(wwidth * 0.9),
        )
        self.infoSnapToGrid()


class FileStoreInput:  # row 5
    def __init__(self):
        self.text = tk.StringVar()
        csv_dir = os.path.join(cwd, "csv_files", "")
        self.text.set(csv_dir)
        self.fSlashText = csv_dir
        self.inputMaxLen = 200
        self.pathEntry = tk.Entry(
            scwindow,
            bg=bgLightColor,
            font=("Bahnschrift SemiLight", 12),
            textvariable=self.text,
            width=round(wwidth / 10),
        )
        self.pathEntry.bind(
            "<KeyPress>",
            lambda x: Timer(0.01, lambda: self.pathInputKeyPress()).start(),
        )

    def pathInputKeyPress(self):
        if len(self.text.get()) >= self.inputMaxLen:
            Timer(
                0.01, lambda: self.text.set(self.text.get()[: self.inputMaxLen + 1])
            ).start()
            Timer(0.02, lambda: scrapeInfotext.updateText()).start()
        # Timer(0.01, lambda: self.updateForwardSlashText()).start()
        Timer(0.05, lambda: scrapeInfotext.updateText()).start()

    def showFileInputBox(self):
        self.pathEntry.grid(row=5, columnspan=maxColumns, sticky="", pady=(20, 0))

    # def updateForwardSlashText(self):
    #     self.fSlashText = self.text.get()
    #     print("." + self.fSlashText + ".")
    #     self.fSlashText.replace("\\", "/")
    #     if self.fSlashText[-1] != "/":
    #         self.fSlashText += "/"


class ScrapeExecutor:  # row 7
    def __init__(self):
        self.button = tk.Button(
            scwindow,
            text="Scrape Skins!",
            command=self.goScrape,
            font=("Bahnschrift", 22, "bold"),
        )
        self.button.config(
            bd=10,
            padx=20,
            pady=10,
            bg=scrapeCdark,
            activebackground=scrapeC,
            fg=scrapeClight,
        )

    def scrapeSnapToGrid(self):
        self.button.grid(
            row=7, column=0, columnspan=maxColumns, pady=(30, 0), sticky="n"
        )

    def goScrape(self):
        format_skin_details = formatSkinDetails()
        if format_skin_details is None:
            print("no skin seleted")
            return
        (
            skinPartLink,
            wearPartLink,
            qLink,
            weaponCodeArg,
            wearArg,
            isKnife,
        ) = format_skin_details

        skinLink = (
            "https://steamcommunity.com/market/search?category_730_Weapon%5B%5D=tag_"
            + skinPartLink
            + wearPartLink
            + "&appid=730&q="
            + qLink
            + "#p1_price_asc"
        )
        print(f"{skinLink= }")
        qfileName = "_" + qLink if qLink else qLink
        if not (wearArg):
            wearArg = "_all"
        csv_file_path = os.path.join(
            cwd, f"{csvPathInput.text.get()}_{weaponCodeArg}{qfileName}{wearArg}.csv"
        )

        fullWearArgList: list[str] = [x.wear for x in wearButtonsArr if x.isToggled]
        if not fullWearArgList:
            fullWearArgList = [x.wear for x in wearButtonsArr]

        if lastButtonPressed == "gun":
            weaponFullName = gunSkinDropDown.current_selection
        elif lastButtonPressed == "knife":
            weaponFullName = knifeSkinDropDown.current_selection
        else:
            sys.exit("Can't retrive full skin name for scrape")
        assert weaponFullName is not None
        nrOfSkinsScraped = generalScrape(
            weaponFullName, fullWearArgList, csv_file_path, skinLink, isKnife, wearTypes
        )
        scrapeResultInfo.updateResultText(nrOfSkinsScraped)


class ScrapeResultInfo:  # row 8
    def __init__(self):
        # self.label = tk.Label(scwindow, font=("Bahnschriftt", 12), background=bgLightColor, padx=5, pady=5, relief='solid', bd=1)
        self.text = tk.Label(
            scwindow,
            font=("Bahnschriftt", 18),
            background=bgLightColor,
            padx=15,
            pady=15,
        )

    def infoSnapToGrid(self):
        self.text.grid(row=8, columnspan=maxColumns, padx=20, pady=(30, 0))

    def updateResultText(self, nrOfSkins: int):
        if not (nrOfSkins):
            self.text.config(text="Didn't find any skins :(")
        elif nrOfSkins == 1:
            self.text.config(text="Successfully scraped 1 Skin!")
        else:
            self.text.config(text=f"Successfully scraped {nrOfSkins} Skins!")
        self.infoSnapToGrid()


def formatSkinDetails():
    global lastButtonPressed
    skinPartLink = ""
    isKnife = False
    if lastButtonPressed == "gun":
        stypes = gunTypes
        sDropDown = gunSkinDropDown
    elif lastButtonPressed == "knife":
        isKnife = True
        stypes = knifeTypes
        sDropDown = knifeSkinDropDown
    else:
        sys.exit("goScrapeFail")

    curr_selected_weapon = sDropDown.current_selection
    if curr_selected_weapon is None:
        return None
    weaponCodeArg = stypes[curr_selected_weapon][7:]
    skinPartLink = stypes[curr_selected_weapon]

    wearPartLink = wearArg = ""
    for x in wearButtonsArr:
        if x.isToggled:
            wearPartLink += "&category_730_Exterior%5B%5D=tag_WearCategory" + str(
                x.wearid
            )
            wearArg += "_" + str(x.wearShort).lower()
    if wearPartLink and wearPartLink[-1] == "5":
        wearPartLink = wearPartLink[:-1] + "NA"
    qLink = ""
    if (
        specSrchInput.text.get() != "Enter Custom Search"
        and specSrchInput.text.get() != ""
    ):
        qLink = specSrchInput.text.get()
    return (skinPartLink, wearPartLink, qLink, weaponCodeArg, wearArg, isKnife)


lastButtonPressed = None
# row -1
versionLabel = tk.Label(
    scwindow, text="v0.8", font=("Bahnschriftt", 8), background=bgColor, padx=0, pady=0
)
versionLabel.place(rely=1, relx=0, anchor="sw")
# row 0
welcomeLabel = tk.Label(
    scwindow,
    text="Welcome to the CS:GO Skin Scraper",
    font=("Bahnschriftt", 24),
    background=bgLightColor,
    padx=20,
    pady=10,
    relief="ridge",
    bd=5,
)
welcomeLabel.grid(row=0, sticky="N", columnspan=maxColumns, padx=30, pady=(20, 20))

# row 1
knifeOrGunLabel = tk.Label(
    scwindow,
    text="Want to scrape a knife or a gun?",
    font=("Bahnschrift SemiLight", 20),
    background=bgLightColor,
    padx=20,
    pady=10,
    relief="ridge",
    bd=5,
)
knifeOrGunLabel.grid(row=1, sticky="N", columnspan=maxColumns, padx=20, pady=(0, 20))

# row3
gunSkinDropDown = SkinDropDown("gun")
knifeSkinDropDown = SkinDropDown("knife")
specSrchInput = SearchInput()

# row 2
gunChoiceB = SkinClassChoiceButton("gun", gunSkinDropDown, knifeSkinDropDown)
knifeChoiceB = SkinClassChoiceButton("knife", knifeSkinDropDown, gunSkinDropDown)

# row 4
wearButtonsArr = [WearChoiceButton(wear) for wear in wearTypes]

# row 5
csvPathInput = FileStoreInput()

# row 6
scrapeInfotext = ScrapeInfoTextC()

# row 7
goScrapeB = ScrapeExecutor()

# row 8
scrapeResultInfo = ScrapeResultInfo()

scwindow.mainloop()
