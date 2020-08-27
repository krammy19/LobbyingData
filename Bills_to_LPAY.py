#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krammy
#
# Created:     23/08/2019
# Copyright:   (c) Krammy 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import re
import sqlite3

def split_bill(billpackage):
    AB = False
    SB = False
    print("0:", billpackage)
    legislature_bills = []
    other_words = []
    list = re.findall('[AaSsBb]{0,2}[Ss]?\W?\s?\d{1,4}', billpackage)

# ------ this is for later when ready to add other text
#    other_words = (re.sub('[AaSsBb]{0,2}[Ss]?\W?\s?\d{1,4}',"", billpackage))
#    words = re.sub('^\W*',"", ("".join(other_words)))
#--------
    for item in list:
        item = (re.sub('\W',"", item)).strip()
        if item.startswith(('AB', 'Ab', 'ab')):
            AB = True
            SB = False
            item = (re.sub('\D',"",item)).strip()
            item = item.lstrip("0")
            item = "AB " + item
            legislature_bills.append(item)
        elif item.startswith(('SB', 'Sb', 'sb')):
            SB = True
            AB = False
            item = (re.sub('\D',"",item)).strip()
            item = item.lstrip("0")
            item = "SB " + item
            legislature_bills.append(item)
        elif item.isdigit():
            item = item.lstrip("0")
            if AB: legislature_bills.append("AB " + item)
            if SB: legislature_bills.append("SB " + item)
    return legislature_bills #,words

def leg_year(date):
    date = date.strip()
    if int(date) % 2 == 0:
        date = str(int(date)-1) + "-" + date
    else:
        date = date + "-" + str(int(date)+1)
    return(date)


conn = sqlite3.connect('lobbying2.db')
cur1 = conn.cursor()
cur2 = conn.cursor()

cur2.execute('''DROP TABLE IF EXISTS Bills_to_LPAY''')

cur2.execute('''CREATE TABLE IF NOT EXISTS Bills_to_LPAY (
id INTEGER PRIMARY KEY AUTOINCREMENT,
LPAY_ID INTEGER,
BILL_ID INTEGER)''')

i = 0
for row in cur1.execute('''SELECT LPAY.legislation, CVR_LOBBY_DISCLOSURE.Report_Date, LPAY.id
FROM CVR_LOBBY_DISCLOSURE
JOIN LPAY on CVR_LOBBY_DISCLOSURE.filing_id = LPAY.filing_id;'''):
    list = split_bill(row[0])
    year = leg_year(row[1])
    lpay_id = int(row[2])
    if list is not None:
        for bill in list:
            try:
                cur2.execute('''SELECT Bills.id FROM Bills
            WHERE Bill = ? AND Year = ?''', (bill, year,))
                bill_id = cur2.fetchone()[0]
                cur2.execute('''INSERT INTO Bills_to_LPAY
        (LPAY_ID, BILL_ID) VALUES (?, ?)''', (lpay_id, bill_id, ))
                print('IM ADDING ' + str(lpay_id), str(bill_id))
            except: continue
            i += 1
            if i > 50:
                conn.commit()
    conn.commit()