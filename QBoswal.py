from bs4 import BeautifulSoup
import json
import re
file = open("AN 100-114.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
QUESTION_TITTLE = "Short Answer Type Questions-"
titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)
next_all = soup.find_all(id="preview-content")
css_styles = """
.my-class {
    color: red;
    font-weight: bold;
}
.ans-my-class {
    color: green;
    font-weight: bold;
}
"""
style_tag = soup.new_tag('style')
style_tag.string = css_styles
soup.head.append(style_tag)
# s=re.compile("Q. 3.")
# tags_containing = soup.find_all(string=s)


for child in next_all[0].children:
    if "Q. " in child.text:
        if not child.text.startswith("Q. "):
            div_split = str(child).split("Q. ")
            # ["<div asdasdasd ", "asdasdasd ></div>"]
            insert_stringOne =  f"{div_split[0]}</div><br><div>Q. {div_split[1]}"
            new_soup = BeautifulSoup(insert_stringOne, 'html.parser')
            child.replace_with(new_soup)
            # content_insert = new_soup.contents
            # child.replace_with(insert_stringOne)
            # sec_new_soup = BeautifulSoup(insert_stringTwo, 'html.parser')
            # child.append(sec_new_soup)





            # new_div = soup.new_tag('div')
            # prev_div = soup.new_tag('div')
            # prev_div.append(div_split[0])
            # new_div.append(div_split[1])
for each in next_all[0].children:
    if each.text.startswith('Q.') or each.text.startswith('Q. '):
        each['class'] = each.get('class', []) + ['my-class']




for ans_child in next_all[0].children:
    if "Ans." in ans_child.text:
        if not ans_child.text.startswith("Ans."):
            div_split = str(ans_child).split("Ans.")
            # ["<div asdasdasd ", "asdasdasd ></div>"]
            insert_ans_stringOne =  f"{div_split[0]}</div><br><div>Ans. {div_split[1]}"
            ans_new_soup = BeautifulSoup(insert_ans_stringOne, 'html.parser')
            ans_child.replace_with(ans_new_soup)



for ans_each in next_all[0].children:
    if ans_each.text.startswith('Ans.') or ans_each.text.startswith('Ans. '):
        ans_each['class'] = ans_each.get('class', []) + ['ans-my-class']





def full_Question_Ans(Iteration):
    print("")








Total_Que_list = []
Answer = []
count = 0
next_all_tags = soup.find_all('div', {"class":"my-class"})
print(len(next_all_tags))
for each_Que_ans in next_all_tags:
    Questions = []
    Question_list = []
    Answer_list = []
    Question_list.append(each_Que_ans)
    each_Que_ans = each_Que_ans.find_next_sibling()
    while True:
        if "my-class" not in each_Que_ans.get('class', []) and "ans-my-class" not in each_Que_ans.get('class', []):
            Question_list.append(each_Que_ans)
            each_Que_ans = each_Que_ans.find_next_sibling()
        else:
            if "ans-my-class" in each_Que_ans.get('class', []):
                Answer_list.append(each_Que_ans)
                while True:
                    each_Que_ans = each_Que_ans.find_next_sibling()
                    if "my-class" not in each_Que_ans.get('class', []) and "ans-my-class" not in each_Que_ans.get(
                            'class', []):
                        Answer_list.append(each_Que_ans)
                    else:
                        Questions.append(Question_list)
                        Questions.append(Answer_list)
                        break
            else:
                Questions.append(Question_list)
                Total_Que_list.append(Questions)
                break
    Total_Que_list.append(Questions)



print(len(Questions))
print(count)














        # while True:
        #     each_Que_ans = each_Que_ans.find_next_sibling()
        #     if isinstance(each_Que_ans, type(None)):
        #         print(each_Que_ans)
        #         print("*********************************************************************************")
        #     print(each_Que_ans)
        #     if "my-class" not in each_Que_ans.get('class', []) and "ans-my-class" not in each_Que_ans.get('class', []):
        #     # if not each_Que_ans.text.startswith("Q. ") or not each_Que_ans.text.startswith("Ans."):
        #         Question_list.append(each_Que_ans)
        #     else:
        #         Questions.append(Question_list)
        #         break
    # if "ans-my-class" in each_Que_ans.get('class', []):
    #     Answer_list.append(each_Que_ans)
    #     while True:
    #         each_Que_ans = each_Que_ans.find_next_sibling()
    #         if isinstance(each_Que_ans, type(None)):
    #             print(each_Que_ans.find_previous_sibling())
    #
    #
    #         if not each_Que_ans.text.startswith("Q. ") or not each_Que_ans.text.startswith("Ans."):
    #         # if "my-class" not in each_Que_ans.get('class', []) and "ans-my-class" not in each_Que_ans.get('class', []):
    #             Answer_list.append(each_Que_ans)
    #
    #         else:
    #             break
#     else:
#         continue
#
#
# print(len(Questions))
#



