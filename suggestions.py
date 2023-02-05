from mlmodel import averages
from rank import data

messeges = ['''Your CO2 emissions were higher than average, try to cut down on 
            your emissions for a better rating.''',
            '''Your percentage of foreign imports of materials was higher than 
            average, try to source materials nationally for a better rating.''',
            '''Your percentage of reusable materials was lower than average, 
            try to find more sustainable materials for a better rating.''',
            ''' Your CO2 emissions and percentage of foreign imports were both 
            lower than average, and your percentage of reusable materials was 
            higher than average. You're company is sustainable! Keep it up!''']




company = data[0]
returnmessege = ''

if company[1] < averages[0] & company[2] < averages[1] & company[3] > averages[2]:
    returnmessege = messeges[3]
else:
    for i in range(0,3):
        if i+1 == 3:
            if company[i+1] < averages[i]:
                returnmessege = messeges[i]
        else:
            if company[i+1] > averages[i]:
                returnmessege = messeges[i]
    