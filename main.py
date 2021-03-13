from bs4 import BeautifulSoup
import subprocess
import requests
import re


# whether to get page from local host or url
def page_type_selector():
    print("\nways to get page")
    print("discriptive require login, so save page from browser then (enter - 0)")
    print("mcq can do direct requests get (enter - 2)")
    pagetype = input()

    if pagetype == "2":
        print("input url of google form below\n")
        url = input()
        page = requests.get(url)
        quest_type_selector(page.text)

    elif pagetype == "0":
        # local default pickup location "~/saved_google-form"
        # only keep one webpage in folder at a time
        filetoread = subprocess.run(["find ~/saved_google-form -maxdepth 1 -type f"], shell=True, capture_output=True, encoding="utf8")
        print(filetoread.stdout[:-1])
        with open(filetoread.stdout[:-1], "r") as file:
            filecontent = file.read()
        quest_type_selector(filecontent)


# question extraction process depending on paper type
def quest_type_selector(questions):
    soup = BeautifulSoup(questions, "html.parser")
    content = soup.body.find(text=re.compile('var FB'))
    print("for discriptive - 0\nfor mcq - 2\nsometimes discriptive option skip some questions, in that case use - 1\n")
    paper_type = int(input("enter question formater input :-  "))
    print("")
    match = re.findall(f'[,]["][\d]*[.]*[\w\s\W]+",null,{paper_type}', content, re.IGNORECASE)
    matchsplit = str(match).split(f'",null,{paper_type}')

    global list2
    list2 = []
    for _ in matchsplit:
        ps1 = _.split(',"')
        ps2 = ps1[-1].replace("…", "")
        ps3 = ps2.encode('utf-8').decode('unicode_escape').replace("\\u003d", "=").replace("\\u0026", "and").replace(
            "\\", "").replace("â", "'")
        list2.append(ps3)
        print(ps3)

    retry = input("\nwant to remove some initial character (y/n) :-  ")
    if retry == "y":
        lis = []
        char_remover(lis)


# last refining bit
def char_remover(list3):
    char_rem = int(input("how many character to remove from start (numerical) :-  "))
    selecrange = input("apply on select range (y/n) ")

    if selecrange == 'y':
        fromchar = int(input("from ques number "))
        tillchar = int(input("till ques number "))
        print("")

        for _ in list2[fromchar - 1:tillchar]:
            new_form = _[char_rem:]
            list3.append(new_form)
            # print(new_form)
        print(*list3, sep="\n")

        # invoke this function again with continue list3 appending
        rerun = input("remove more (y/n) ")
        if rerun == 'y':
            char_remover(list3)

    else:
        list3 = []
        for _ in list2:
            new_form = _[char_rem:]
            list3.append(new_form)
            print(new_form)


if __name__ == "__main__":
    page_type_selector()
