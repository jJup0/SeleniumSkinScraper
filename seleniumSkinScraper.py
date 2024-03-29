import csv
import datetime
import os
import time
from typing import Any, Mapping

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By

cwd = os.path.dirname(__file__)

op = webdriver.ChromeOptions()
op.add_argument("headless")  # type: ignore # unknown
driver: webdriver.Chrome = webdriver.Chrome(options=op)


def scrapeSkinPage(
    gunType: str,
    gtLen: int,
    wearTypes: list[str],
    skinsDict: dict[str, Any],
    nrOfPages: int,
    driver: webdriver.Chrome,
    isKnife: bool,
    wearTypeDict: Mapping[str, tuple[str, int]],
):
    try:
        for _ in range(nrOfPages):
            time.sleep(0.5)
            skins_web_elements = []
            while not skins_web_elements:
                no_more_items_elements = driver.find_elements(
                    By.CLASS_NAME, "market_listing_table_message"
                )
                if no_more_items_elements:
                    return

                time.sleep(0.1)
                skins_web_elements = driver.find_elements(
                    By.CLASS_NAME,
                    "market_listing_row.market_recent_listing_row.market_listing_searchresult",
                )

            skinNames: list[str] = []
            for skin in skins_web_elements:
                skinNames.append(skin.get_attribute("data-hash-name"))  # type: ignore #unknown
            knDisp = 2 if isKnife else 0  # knifes have start in their name
            for i in range(len(skinNames)):
                curS = skinNames[i]
                isPainted = True
                wearType = shortWearType = ""
                for localwtype in wearTypes:
                    if curS.find(localwtype) != -1:
                        wearType = localwtype
                        shortWearType = wearTypeDict[wearType][0]
                        break
                    isPainted = False

                if isPainted:
                    if curS.find("StatTrak") != -1:
                        curS = (
                            curS[knDisp : 8 + knDisp]
                            + curS[gtLen + knDisp + 12 : curS.find(wearType) - 2]
                            + " "
                            + shortWearType
                        )  # include stattrak or souvenir in name, ignore weapon
                    elif curS.find("Souvenir") != -1:
                        curS = (
                            curS[:8]
                            + curS[gtLen + 11 : curS.find(wearType) - 2]
                            + " "
                            + shortWearType
                        )
                    else:
                        curS = (
                            curS[gtLen + knDisp + 3 : curS.find(wearType) - 2]
                            + " "
                            + shortWearType
                        )
                else:
                    if curS.find("StatTrak") != -1:
                        curS = (
                            curS[knDisp : 8 + knDisp]
                            + curS[gtLen + knDisp + 12 : curS.find(wearType) - 2]
                        )
                    else:
                        curS = curS[knDisp:]

                skinNames[i] = curS

            skinPrices: list[float] = []
            skinPricesWE = driver.find_elements(By.CLASS_NAME, "normal_price")
            for spWE in skinPricesWE:
                skinPrice = spWE.get_attribute("data-price")  # type: ignore #unknown
                if skinPrice:
                    skinPrices.append(int(skinPrice) / 100)

            for name, price in zip(skinNames, skinPrices, strict=True):
                skinsDict[name] = price

            try:
                lastItemNr = driver.find_element(By.ID, "searchResults_end")
                totalItemNr = driver.find_element(By.ID, "searchResults_total")
                if lastItemNr.get_attribute("innerHTML") == totalItemNr.get_attribute("innerHTML"):  # type: ignore #unknown
                    print("Scraped last page")
                    break
            except:
                print("Something went wrong, probably no results")
            click_attempt = 0
            for click_attempt in range(5):
                # try to click 10 times
                try:
                    nextPageButtonWE = driver.find_element(
                        By.ID, "searchResults_btn_next"
                    )
                    # print(nextPageButtonWE.get_attribute('innerHTML'))
                    nextPageButtonWE.click()
                    print("Continuing to next page")
                except selenium.common.exceptions.ElementClickInterceptedException:
                    print("Failed to click, trying again")
                    reject_cookies_button = driver.find_elements(
                        By.ID, "rejectAllButton"
                    )
                    if reject_cookies_button:
                        reject_cookies_button[0].click()
                    pass
            if click_attempt == 4:
                print("failed to click 5 times, saving html")
                with open("temp.html", "wb") as f:
                    f.write(driver.page_source.encode("utf-8", "ignore"))

    except KeyboardInterrupt:
        pass
    return skinsDict


# csv prep
def checkCSVexists(skinsDict: dict[str, Any], CSVFileName: str):
    try:
        with open(CSVFileName):
            print("File Exists")
    except IOError:
        print("CSV File Doesn't exist yet")
        with open(CSVFileName, "w+", newline="") as csvf:
            csvWriter = csv.writer(csvf, delimiter=",")
            csvWriter.writerow(list(skinsDict.keys()))
            # csvWriter.writerow([1, currentDT] + allSkinPrices)


def csvWork(skinsDict: dict[str, Any], CSVFileName: str, extraInfoFileName: str = ""):
    # with open(extraInfoFileName, 'r+') as extratxt:
    #     totalRows = str(int(extratxt.readline())+1)
    #     extratxt.seek(0)
    #     extratxt.write(totalRows)
    with open(CSVFileName, "r") as csvf:
        csvReader = csv.reader(csvf, delimiter=",")
        skinHeaders = next(csvReader)
        lastrow = skinHeaders.copy()  # idk y, dont know if i shouldnt just: = ''
        for row in csvReader:
            lastrow = row
        totalRows = lastrow[0]

    skinsDict["Row"] = totalRows  # type: ignore #
    with open(CSVFileName, "a", newline="") as csvf:
        csvWriter = csv.DictWriter(csvf, fieldnames=skinHeaders, delimiter=",")
        csvWriter.writerow(skinsDict)


def generalScrape(
    weaponName: str,
    wearTypesArr: list[str],
    csvFilepath: str,
    skinLink: str,
    isKnife: bool,
    wearTypesDict: Mapping[str, tuple[str, int]],
):
    print("*" * 100)
    print("*" * 100)
    maxPages = 10
    wnLen = len(weaponName)
    # print(weaponName)
    # print(wnLen)

    currentDT = datetime.datetime.now()
    currentDT = (
        str(currentDT.year)[2:]
        + str(currentDT.month).zfill(2)
        + str(currentDT.day).zfill(2)
        + str(currentDT.hour)
    )
    skinsDict = {"Row": 0, "Time": currentDT}

    print("Starting Browser...")
    driver.get(skinLink)
    print("Scraping Pages...")
    skinsDict = scrapeSkinPage(
        weaponName,
        wnLen,
        wearTypesArr,
        skinsDict,
        maxPages,
        driver,
        isKnife,
        wearTypesDict,
    )
    if skinsDict == None:
        print("No Skins found")
        return 0
    # print(skinsDict)
    checkCSVexists(skinsDict, csvFilepath)
    print("Writing to CSV")
    csvWork(skinsDict, csvFilepath)
    return len(skinsDict) - 2
