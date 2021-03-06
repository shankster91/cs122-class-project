'''
This file counts the number of variables from each table in zip_db.sqlite3. It
also counts the number of bins in each Census distribution.
Finally, both sets of counts are written to text files.
'''

import sqlite3
import json


table_counts = {'census' : 0, 'business' : 0, 'school' : 0, 'votes' : 0,
                'libraries' : 0, 'museums' : 0, 'walk' : 0, 'weather' : 0,
                'property' : 0}
census_dist_counts = {'age' : 0, 'sex': 0, 'educ' : 0, 'income' : 0,
                      'marital' : 0, 'race' : 0, 'language' : 0,
                      'birthPlace' : 0, 'HHsize' : 0, 'housing' : 0,
                      'lastMove' : 0, 'popDensity' : 0, 'unemployment' : 0,
                      'lfpr' : 0,}

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
    words = col.split('_')
    table = words[0]
    if table == 'census':
        var = words[1]
    if table != col:
        table_counts[table] += 1
        if table == 'census':
            census_dist_counts[var] += 1

# Count the total number of Census variables. (The above number is not valid
# because it counts the total number of bins, not variables.)
table_counts['census'] = len(census_dist_counts)

with open('algorithm/table_counts.txt','w') as f:
    f.write(json.dumps(table_counts))

with open('algorithm/census_dist_counts.txt','w') as f:
    f.write(json.dumps(census_dist_counts))
