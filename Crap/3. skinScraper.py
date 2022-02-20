from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import csv
import time


# skin constants
gunType = 'M4A1-S'
gtLen = len(gunType)
wearType = 'Minimal Wear'

# csv prep
filename = 'm4a1_skins.csv'
with open(filename, 'w') as csvf:
    headers = ['Guntype', 'Wear', 'Special_type', 'Skin_name', 'Price']
    csvWriter = csv.DictWriter(csvf, fieldnames=headers, delimiter=',')
    csvWriter.writeheader()

# with open('new_names.csv', 'w', newline='') as new_csv_file:
#     csv_writer = csv.DictWriter(new_csv_file, fieldnames=myFieldNames, delimiter=',')

#     csv_writer.writeheader()
#     for eachLine in csv_reader:
#         del eachLine['email']
#         csv_writer.writerow(eachLine)

for x in range(1, 2):
    # html prep
    url_m4a1_bloodtiger = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=tag_weapon_m4a1_silencer&category_730_Exterior%5B0%5D=tag_WearCategory1&category_730_Rarity%5B0%5D=tag_Rarity_Rare_Weapon&appid=730#p' + \
        str(x) + '_price_asc'
    # print(url_m4a1_bloodtiger)
    uClient = uReq(url_m4a1_bloodtiger)
    time.sleep(2)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, 'html.parser')

    all_skins = page_soup.findAll('a', {'class': "market_listing_row_link"})
    print(len(all_skins))
    for skin in all_skins:
        skin_name = skin.div['data-hash-name']
        # remove wear from name
        skin_name = skin_name[:skin_name.find(wearType) - 2]

        if skin_name.find('StatTrak™') != -1:
            skin_name = skin_name[gtLen+13:]
            specialT = 'StatTrak'
        elif skin_name.find('Souvenir') != -1:
            skin_name = skin_name[gtLen+12:]
            specialT = 'Souvenir'
        else:
            skin_name = skin_name[gtLen+3:]
            specialT = ''

        skin_price_obj = skin.find('span', {'class': 'normal_price'}).span
        skin_price = int(skin_price_obj['data-price'])/100
        with open(filename, 'a') as csvf:
            csvf.write(gunType + ',' + wearType + ',' + specialT + ',' + skin_name + ',' + str(skin_price) + '\n')
            # csvWriter.writerow(gunType + ',' + wearType + ',' + specialT + ',' + skin_name + ',' + str(skin_price) + '\n')


# f.close()
