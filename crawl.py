import datetime

import pandas as pd
import requests
from lxml import html


# the last update on 09/18/2019

def phone_ranking(top=10):
    url = 'https://www.dxomark.com/category/mobile-reviews/'
    page = requests.Session().get(url)
    tree = html.fromstring(page.text)
    scores = tree.xpath('//div[@class="deviceScore"]/text()')
    phones = tree.xpath('//div[@class="deviceName sensor"]//a/text()')
    links = tree.xpath('//div[@class="deviceName sensor"]//a/@href')

    record = {}  # rank by photo score
    results = []  # for result display
    for i in range(top):
        score = scores[i]
        phone = phones[i]
        link = links[i]
        page = requests.Session().get(link)
        tree = html.fromstring(page.text)

        photo_score = tree.xpath('//div[@class="chart-container bars photo "]//div/@data-score')[0]
        photo_detail = tree.xpath('//div[@class="chart-container bars photo "]//div/@data-array')[0]
        photo_detail = [int(x) if 'n/a' not in x else '-' for x in photo_detail.split(',')]
        video_score = tree.xpath('//div[@class="chart-container bars video "]//div/@data-score')[0]
        video_detail = tree.xpath('//div[@class="chart-container bars video "]//div/@data-array')[0]
        video_detail = [int(x) if 'n/a' not in x else '-' for x in video_detail.split(',')]
        front_link = tree.xpath('//div[@class="protocolsNav"]//li[@class="selfie"]//@href')
        if len(front_link) > 0:
            front_link = tree.xpath('//div[@class="protocolsNav"]//li[@class="selfie"]//@href')[0]
            page = requests.Session().get(front_link)
            tree = html.fromstring(page.text)
            selfie = tree.xpath('//div[@class="scoreBadge selfie"]//div[@class="scoreBadgeValue"]/text()')
            selfie = selfie[0] if len(selfie) > 0 else '-'
        else:
            selfie = '-'

        if int(photo_score) in record:
            record[int(photo_score)].append(phone)
        else:
            record[int(photo_score)] = [phone]
        if len(selfie) > 1:
            total = int(photo_score) + int(selfie) + int(video_score)
        else:
            total = '-'
        photo_video = int(photo_score) + int(video_score)
        detail = [phone, score, photo_score, selfie, video_score, photo_video, total]
        results.append(detail)

    date = datetime.date.today()
    path = 'output/DXOMARK_' + str(date) + '.txt'
    save_to_file(path, results, record)
    return results, record


def save_to_file(path, results, record):
    display = pd.DataFrame(results, columns=['model', 'overall', 'photo', 'selfie', 'video', 'p+v', 'p+s+v'])
    print(display)
    display.to_csv(path, sep='\t')

    display.index += 1
    fos = open(path, 'a+', encoding='utf-8')
    res = '\nrank by photo score'
    fos.write(res + '\n')
    fos.flush()
    rank_by_photo = sorted(record)[:: -1]
    for i, r in enumerate(rank_by_photo):
        res = '{0}\t{1}\t{2}'.format(i + 1, r, record[r])
        print(res)
        fos.write(res + '\n')
        fos.flush()
    fos.close()


phone_ranking(15)
