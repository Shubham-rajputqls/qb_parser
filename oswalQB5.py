from bs4 import BeautifulSoup
import json
import re

file = open("Bussiness studies 80mb-1-23.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')

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
.start-AR-heading {
    color: green;
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
    elif "Q." in child.text:
        if not child.text.startswith("Q.") or not child.text.startswith("Q. "):
            div_split = str(child).split("Q.")
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

count = 0
for head_tag in next_all[0].children:
    if 'Short Answer Type' in head_tag.text or 'Long Answer Type' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-heading']
        count = count + 1
    elif 'Multiple Choice Questions' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-obj-heading']
        count = count + 1
    elif 'Assertion and Reason' in head_tag.text or 'B Assertion & Reason' in head_tag.text:
        head_tag['class'] = head_tag.get('class', []) + ['start-AR-heading']
        count = count + 1
    # if count>=5:
    #     break

next_all_Qrep = soup.find_all('div', class_=["start-question"])
for div_tag in next_all_Qrep:
    div_tag.string = re.sub(r'Q.[\ ]*[0-9]+.', '', div_tag.text)

next_all_Arep = soup.find_all('div', class_=["start-answer"])
for div_tag in next_all_Arep:
    div_tag.string = re.sub(r'Ans\.?', '', div_tag.text)

next_all_Exrep = soup.find_all('div', class_=["start-explanation"])
for div_tag in next_all_Exrep:
    div_tag.string = re.sub(r'Explanation:', '', div_tag.text)

text_to_delete = soup.find_all(string='Choose the correct option from options given below:')
for each in text_to_delete:
    each.extract()


# Match_text = 'Choose the correct option from options given below:'
# divs = soup.find_all('div')
# for div_element in divs:
#     if div_element.get_text(strip=True) == Match_text:
#         print(div_element)

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
            elif "start-obj-heading" in find_next.get('class', []):
                break
            elif "start-A&R-heading" in find_next.get('class', []):
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


def extract_obj_question(next_all_tags):
    Obj_Que_list = []
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
            elif "start-obj-heading" in find_next.get('class', []):
                break
            elif "start-AR-heading" in find_next.get('class', []):
                break
            if is_answer_mode:
                find_next.text.replace("Ans.", "")
                Answer_list.append(find_next)
            else:
                Question_list.append(find_next)
            find_next = find_next.find_next_sibling()
        Question_lists = []
        Option_lists = []
        if "(A)" in Question_list[0].text and "(B)" in Question_list[0].text and "(C)" in Question_list[
            0].text and "(D)" in Question_list[0].text:
            pattern = r'\((A|B|C|D)\)'
            string = str(Question_list[0])
            result = [x for x in re.split(pattern, string) if x not in ['A', 'B', 'C', 'D']]
            remove_List = []
            for eachStr in result:
                remove_List.append(
                    eachStr.replace("\n", "").replace("<li>", "").replace("<div>", "").replace("</div>", "").replace(
                        "</li>", ""))
            Question_lists.append(remove_List[0])
            Option_lists.append(remove_List[1])
            Option_lists.append(remove_List[2])
            Option_lists.append(remove_List[3])
            Option_lists.append(remove_List[4])

        else:
            for Q_each in Question_list:
                if "(A)" in Q_each.text and "(B)" in Q_each.text and "(C)" in Q_each.text and "(D)" in Q_each.text:
                    pattern = r'\((A|B|C|D)\)'
                    string = str(Q_each)
                    result = [x for x in re.split(pattern, string) if x not in ['A', 'B', 'C', 'D']]
                    remove_List = []
                    Q1 = []
                    for eachStr in result:
                        remove_List.append(
                            eachStr.replace("\n", "").replace("<li>", "").replace("<div>", "").replace("</div>",
                                                                                                       "").replace(
                                "</li>", ""))
                    Question_lists.append(remove_List[0])
                    Option_lists.append(remove_List[1])
                    Option_lists.append(remove_List[2])
                    Option_lists.append(remove_List[3])
                    Option_lists.append(remove_List[4])
                else:
                    Question_lists.append(Q_each)
            if len(Question_list) >= 5:
                if Question_list[1].text.startswith('Statement'):
                    Question_lists = [Question_list[0], Question_list[1]]
                    Option_lists = [Question_list[3], Question_list[4], Question_list[5], Question_list[6]]
                else:
                    Question_lists = [Question_list[0]]
                    Option_lists = [Question_list[1], Question_list[2], Question_list[3], Question_list[4]]
        Obj_Que_list.append([Question_lists, Option_lists, Answer_list])

    return len(Obj_Que_list)


def extract_AR_question(next_all_tags):
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
            elif "start-obj-heading" in find_next.get('class', []):
                break
            elif "start-AR-heading" in find_next.get('class', []):
                break
            elif "start-heading" in find_next.get('class', []):
                break
            if is_answer_mode:
                find_next.text.replace("Ans.", "")
                Answer_list.append(find_next)
            else:
                Question_list.append(find_next)
            find_next = find_next.find_next_sibling()
        Assertion = []
        Reason = []
        if "Assertion (A)" in Question_list[0].text and len(Question_list) >= 2:
            Assertion.append(Question_list[0])
            if "Reason" in Question_list[1].text:
                Reason.append(Question_list[1])
        elif "Assertion (A)" in Question_list[0].text:
            Assertion.append((Question_list[0]))
            Reason.append([])
        else:
            continue
        Total_Que_list.append([Assertion, Reason, Answer_list])
    return len(Total_Que_list)


class_blocks = soup.find_all(class_='start-heading')
Dict = {}
for each_block in class_blocks:
    Question_class = []
    next_sibling = each_block.find_next_sibling()
    while next_sibling and 'start-heading' not in next_sibling.get('class', []):
        if "start-question" in next_sibling.get('class', []):
            Question_class.append(next_sibling)
        next_sibling = next_sibling.find_next_sibling()
    Dict[re.sub(r'\n?\d+\.\s', '', each_block.text)] = extract_this_section(Question_class)

Obj_class_blocks = soup.find_all(class_='start-obj-heading')

for each_block in Obj_class_blocks:
    Obj_Question_class = []
    next_sibling = each_block.find_next_sibling()
    while next_sibling and 'start-AR-heading' not in next_sibling.get('class', []):
        if "start-question" in next_sibling.get('class', []):
            Obj_Question_class.append(next_sibling)
        next_sibling = next_sibling.find_next_sibling()
    extract_obj_question(Obj_Question_class)

Obj_class_blocks = soup.find_all(class_='start-AR-heading')
for each_block in Obj_class_blocks:
    AR_Question_class = []
    next_sibling = each_block.find_next_sibling()
    while next_sibling and 'start-AR-heading' not in next_sibling.get('class', []):
        if "start-question" in next_sibling.get('class', []):
            AR_Question_class.append(next_sibling)
        next_sibling = next_sibling.find_next_sibling()
    extract_AR_question(AR_Question_class)
