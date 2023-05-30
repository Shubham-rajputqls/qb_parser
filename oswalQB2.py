from bs4 import BeautifulSoup
import json
import re

file = open("AN 100-114.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
# QUESTION_TITTLE = ["Short Answer Type Questions-", "Long Answer Type Questions", "Multiple Choice Questions", "Assertion and Reason"]
# titleTag = soup.find(lambda tag: (tag.name == "h2" or tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE[i] in tag.text)


next_all = soup.find_all(id="preview-content")
css_styles = """
.start-question {
    color: red;
    font-weight: bold;
}
.start-answer {
    color: green;
    font-weight: bold;
}
.start-heading {
    color: blue;
    font-weight: bold;
}
.start-explanation {
    color: yellow;
    font-weight: bold;
}

"""
style_tag = soup.new_tag('style')
style_tag.string = css_styles
soup.head.append(style_tag)

# Pre-Process For Question
for child in next_all[0].children:
    if "Q. " in child.text:
        if not child.text.startswith("Q. "):
            div_split = str(child).split("Q. ")
            insert_stringOne = f"{div_split[0]}</div><br><div>Q. {div_split[1]}"
            new_soup = BeautifulSoup(insert_stringOne, 'html.parser')
            child.replace_with(new_soup)

for each in next_all[0].children:
    if each.text.startswith('Q.') or each.text.startswith('Q. '):
        each['class'] = each.get('class', []) + ['start-question']
    elif each.text.startswith('Explanation:'):
        each['class'] = each.get('class', []) + ['start-explanation']
        # each.text.replace("Explanation:", "")



# Pre-Process For Answer
for ans_child in next_all[0].children:
    if "Ans." in ans_child.text:
        if not ans_child.text.startswith("Ans."):
            div_split = str(ans_child).split("Ans.")
            # ["<div asdasdasd ", "asdasdasd ></div>"]
            insert_ans_stringOne = f"{div_split[0]}</div><br><div>Ans. {div_split[1]}"
            ans_new_soup = BeautifulSoup(insert_ans_stringOne, 'html.parser')
            ans_child.replace_with(ans_new_soup)

for ans_each in next_all[0].children:
    if ans_each.text.startswith('Ans.') or ans_each.text.startswith('Ans. '):
        ans_each['class'] = ans_each.get('class', []) + ['start-answer']

count=0
for head_tag in next_all[0].children:
    if 'Short Answer Type Questions' in head_tag.text or 'Long Answer Type Questions' in head_tag.text or 'Multiple Choice Questions' in head_tag.text or 'Assertion and Reason' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-heading']
        count = count + 1
    if count>=5:
        break

next_all_Qrep = soup.find_all('div', class_=["start-question"])
for div_tag in next_all_Qrep:
    div_tag.string = re.sub(r'Q.[\ ]*[0-9]+.', '', div_tag.text)

next_all_Arep = soup.find_all('div', class_=["start-answer"])
for div_tag in next_all_Arep:
    div_tag.string = re.sub(r'Ans\.?', '', div_tag.text)

next_all_Exrep = soup.find_all('div', class_=["start-explanation"])
for div_tag in next_all_Exrep:
    div_tag.string = re.sub(r'Explanation:', '', div_tag.text)


# next_all_Hrep = soup.find_all('h2' or 'h1', class_=["start-heading"])
# for div_tag in next_all_Hrep:
#     div_tag.string = re.sub(r'\d+\.', '', div_tag.text)

def extract_this_section(next_all_tags):
    Total_Que_list = []
    for each_Que_ans in next_all_tags:
        Question_list = []
        Answer_list = []
        Question_list.append(each_Que_ans)
        find_next = each_Que_ans.find_next_sibling()
        count = 0
        is_answer_mode = False
        while find_next is not None:
            if "start-answer" in find_next.get('class', []):
                is_answer_mode = True
            elif "start-question" in find_next.get('class', []):
                break
            elif "start-heading" in find_next.get('class', []):
                break
            # elif re.search(r'\[.*?\]', find_next.text):
            #     find_next.decompose()
            if is_answer_mode:
                find_next.text.replace("Ans.", "")
                Answer_list.append(find_next)
            else:
                Question_list.append(find_next)
            find_next = find_next.find_next_sibling()
        Total_Que_list.append([Question_list, Answer_list])
    return Total_Que_list




class_blocks = soup.find_all(class_='start-heading')
#print(soup.prettify())
Dict={}
for each_block in class_blocks:
    M_Question_class=[]
    Question_class =[]
    next_sibling = each_block.find_next_sibling()
    while next_sibling and 'start-heading' not in next_sibling.get('class', []):
        if "start-question" in next_sibling.get('class', []):
            Question_class.append(next_sibling)
        next_sibling = next_sibling.find_next_sibling()
    while next_sibling and 'Multiple Choice Questions' in next_sibling.text and 'Assertion and Reason'not in next_sibling.text:
        if "start-question" in next_sibling.get('class',[]):
            M_Question_class.append(next_sibling)
        next_sibling = next_sibling.find_next_sibling()
    Dict[re.sub(r'\n?\d+\.\s', '', each_block.text)] = extract_this_section(Question_class)


# next_all_tags = soup.find_all('div', class_=["start-question"])
# Total_Que_list = []
# for each_Que_ans in next_all_tags:
#     Questions = []
#     Question_list = []
#     Answer_list = []
#     Question_list.append(each_Que_ans)
#     find_next = each_Que_ans.find_next_sibling()
#     count = 0
#     is_answer_mode = False
#     while find_next is not None:
#         if "start-answer" in find_next.get('class', []):
#             is_answer_mode = True
#         elif "start-question" in find_next.get('class', []):
#             break
#         if is_answer_mode:
#             Answer_list.append(find_next)
#         else:
#             Question_list.append(find_next)
#         find_next = find_next.find_next_sibling()
#     Total_Que_list.append([Question_list, Answer_list])
#
#
# Collecting Questions

# lists = []
# for block in class_blocks:
#     items = []
#     next_sibling = block.find_next_sibling()
#     while next_sibling and 'start-heading' not in next_sibling.get('class', []):
#         items.append(next_sibling.get_text(strip=True))
#         next_sibling = next_sibling.find_next_sibling()
#     lists.append(items)
# print(len(lists))
#
#









# QUESTION_TITTLE = ["Short Answer Type Questions", "Short Answer Type Questions", "Long Answer Type Questions", "Multiple Choice Questions", "Assertion and Reason"]
# current_tag = soup.find(lambda tag: ((tag.name == "div" and tag.text==QUESTION_TITTLE[0]) or tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE[0] in tag.text)
# for i in range(0, len(QUESTION_TITTLE)-1):
#     current_tag = current_tag.find_next_sibling()
#     next_siblings = []
#     while current_tag and QUESTION_TITTLE[i+1].lower() in current_tag.text.lower():
#         if "start-question" in current_tag.get('class', []):
#             next_siblings.append(current_tag)
#         current_tag = current_tag.find_next_sibling()
#     print(len(extract_this_section(next_siblings)))
#
























    #
    # if "start-question" not in find_next.get('class', []) and "start-answer" not in find_next.get('class', []):
    #     Question_list.append(find_next)
    #     find_next = find_next.find_next_sibling()
    # elif "start-answer" in find_next.get('class', []):
    #     Answer_list.append(find_next)
    #     find_next = find_next.find_next_sibling()
    #     while find_next is not None:
    #         if "start-question" not in find_next.get('class', []) and "start-answer" not in find_next.get('class', []):
    #             Answer_list.append(find_next)
    #             find_next = find_next.find_next_sibling()
    #         else:
    #
    #             count = count + 1
    #             break
    #     Questions.append(Question_list)
    #     Questions.append(Answer_list)
    #     break
    # else:
    #     break
    # if count == 0:
    #     Questions.append(Question_list)
    #     Questions.append(Answer_list)
    # Total_Que_list.append(Questions)


# All_question = []
# for Que_no in range(2, 3):  # len(Total_Que_list)):
#     #print(f"Question {Que_no}")
#     #print(Total_Que_list[Que_no][0])
#     #print(f"Answer {Que_no}")
#     print(Total_Que_list[Que_no][1])
