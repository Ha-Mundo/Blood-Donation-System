import datetime


#print(datetime.now())

donation_day = datetime.datetime.now()

print(donation_day)

threshold = datetime.timedelta(seconds=60) 

#print(threshold)

print(donation_day + threshold)

#bday = datetime.date()

#till_bday = bday - tday
#print(till_bday.days)

def threshold_time():
    donation_day = datetime.datetime.now()
    threshold = datetime.timedelta(seconds=60)
    till_day =  donation_day + threshold
    print(till_day)
    return till_day
    #if till_day == datetime.date.today():
        #return True
    #else:
        #print('Donation forbidden!')

#donation_permit(donation_day)


