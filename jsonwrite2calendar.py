import json

calendar = dict()      # create dictionary

calendar['muslim'] = 'y - 622 + ((y-622)/32)'        # fill the structure with data
calendar['JDN'] = 'd + ((153 * m + 2) / 5) + (365 * y) + (y / 4) - (y / 100) + (y / 400) - 32045'
calendar['value'] = ('y','m', 'd')

with open('basic1.json', mode='w', encoding='utf-8') as f:                # open the file for writing in utf-8
    json.dump(calendar, f, indent=2,  ensure_ascii = False, sort_keys=False)         # write data to file with parameters

print(calendar)