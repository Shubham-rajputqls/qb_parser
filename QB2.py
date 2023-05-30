from bs4 import BeautifulSoup
import json
file = open("mathematics.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
QUESTION_TITTLE = "Multiple Choice Questions"
ANSWER_TITLE = "ANSWERS"
QUESTION_SUB_TITTLE = "Choose the correct answer:"
titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name =="h1") and QUESTION_TITTLE in tag.text)
total_Exercise=len(titleTag)

All_Quetions = []
for eachEx in range(0,total_Exercise):
    titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name == "h1") and QUESTION_TITTLE in tag.text)[eachEx]
    ques_list = []
    def question_print(q_doc):
        for item in q_doc.children:
            if item.name != 'li':
                continue
            l1 = [item]
            if item.find_next_sibling() == "div":
                l1.append(item.find_next_sibling)
            ques_list.append(l1)
        print(ques_list)


    answer_list = []
    def answer_print(A_doc):
        for item in A_doc.children:
            l2 = []
            if item.name == 'li':
                l2.append(item)
                if item.find_next_sibling() == "div":
                    l2.append(item.find_next_sibling)
                answer_list.append(l2)
    # def divInsert():
    #     for eachdiv in divList:
    #         br = soup.new_tag('br')
    #         ques_list[len(ques_list) - 1][0].append(br)
    #         ques_list[len(ques_list) - 1][0].append(eachdiv.text)
    for h2_sibling in titleTag.find_next_siblings():
        if h2_sibling.name == "ol":
            question_print(h2_sibling)
            # r = h2_sibling
            # count = 0
            # divList=[]
            # while True:
            #     k = r.find_next_sibling()
            #     if k.name == 'div' and k.get_text().startswith("("):
            #         divList.append(k)
            #         r = k
            #         count += 1
            #     else:
            #         if count != 0:
            #             divInsert()
            #         break
            #
    # titleTag = soup.find_all(lambda tag: tag.name == "h2" and tag.get_text().endswith(ANSWER_TITLE))[eachEx]
    # title_loopAns = titleTag.find_next_siblings()
    # for h2_sibling in title_loopAns:
    #     if h2_sibling.name == "ol":
    #         answer_print(h2_sibling)
    #     elif h2_sibling.name == 'h2':
    #         break
    parsed_question = []
    for t in range(0, len(ques_list)):
        # l = []
        l = []
        l = str(ques_list[t][0]).split("<br/>")
        Q1 = []
        Dict = {}
        parsed_question = []
        remove_List=[]
        for eachStr in l:
            remove_List.append(eachStr.replace("\n","").replace("<li>", "").replace("<div>", "").replace("</div>", "").replace("</li>", ""))
        remove_List[1] = remove_List[1].replace("(a) ", "")
        remove_List[2] = remove_List[2].replace("(b) ", "")
        remove_List[3] = remove_List[3].replace("(c) ", "")
        remove_List[4] = remove_List[4].replace("(d) ", "")
        for i in remove_List:
            Q1.append("<p>" + i + "</p>")
        Dict["Question"] = Q1[0]

        Dict["Option"] = [Q1[1], Q1[2], Q1[3], Q1[4]]
        # print(answer_list[t][0].text.split())
        # if answer_list[t][0].text == '(a)' or 'a)' in answer_list[t][0].text.split("(") or '(a)' in answer_list[t][0].text.split():
        #     Dict["correct_option"] = [1]
        # elif answer_list[t][0].text == '(b)' or 'b)' in answer_list[t][0].text.split("(") or '(b)' in answer_list[t][0].text.split():
        #     Dict["correct_option"] = [2]
        # elif answer_list[t][0].text == '(c)' or 'c)' in answer_list[t][0].text.split("(") or '(c)' in answer_list[t][0].text.split():
        #     Dict["correct_option"] = [3]
        # elif answer_list[t][0].text == '(d)' or 'd)' in answer_list[t][0].text.split("(") or '(d)' in answer_list[t][0].text.split():
        #     Dict["correct_option"] = [4]
        # else:
        #     Dict["correct_option"] = ["Not detect"]
        parsed_question.append(Dict)
        All_Quetions.append((parsed_question))
out_File = open("MathematicsQuetions.json", "w")
json.dump(All_Quetions, out_File, indent=6)
