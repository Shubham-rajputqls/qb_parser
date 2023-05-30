from bs4 import BeautifulSoup
import json
import re
file = open("AN 100-114.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
next_div = soup.find('div')
# print(next_div)
QUESTION_TITTLE = "Short Answer Type Questions-"
# ANSWER_TITLE = "ANSWERS"
# QUESTION_SUB_TITTLE = "Choose the correct answer:"
titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)
total_Exercise = len(titleTag)
print(total_Exercise)

tags = soup.find_all(lambda tag: tag.name == 'p' and (tag.text.startswith('Q.') or tag.text.startswith('Q')))















# All_Quetions = []
# pattern=re.compile(r'^Q.')
# titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)
# # print(titleTag)
# for i in titleTag:
#     print(i)
#
#
# # for i in titleTag:
# #     print(i)
#
# div_store = soup.find_all('div')
# print(div_store[0:3])
# # for each in div_store:
# #     print(each)