'''
This file counts the number of variables from each table in zip_db.sqlite3. It
also counts the number of bins in each Census distribution.
Finally, it writes both sets of counts to text files.
'''

import sqlite3
import json


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

table_counts = {}
census_dist_counts = {}
for col in col_names:
    words = col.split('_')
    table = words[0]
    if table != col:
        table_counts[table] = table_counts.get(table, 0) + 1
        if table == 'census':
            var = words[1]
            census_dist_counts[var] = census_dist_counts.get(var, 0) + 1

# Count the total number of Census variables. (The above number is not valid
# because it counts the total number of bins instead of variables.)
table_counts['census'] = len(census_dist_counts)

with open('algorithm/table_counts.txt','w') as f:
    f.write(json.dumps(table_counts))

with open('algorithm/census_dist_counts.txt','w') as f:
    f.write(json.dumps(census_dist_counts))
