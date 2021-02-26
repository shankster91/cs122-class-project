'''
This file contains the algorithm that computes the sum of squared differences
between the attributes of a user-specified zip code and the attributes of each
zip code in a user-specified state. The algorithm then selects the five zip
codes in that state that are most similar to the user-specified zip code
(i.e. it selects the five zip codes with the smallest sum of squared differences).
'''

def get_zip_data(state=None, zip_code=None):
    '''
    INSET HEADER
    '''
    preamble = '''SELECT * 
                  FROM census AS c
                  JOIN business_count AS b
                  JOIN ideology AS i
                  JOIN libraries AS l
                  JOIN museums AS m
                  JOIN walk_score AS w
                  JOIN zillow AS z
                  ON c.zip = b.zip = i.zip = l.zip = m.zip = w.zip = z.zip'''
    arg_lst = []
    state_condition = ""
    connector = ""
    zip_condition = ""
    if state:
        state_condition = "WHERE state = ?"
        arg_lst.append(state)
        if zip_code:
            connector = "AND"
    if zip_code:
        zip_condition = "WHERE zip = ?"
        arg_lst.append(zip_code)
    sql_query = " ".join([preamble, state_condition, connector, zip_condition, ";"])
    return (sql_query, tuple(arg_lst))

    # try all four types of searches




# headers
# eliminate the specifid zip code form the output list
# weights on different aspects
