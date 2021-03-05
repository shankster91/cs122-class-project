import sqlite3
import csv


def generate_lists():

    connection = sqlite3.connect('../../../zip_db.sqlite3')
    c = connection.cursor()

    # get lists of unique values from sql database
    zip_codes = c.execute('''SELECT DISTINCT zip FROM census''').fetchall()
    states = c.execute('''SELECT DISTINCT state FROM census''').fetchall()
    zip_codes.sort()
    states.sort()

    connection.close()

    # write lists of unique values to file
    f = open('zip_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in zip_codes:
        w.writerow(row)
    f.close()

    f = open('state_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in states:
            w.writerow(row)
    f.close()