#
#
#
#
#
# Question_list=[]
# for each_Que_ans in next_all_tags:
#     FullQuestion = []
#     FullAnswer = []
#     if "my-class" in each_Que_ans.get('class', []):
#         Question = soup.new_tag('div')
#         Question.append(each_Que_ans)
#         while True:
#             each_Que_ans = each_Que_ans.find_next_sibling()
#             print(each_Que_ans)
#             if not each_Que_ans.text.startswith("Q. ") or not each_Que_ans.text.startswith("Ans."):
#             # if "my-class" not in each_Que_ans.get('class', []) and "ans-my-class" not in each_Que_ans.get('class', []):
#                 br = soup.new_tag('br')
#                 Question.append(br)
#                 Question.append(each_Que_ans)
#             else:
#                 break
#         FullQuestion.append(Question)
#         #print("yes")
#     if "ans-my-class" in each_Que_ans.get('class', []):
#         Answer = soup.new_tag('div')
#         Answer.append(each_Que_ans)
#         while True:
#             each_Que_ans = each_Que_ans.find_next()
#             print(each_Que_ans)
#             if not each_Que_ans.text.startswith("Q. ") or not each_Que_ans.text.startswith("Ans."):
#             # if "my-class" not in each_Que_ans.get('class', []) and "ans-my-class" not in each_Que_ans.get('class', []):
#                 br = soup.new_tag('br')
#                 Answer.append(br)
#                 Answer.append(each_Que_ans)
#             else:
#                 break
#         FullAnswer.append(Answer)
#
#     if len(FullQuestion)>0:
#         MainList = []
#         MainList.append(FullQuestion)
#         MainList.append(FullAnswer)
#         if len(MainList)>0:
#             Question_list.append(MainList)
#
#     else:
#         continue
#
#
# print(Question_list)
#
#
#
# #
# #






















# print(len(next_all_tags))
# for i in next_all_tags:
#     while True:
#         i = i.find_next_sibling()
#         print(type(i))
#




































# titleTag_div = soup.find_all(lambda tag: tag.name == "div" and "Q. 3." in tag.text)

# for each in titleTag_div:
#     print()
# # pattern = "Q. "
# # t = soup.find_all('div', string = pattern)
# # print(t)
# word = "Q. "
# tag = soup.find_all('div', lambda string: word in string)
# for div in tag:
#     print(div)
# for each in next_all:
#     print(each)
#     check_word = "Q. "
#     if check_word in each.text:
#         print("*************************")
#         print(each)
        # parts = each.text.split(check_word)
        # next_div = soup.new_tag('div')
        # next_div.append(parts[1])
        # next_div['class'] = next_div.get('class', []) + ['my-class']







#print(soup.prettify())











# css_styles = """
# .my-class {
#     color: red;
#     font-weight: bold;
# }
# """
# style_tag = soup.new_tag('style')
# style_tag.string = css_styles
# soup.head.append(style_tag)
# titleTag[0]['class'] = titleTag[0].get('class', []) + ['my-class']









# print(next_div)
# QUESTION_TITTLE = "Short Answer Type Questions-"
# # ANSWER_TITLE = "ANSWERS"
# # QUESTION_SUB_TITTLE = "Choose the correct answer:"
# titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)
# total_Exercise = len(titleTag)
#
# titleTag[0].string="Hii shubham"

# # find_next = titleTag[0].find_next_siblings()
# print(find_next)

# tags = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)
# print(len(tags))
# Questions=[]
#
# def next_div_iterate(divtags):
#     for eachDiv in divtags:
#         if eachDiv.text.startswith('Q'):
#             div_container = soup.new_tag('div')
#             div_container.append(eachDiv)
#             while True:
#                 next_same_type_tag = eachDiv.find_next_sibling()
#                 if next_same_type_tag.text.startswith('Q'):
#                     break
#                 elif next_same_type_tag.text.startswith('Ans'):
#                     next_answer_div_tag(next_same_type_tag)
#                 elif "Ans" in next_same_type_tag.text:
#                     l = str(next_same_type_tag).split("Ans")
#                     div_container.append(l[0])
#
#
#                 div_container.append((next_same_type_tag))
#
#
# def next_answer_div_tag(answer_tag):
#     answerdiv_container = soup.new_tag('div')
#     while True:
#         answerdiv_container.append(answer_tag)
#         answer_tag = answer_tag.find_next_sibling()
#         if answer_tag.text.startswith('Q'):
#             break
#
#
#
# for tag in tags:
#     div_tags_after_specific = tag.find_next_siblings()
#     next_div_iterate(div_tags_after_specific)
#
#
#
#
#
#     for i in div_tags_after_specific:
#         l1=[]
#         if i.text.startswith('Q') or i.text.startswith('Q.'):
#             l1.append(i)
#             if i.find_next_sibling().startswith('Ans') or i.find_next_sibling().startswith('Ans.'):
#
#
#
#
#
#

# # Traverse all div tags after the specific div tag
# div_tags_after_specific = titleTag[0].find_next_siblings('div')
# # Print the found div tags
# for div_tag in div_tags_after_specific:
#     print(div_tag)