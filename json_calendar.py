import json

calendar = dict()      # create dictionary
JDN = dict()           # create subdictionaries
nepal = dict() 

calendar['value'] = ('y','m', 'd')   # tuple, constant`s list

calendar['muslim'] = 'y - 622 + ((y-622)//32)'        # fill the structure with data
calendar['mongol'] = 'y - 1910'
calendar['bengal'] = 'y + 593'
calendar['thai'] = 'y + 543'

calendar['nepal'] = nepal
nepal['day'] = 'd + 15'
nepal['month'] = 'm + 8'
nepal['year'] = 'y + 56'

calendar['JDN'] = JDN
JDN['JDNnum'] = 'd + ((153 * m + 2) // 5) + (365 * y) + (y // 4) - (y //100) + (y // 400) - 32045'
JDN['JDNc'] = 'JDNnum + 32082'
JDN['JDNd'] = '(JDNc*4 + 3)//1461'
JDN['JDNe'] = 'JDNc - (1461*JDNd)//4'
JDN['JDNm'] = '(5*JDNe+2)//153'
JDN['JDNday'] = 'JDNe - ((153*JDNm +2)//5) +1'
JDN['JDNmonth'] = 'JDNm + 3 - 12*(JDNm//10)'
JDN['JDNyear'] = 'JDNd - 4800 + (JDNm//10)'
                                      
with open('calendar.json', mode='w', encoding='utf-8') as f:                 # open the file for writing in utf-8
    json.dump(calendar, f, indent=2,  ensure_ascii = False, sort_keys=False)         # write data to file with parameters

print(calendar)
