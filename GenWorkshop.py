import requests, sys

if len(sys.argv) == 1:
    print('Please supply collection ID')
    exit()

url = 'https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/'
data = {'collectioncount': 1, 'publishedfileids[0]': sys.argv[1]}

res = requests.post(url, data)

resJson = res.json()
collectionItems = resJson['response']['collectiondetails'][0]['children']

itemsUrl = 'https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/'
itemsData = {'itemcount': len(collectionItems)}

itemNum = 0
for item in collectionItems:
    itemsData.update({f'publishedfileids[{itemNum}]': item['publishedfileid']})
    itemNum += 1

itemsRes = requests.post(itemsUrl, itemsData)

f = open('workshop.lua', 'w')

itemNum = 0
for item in collectionItems:
    f.write('resource.AddWorkshop("' + item['publishedfileid'] + '") -- ' + itemsRes.json()['response']['publishedfiledetails'][itemNum]['title'])
    f.write('\n')
    itemNum += 1

f.close()