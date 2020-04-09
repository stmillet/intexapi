import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'intexAPI.settings'
import django
django.setup()

from api.models import Campaign
import json

def main():
    import csv
    import json

    if len(Campaign.objects.all()) == 0:
        with open('campaigns.json') as json_file:
            data = json.load(json_file)
        campaigns = data
        id = 0
        for p in campaigns:
            theCamp = Campaign()
            theCamp.currencycode = campaigns[p]['currencycode']
            theCamp.current_amount = campaigns[p]['current_amount']
            theCamp.goal = campaigns[p]['goal']
            theCamp.auto_fb_post_mode = campaigns[p]['auto_fb_post_mode']
            theCamp.donators = campaigns[p]['donators']
            theCamp.days_active = campaigns[p]['days_active']
            theCamp.title = campaigns[p]['title']
            theCamp.description = campaigns[p]['description']
            theCamp.has_beneficiary = campaigns[p]['has_beneficiary']
            theCamp.status = campaigns[p]['status']
            theCamp.deactivated = campaigns[p]['deactivated']
            theCamp.campaign_hearts = campaigns[p]['campaign_hearts']
            theCamp.social_share_total = campaigns[p]['social_share_total']
            theCamp.location_country = campaigns[p]['location_country']
            theCamp.is_charity = campaigns[p]['is_charity']
            theCamp.charity_valid = campaigns[p]['charity_valid']
            if campaigns[p]['donators'] != '0':
                avg_donation = round((int(campaigns[p]['current_amount'])/int(campaigns[p]['donators'])), 2)
                theCamp.avg_donation = avg_donation
            else:
                avg_donation = 0
                theCamp.avg_donation = avg_donation

            theScore = 0
            if int(campaigns[p]['donators']) < 2:
                theScore += 0
            elif int(campaigns[p]['donators']) < 10:
                theScore += 0.5
            elif int(campaigns[p]['donators']) < 25:
                theScore += 1
            elif int(campaigns[p]['donators']) < 50:
                theScore += 1.5
            elif int(campaigns[p]['donators']) < 100:
                theScore += 2
            elif int(campaigns[p]['donators']) < 200:
                theScore += 2.5
            elif int(campaigns[p]['donators']) < 500:
                theScore += 3
            elif int(campaigns[p]['donators']) < 1000:
                theScore += 3.5
            elif int(campaigns[p]['donators']) < 2000:
                theScore += 4
            elif int(campaigns[p]['donators']) < 10000:
                theScore += 4.5
            elif int(campaigns[p]['donators']) > 10000:
                theScore += 5

            if int(avg_donation) < 5:
                theScore += 0
            elif int(avg_donation) < 10:
                theScore += 0.5
            elif int(avg_donation) < 15:
                theScore += 1
            elif int(avg_donation) < 20:
                theScore += 1.5
            elif int(avg_donation) < 30:
                theScore += 2
            elif int(avg_donation) < 50:
                theScore += 2.5
            elif int(avg_donation) < 75:
                theScore += 3
            elif int(avg_donation) < 125:
                theScore += 3.5
            elif int(avg_donation) < 200:
                theScore += 4
            elif int(avg_donation) < 500:
                theScore += 4.5
            elif int(avg_donation) > 500:
                theScore += 5
            theCamp.c_rating = theScore




            theCamp.save()
            print(p, theScore)
    else:
        print('Already loaded')







    # csvFilepath = 'Intex.csv'
    # jsonFilePath = 'campaigns.json'

    # data = {}
    # print('hello')

    # with open(csvFilepath) as csvFile:
    #     csvReader = csv.DictReader(csvFile)
    #     id = 0
    #     for rows in csvReader:
            
    #         data[id] = { 'currencycode': rows['currencycode'],
    #                     'current_amount': rows['current_amount'],
    #                     'goal': rows['goal'],
    #                     'auto_fb_post_mode': rows['auto_fb_post_mode'],
    #                     'donators': rows['donators'],
    #                     'days_active': rows['days_active'],
    #                     'title': rows['title'],
    #                     'description': rows['description'],
    #                     'has_beneficiary': rows['has_beneficiary'],
    #                     'status': rows['status'],
    #                     'deactivated': rows['deactivated'],
    #                     'campaign_hearts': rows['campaign_hearts'],
    #                     'social_share_total': rows['social_share_total'],
    #                     'location_country': rows['location_country'],
    #                     'is_charity': rows['is_charity'],
    #                     'charity_valid': rows['charity_valid']
    #         }
    #         id = id + 1
    # with open(jsonFilePath, 'w') as jsonFile:
    #     jsonFile.write(json.dumps(data, indent=4))



if __name__ == '__main__':
    main()