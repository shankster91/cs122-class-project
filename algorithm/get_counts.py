'''
This file counts the number of variables from each table in zip_db.sqlite3. It
also counts the number of bins in each Census distribution.
Finally, both sets of counts are written to text files.
'''

import sqlite3
import re
import json


table_counts = {'census' : 0, 'business' : 0, 'school' : 0, 'votes' : 0,
                'libraries' : 0, 'museums' : 0, 'walk' : 0, 'weather' : 0,
                'property' : 0}
census_dist_counts = {'age_' : 0, 'sex': 0, 'educ' : 0, 'income' : 0,
                      'marital' : 0, 'race' : 0, 'language' : 0,
                      'birth_place' : 0, 'occupied_housing' : 0, 'last_move' : 0}

conn = sqlite3.connect('zip_db.sqlite3')
sql_query = '''SELECT * FROM census
               JOIN business_count USING (zip)
               JOIN great_schools USING (zip)
               JOIN ideology USING (zip)
               JOIN libraries USING (zip)
               JOIN museums USING (zip)
               JOIN walk_score USING (zip)
               JOIN weather USING (zip)
               JOIN zillow USING (zip)'''
cursor = conn.execute(sql_query)
col_names = [description[0] for description in cursor.description]
conn.close()

for col in col_names:
    for table in table_counts:
        if col.startswith(table):
            table_counts[table] += 1
            break
    if table == 'census':
        for var in census_dist_counts:
            if re.search(var, col):
                census_dist_counts[var] += 1
                break

# Count the total number of Census variables by taking the number of columns,
# subtracting the total number of bins in the Census distributions, and adding
# back the number of Census variables that have distributions.
table_counts['census'] += len(census_dist_counts) - sum(census_dist_counts.values())

with open('algorithm/table_counts.txt','w') as f:
    f.write(json.dumps(table_counts))

with open('algorithm/census_dist_counts.txt','w') as f:
    f.write(json.dumps(census_dist_counts))
