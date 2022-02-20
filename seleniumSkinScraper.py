from selenium import webdriver
import csv
import time
import sys


def setupDriver(siteName):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    # driver = webdriver.Chrome()
    driver.get(siteName)
    return driver


def scrapeSkinPage(gunType, gtLen, wearTypes, skinsDict, nrOfPages, driver, isKnife, wearTypeDict):
    # try:
    #     disableButton = driver.find_element_by_class_name('market_listing_table_message')
    #     return
    # except:
    #     pass

    for _ in range(nrOfPages):
        time.sleep(0.5)
        skinsWE = []
        while not skinsWE:
            try:
                driver.find_element_by_class_name('market_listing_table_message')
                print('Scraped last Page')
                driver.close()
                return
            except:
                pass
            print('fetching skins')
            time.sleep(0.1)
            skinsWE = driver.find_elements_by_class_name("market_listing_row.market_recent_listing_row.market_listing_searchresult")

        skinNames = []
        for skin in skinsWE:
            skinNames.append(skin.get_attribute("data-hash-name"))
        knDisp = 2 if isKnife else 0  # knifes have start in their name
        for i in range(len(skinNames)):
            curS = skinNames[i]
            for localwtype in wearTypes:
                isPainted = True
                if curS.find(localwtype) != -1:
                    wearType = localwtype
                    shortWearType = wearTypeDict[wearType][0]
                    break
                isPainted = False

            if isPainted:
                if curS.find('StatTrak') != -1:
                    curS = curS[knDisp:8+knDisp] + curS[gtLen+knDisp+12:curS.find(wearType) - 2] + ' ' + shortWearType  # include stattrak or souvenir in name, ignore weapon
                elif curS.find('Souvenir') != -1:
                    curS = curS[:8] + curS[gtLen+11:curS.find(wearType) - 2] + ' ' + shortWearType
                else:
                    curS = curS[gtLen+knDisp+3:curS.find(wearType) - 2] + ' ' + shortWearType
            else:
                if curS.find('StatTrak') != -1:
                    curS = curS[knDisp:8+knDisp] + curS[gtLen+knDisp+12:curS.find(wearType) - 2]
                else:
                    curS = curS[knDisp:]

            skinNames[i] = curS

        skinPrices, skinPricesWE = [], driver.find_elements_by_class_name("normal_price")
        for spWE in skinPricesWE:
            skinPrice = (spWE.get_attribute('data-price'))
            if skinPrice:
                skinPrices.append(int(skinPrice)/100)

        if len(skinPrices) != len(skinNames):
            sys.exit('DIFFERENT AMOUNT OF SKINS AND PRICES')

        for name, price in zip(skinNames, skinPrices):
            skinsDict[name] = price

        try:
            lastItemNr = driver.find_element_by_id('searchResults_end')
            totalItemNr = driver.find_element_by_id('searchResults_total')
            if lastItemNr.get_attribute('innerHTML') == totalItemNr.get_attribute('innerHTML'):
                print('last page')
                break
            else:
                print('not last page')
        except:
            print('prob no results')
        try:
            nextPageButtonWE = driver.find_element_by_id('searchResults_btn_next')
            # print(nextPageButtonWE.get_attribute('innerHTML'))
            nextPageButtonWE.click()
        except:
            print('shid')
            break
    driver.close()
    return skinsDict


# csv prep
def checkCSVexists(skinsDict, CSVFileName):
    try:
        with open(CSVFileName):
            print('File Exists')
    except IOError:
        print('CSV File Doesn\'t exist yet')
        with open(CSVFileName, 'w+', newline='') as csvf:
            csvWriter = csv.writer(csvf, delimiter=',')
            csvWriter.writerow(list(skinsDict.keys()))
            # csvWriter.writerow([1, currentDT] + allSkinPrices)


def csvWork(skinsDict, CSVFileName, extraInfoFileName=''):
    # with open(extraInfoFileName, 'r+') as extratxt:
    #     totalRows = str(int(extratxt.readline())+1)
    #     extratxt.seek(0)
    #     extratxt.write(totalRows)
    with open(CSVFileName, 'r') as csvf:
        csvReader = csv.reader(csvf, delimiter=',')
        skinHeaders = next(csvReader)
        lastrow = skinHeaders.copy()        #idk y, dont know if i shouldnt just: = ''
        for row in csvReader:
            lastrow = row
        totalRows = lastrow[0]

    skinsDict['Row'] = totalRows
    with open(CSVFileName, 'a',  newline='') as csvf:
        csvWriter = csv.DictWriter(csvf, fieldnames=skinHeaders, delimiter=',')
        csvWriter.writerow(skinsDict)
