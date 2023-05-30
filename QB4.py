from bs4 import BeautifulSoup
import json
file = open("chapter4 and 5.html", "r")
fp = file.read()
soup = BeautifulSoup(fp, 'html.parser')
QUESTION_TITTLE = "Multiple Choice Questions"
ANSWER_TITLE = "Answer Key"
QUESTION_SUB_TITTLE = "Choose the correct answer:"
titleTag = soup.find_all(lambda tag: (tag.name == "h2" or tag.name =="h1") and QUESTION_TITTLE in tag.text)
total_Exercise=len(titleTag)
print(total_Exercise)
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
    answer_list = []
    def answer_print(h2_sibling):
        count = 0
        table_row = h2_sibling.select('table > tbody > tr')
        count = count + 1
        if len(table_row) > 0:
            for row in table_row:
                count = count + 1
                cells = row.find_all('td')
                for cell in cells:
                    data = cell.get_text()
                    if data == '':
                        continue
                    answer_list.append(data)
        # for item in A_doc.children:
        #     l2 = []
        #     if item.name == 'li':
        #         l2.append(item)
        #         if item.find_next_sibling() == "div":
        #             l2.append(item.find_next_sibling)
        #         answer_list.append(l2)
    def divInsert():
        for eachdiv in divList:
            br = soup.new_tag('br')
            ques_list[len(ques_list) - 1][0].append(br)
            ques_list[len(ques_list) - 1][0].append(eachdiv.text)
    for h2_sibling in titleTag.find_next_siblings():
        if h2_sibling.name == "ol":
            question_print(h2_sibling)
            r = h2_sibling
            count = 0
            divList=[]
            while True:
                k = r.find_next_sibling()
                if k.name == 'div' and k.get_text().startswith("("):
                    divList.append(k)
                    r = k
                    count += 1
                else:
                    if count != 0:
                        divInsert()
                    break
        elif h2_sibling.name == 'h2' and QUESTION_SUB_TITTLE not in h2_sibling.text:
            break
    titleTag = soup.find_all(lambda tag: tag.name == "h2" and tag.get_text().endswith(ANSWER_TITLE))[eachEx]

    title_loopAns = titleTag.find_next_siblings()
    count1 =0
    for h2_sibling in title_loopAns:

        table_row = h2_sibling.select('table > tbody')

        for i in range(len(table_row)):
            if (table_row[i].name) == "tbody":
                count1 = count1 +1
                answer_print(h2_sibling)
                if count1 == 1:
                    break

            else:
                continue
        if count1 == 1:
            break
    print(len(ques_list))
    print(len(answer_list))



        # elif h2_sibling.name == 'h2':
        #     break
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
        if len(remove_List)<5:
            remove_List.append("Not Detect")


        remove_List[1] = remove_List[1].replace("(a) ", "")
        remove_List[2] = remove_List[2].replace("(b) ", "")
        remove_List[3] = remove_List[3].replace("(c) ", "")
        remove_List[4] = remove_List[4].replace("(d) ", "")
        for i in remove_List:
            Q1.append("<p>" + i + "</p>")
        Dict["Question"] = Q1[0]
        # if Q1[1]=="":
        #     Q1[1]=
        # elif Q1[2] =="":
        # elif Q1[3] == "":
        # elif Q1[4] == "":

        Dict["Option"] = [Q1[1], Q1[2], Q1[3], Q1[4]]
        # print(answer_list[t][0].text.split())
        if 'a)' in answer_list[t].split("(") or '(a)' in answer_list[t].split():
            Dict["correct_option"] = [1]
        elif 'b)' in answer_list[t].split("(") or '(b)' in answer_list[t].split():
            Dict["correct_option"] = [2]
        elif 'c)' in answer_list[t].split("(") or '(c)' in answer_list[t].split():
            Dict["correct_option"] = [3]
        elif 'd)' in answer_list[t].split("(") or '(d)' in answer_list[t].split():
            Dict["correct_option"] = [4]
        else:
            Dict["correct_option"] = ["Not detect"]
        parsed_question.append(Dict)
        All_Quetions.append((parsed_question))
out_File = open("MathematicsQuetions2.json", "w")
json.dump(All_Quetions, out_File, indent=6)
print(out_File)