#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Krammy
#
# Created:     06/10/2019
# Copyright:   (c) Krammy 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import re
import sqlite3

conn = sqlite3.connect('lobbying2.db')
cur1 = conn.cursor()
cur2 = conn.cursor()

cur2.execute('''DROP TABLE IF EXISTS LPAY_to_LEXP''')

cur2.execute('''CREATE TABLE IF NOT EXISTS LPAY_to_LEXP (
id INTEGER PRIMARY KEY AUTOINCREMENT,
LPAY_ID INTEGER,
LEXP_ID INTEGER)''')

i = 0
for row in cur1.execute('''SELECT LPAY.ID, LEXP.ID
FROM LPAY
JOIN LEXP on LPAY.filing_id = LEXP.filing_id;'''):

    LPAY_id = row[0]
    LEXP_id = row[1]
    try:
        cur2.execute('''INSERT INTO LPAY_to_LEXP
        (LPAY_ID, LEXP_ID) VALUES (?, ?)''', (LPAY_id, LEXP_id, ))
        print("inserting", LPAY_id, " ", LEXP_id)
    except:
        continue
    i += 1
    if i > 50:
        conn.commit()
