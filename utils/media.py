import csv
import math

def calcola_media_stelle(file_path):
    total_stars = 0
    count = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            review_stars = row['review_stars'].strip().split(' ')[0]
            total_stars += float(review_stars.replace(',', '.'))
            count += 1

    if count > 0:
        media_stelle = total_stars / count
        media_stelle = math.floor(media_stelle * 10) / 10
        media_stelle -= 0.1
        media_stelle = math.floor(media_stelle * 10) / 10
        return media_stelle
    else:
        return 0

