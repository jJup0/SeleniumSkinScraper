import seleniumSkinScraper as sssc
import datetime
from sys import exit


def generalScrape(weaponName, wearTypesArr, csvFilepath, skinLink, isKnife, wearTypesDict):
    print('*********************************************************************************************************')
    print('*********************************************************************************************************')
    maxPages = 50
    wnLen = len(weaponName)
    # print(weaponName)
    # print(wnLen)

    currentDT = datetime.datetime.now()
    currentDT = str(currentDT.year)[2:] + str(currentDT.month).zfill(2) + str(currentDT.day).zfill(2)+str(currentDT.hour)
    skinsDict = {'Row': 0, 'Time': currentDT}

    print('Starting Browser...')
    driver = sssc.setupDriver(skinLink)
    print('Scraping Pages...')
    skinsDict = sssc.scrapeSkinPage(weaponName, wnLen, wearTypesArr, skinsDict, maxPages, driver, isKnife, wearTypesDict)
    if skinsDict == None:
        print('No Skins found')
        return 0
    else:
        # print(skinsDict)
        sssc.checkCSVexists(skinsDict, csvFilepath)
        print('Writing to CSV')
        sssc.csvWork(skinsDict, csvFilepath)
        return len(skinsDict)
