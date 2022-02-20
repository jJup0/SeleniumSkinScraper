from selenium import webdriver
import csv
import time
import sys
import os
import datetime

currentDT = datetime.datetime.now()
currentDT = str(currentDT.year)[2:] + str(currentDT.month).zfill(2) + str(currentDT.day).zfill(2)+str(currentDT.hour)

filename = 'C:/Users/Jakob/Desktop/PyEnvs/myenv38/myenv38progs/WebAutomation/m4a1_minwear.csv'
try:
    with open(filename) as csvf:
        sys.exit('CSV file exists')
except IOError:
    print('Ready for init')


# skin constants
gunType = 'M4A1-S'
gtLen = len(gunType)
wearType = 'Minimal Wear'
nrOfPages = 5

# -----------------------------------------------------
siteName = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=tag_weapon_m4a1_silencer&category_730_Exterior%5B0%5D=tag_WearCategory1&appid=730#p1_price_asc'
driver = webdriver.Chrome()
driver.get(siteName)
allSkinNames = []
allSkinPrices = []
for i in range(nrOfPages):
    time.sleep(0.5)
    skinsWE = []
    while not skinsWE:
        print('fetching skins')
        skinsWE = driver.find_elements_by_class_name("market_listing_row.market_recent_listing_row.market_listing_searchresult")
        time.sleep(0.1)
    skinNames = []
    for skin in skinsWE:
        skinNames.append(skin.get_attribute("data-hash-name"))
    for i in range(len(skinNames)):
        curS = skinNames[i]
        if curS.find('StatTrak') != -1:
            curS = curS[:8] + curS[gtLen+12:curS.find(wearType) - 2]
        elif curS.find('Souvenir') != -1:
            curS = curS[:8] + curS[gtLen+11:curS.find(wearType) - 2]
        else:
            curS = curS[gtLen+3:curS.find(wearType) - 2]
        skinNames[i] = curS
    allSkinNames += skinNames

    skinPrices, skinPricesWE = [], driver.find_elements_by_class_name("normal_price")
    for spWE in skinPricesWE:
        skinPrice = (spWE.get_attribute('data-price'))
        if skinPrice:
            skinPrices.append(int(skinPrice)/100)
    allSkinPrices += skinPrices

    if len(skinPrices) != len(skinNames):
        sys.exit('DIFFERENT AMOUNT OF SKINS AND PRICES')

    nextPageButtonWE = driver.find_element_by_id('searchResults_btn_next')
    nextPageButtonWE.click()
driver.close()

with open(filename, 'w+', newline='') as csvf:
    print("Writing skin names")
    csvWriter = csv.writer(csvf, delimiter=',')
    csvWriter.writerow(['Row', 'Time'] + allSkinNames)
    csvWriter.writerow([1, currentDT] + allSkinPrices)
