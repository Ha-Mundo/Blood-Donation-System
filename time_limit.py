import datetime


#print(datetime.now())

donation_day = datetime.datetime.now()

print(donation_day)

threshold = datetime.timedelta(seconds=60) 

print(threshold)

print(donation_day + threshold)


def threshold_time(donation_day):
    #donation_day = datetime.datetime.now()
    threshold = datetime.timedelta(seconds=60)
    till_day =  donation_day + threshold
    #print(till_day)
    return till_day

condition = threshold_time(donation_day)  

def timer(condition, donation_day):   
    if condition <= donation_day:
       return True
    else:
        return False

t = timer(condition, donation_day)
print(t)


