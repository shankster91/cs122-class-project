
'''
Scraping GreatSchools.org for average rating of list of schools by zip code
'''

import bs4
import requests
import urllib3
import certifi
import csv
import json
import re
       
req = requests.get("https://www.greatschools.org/search/search.zipcode?sort=rating&view=table&zip=02136")

soup2 = bs4.BeautifulSoup(req.text)

tag_list2 = soup2.find(id = "search-page")

soup2.find(id = "Search-react-component-ad65c5fa-112b-466c-9e2b-788a1aacd3bc").find_all("section", class_ = 'school-list')




clean_string = str(soup2.find_all("script", type = "text/javascript")[0]).replace('<script type="text/javascript">\n//<![CDATA[\n', "").replace(";\n//]]>\n</script>","")


data_layer = clean_string[clean_string.find('gon.search'):]
school_string = data_layer.replace('gon.search={"schools":[', "")

re.findall(r'{"id":', school_string)
re.search(r'{"id":[^{"id:"}]*', school_string)



one_school = '''{"id":340,"districtId":99,"districtName":"Boston School District","districtCity":"Boston","levelCode":"h","lat":42.262688,"lon":-71.117836,"name":"New Mission High School","gradeLevels":"9-12","assigned":null,"address":{"street1":"655 Metropolitan Avenue","street2":"","zip":"02136","city":"Boston"},"csaAwardYears":[],"rating":6,"ratingScale":"Average","schoolType":"public","state":"MA","zipcode":"02136","type":"school","links":{"profile":"/massachusetts/boston/340-New-Mission-High-School/","reviews":"/massachusetts/boston/340-New-Mission-High-School/#Reviews","collegeSuccess":"/massachusetts/boston/340-New-Mission-High-School/#College_success"},"highlighted":false,"pinned":null,"testScoreRatingForEthnicity":null,"percentLowIncome":"63%","collegePersistentData":{"school_value":"67%","state_average":"87%"},"collegeEnrollmentData":{"school_value":"85%","state_average":"70%"},"enrollment":392,"parentRating":4,"numReviews":4,"studentsPerTeacher":14,"subratings":{"Test Scores Rating":4,"Student Progress Rating":9,"College Readiness Rating":5,"Equity Overview Rating":5},"ethnicityInfo":[{"label":"Low-income","rating":4,"percentage":63},{"label":"All students","rating":4},{"label":"African American","rating":4,"percentage":60},{"label":"Hispanic","rating":4,"percentage":35},{"label":"White","percentage":2},{"label":"Two or more races","percentage":2},{"label":"Asian","percentage":1}],"remediationData":{"Overall":[{"data_type":"Percent Needing any Remediation for College","subject":"Any Subject","school_value":"17%","state_average":"24%"}]}} '''
