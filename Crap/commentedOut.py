def updateText(self):
    pass
    # legacy    # skinSelectedStr = 'nothing'
    # if lastButtonPressed == 'gun':
    #     if gunSkinDropDown.curSelection:
    #         skinSelectedStr = 'the ' + gunSkinDropDown.curSelection
    # elif lastButtonPressed == 'knife':
    #     if knifeSkinDropDown.curSelection:
    #         skinSelectedStr = 'the '+knifeSkinDropDown.curSelection
    # else:
    #     self.text.config(text='Invalid weapon type, must be knife or gun', wraplength=round(wwidth*0.9))
    #     self.infoSnapToGrid()
    #     return

    # legacy    # catSelStr = 'in the wear categories '
    # for b in wearButtonsArr:
    #     if b.isToggled:
    #         catSelStr += b.wearShort + ', '
    # if catSelStr == 'in the wear categories ' or catSelStr == 'in the wear categories FN, MW, FT, WW, BS, ':
    #     catSelStr = 'in all wear categories,'

    # legacy    # custSearch = 'oopsie'
    # if specSrchInput.text.get() == 'Enter Custom Search' or specSrchInput.text.get() == '':
    #     custSearch = 'without a custom input'
    # else:
    #     custSearch = 'with the custom search phrase: \"' + specSrchInput.text.get() + '\"'
#


# scrapeClight = '#8295e8'
# scrapeC = '#4962d1'
# scrapeCdark = '#1b37b3'


# knivesDict = {
#     'Bayonet': 'weapon_bayonet',
#     'Bowie Knife':	'weapon_knife_survival_bowie',
#     'Butterfly Knife':	'weapon_knife_butterfly',
#     'Falchion Knife':	'weapon_knife_falchion',
#     'Flip Knife':	'weapon_knife_flip',
#     'Gut Knife':	'weapon_knife_gut',
#     'Huntsman Knife':	'weapon_knife_tactical',
#     'Karambit':	'weapon_knife_karambit',
#     'M9 Bayonet':	'weapon_knife_m9_bayonet',
#     'Navaja Knife':	'weapon_knife_gypsy_jackknife',
#     'Shadow Daggers':	'weapon_knife_push',
#     'Stiletto Knife':	'weapon_knife_stiletto',
#     'Talon Knife':	'weapon_knife_widowmaker',
#     'Ursus Knife':	'weapon_knife_ursus'}
# knivesDict.sort()
# print(knivesDict)


# 'Bayonet,Bowie Knife,Butterfly Knife,Falchion Knife,Flip Knife,Gut Knife,Huntsman Knife,Karambit,'
# 'M9 Bayonet,Navaja Knife,Shadow Daggers,Stiletto Knife,Talon Knife,Ursus Knife'

# knivesArr = [
#     ['Bayonet', 'weapon_bayonet'],
#     ['Karambit',	'weapon_knife_karambit'],
#     ['M9 Bayonet',	'weapon_knife_m9_bayonet'],
#     ['Flip Knife',	'weapon_knife_flip'],
#     ['Gut Knife',	'weapon_knife_gut'],
#     ['Huntsman Knife',	'weapon_knife_tactical'],
#     ['Butterfly Knife',	'weapon_knife_butterfly'],
#     ['Falchion Knife',	'weapon_knife_falchion'],
#     ['Shadow Daggers',	'weapon_knife_push'],
#     ['Bowie Knife',	'weapon_knife_survival_bowie'],
#     ['Talon Knife',	'weapon_knife_widowmaker'],
#     ['Stiletto Knife',	'weapon_knife_stiletto'],
#     ['Navaja Knife',	'weapon_knife_gypsy_jackknife'],
#     ['Ursus Knife',	'weapon_knife_ursus']]

# onlyGunsArr = ['AK-47', 'AUG', 'AWP', 'CZ75-Auto', 'Desert Eagle', 'Dual Berettas', 'FAMAS', 'Five-Seven', 'G3SG1', 'Galil AR', 'Glock-18', 'M249', 'M4A1-S', 'M4A4', 'MAC-10',
#                'MAG-7', 'MP7', 'MP9', 'Negev', 'Nova', 'P2000', 'P250', 'P90', 'PP-Bizon', 'R8 Revolver', 'SCAR-20', 'SG 553', 'SSG 08', 'Sawed-Off', 'Tec-9', 'UMP-45', 'USP-S', 'XM1014']

# chooseKnifeButton = tk.Button(scwindow, text='Knife', command=lambda: knifeSkinDropDown.showDropDown(gunSkinDropDown), font=("Bahnschrift Light", 18, 'bold'), bd=4, padx=30)
# chooseKnifeButton.grid(row=2, column=0, sticky='E', padx=20)
# chooseGunButton = tk.Button(scwindow, text='Gun', command=lambda: gunSkinDropDown.showDropDown(knifeSkinDropDown), font=("Bahnschrift Light", 18, 'bold'), bd=4, padx=30)
# chooseGunButton.grid(row=2, column=1, sticky='W', padx=20)

# searchInput = tk.StringVar()
# searchInput.set('Enter Custom Search')
# searchQuery = tk.Entry(scwindow,  bg=bgLightColor, font=("Bahnschrift SemiLight", 16), textvariable=searchInput)
# searchQuery.bind("<1>", lambda x: searchInput.set('') if searchInput.get() == 'Enter Custom Search' else None)
# searchQuery.bind("<Key>", searchQueryKeyPress())


# def m4a1_min_test():
#     filename = 'C:/Users/Jakob/Desktop/PyEnvs/myenv38progs/WebAutomation/SeleniumSkinScraper/m4a1_minwear.csv'
#     extraInfoFile = 'C:/Users/Jakob/Desktop/PyEnvs/myenv38progs/WebAutomation/SeleniumSkinScraper/m4a1_minwear_extra.txt'
#     # skin constants
#     gunType = 'M4A1-S'
#     gtLen = len(gunType)
#     wearType = 'Minimal Wear'
#     maxPages = 50
#     # skinsDict = {'Time': currentDT, 'Row': 0}

#     site_m4a1_min = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=tag_weapon_m4a1_silencer&category_730_Exterior%5B0%5D=tag_WearCategory1&appid=730#p1_price_asc'
#     currentDT = datetime.datetime.now()
#     currentDT = str(currentDT.year)[2:] + str(currentDT.month).zfill(2) + str(currentDT.day).zfill(2)+str(currentDT.hour)
#     skinsDict = {'Row': 0, 'Time': currentDT}

#     print('Starting Browser...')
#     driver = sssc.setupDriver(site_m4a1_min)
#     print('Scraping Pages...')
#     skinsDict = sssc.scrapeSkinPage(gunType, gtLen, wearType, skinsDict, maxPages, driver, isKnife, wearTypeDict)
#     if skinsDict == None:
#         print('No Skins found')
#     else:
#         sssc.checkCSVexists(filename)
#         print('Writing to CSV')
#         sssc.csvWork(skinsDict, filename)

# generalScrape(weaponCodeArg, weaponCodeArg,  wearArg, csvPathInput.fShlashText, skinLink)
