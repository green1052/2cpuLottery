import random

import requests
from bs4 import BeautifulSoup

userId = input("아이디를 입력해주세요: ")
password = input("비밀번호를 입력해주세요: ")
url = input("게시글 주소를 입력해주세요: ")
lotteryCount = int(input("몇명을 선출할지 정해주세요: "))

if not userId or not password or not url or not lotteryCount:
    print("입력 값이 잘못됐습니다.")
    exit()

print("\n\n\n\n\n")

session = requests.Session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
}

session.post("https://www.2cpu.co.kr/bbs/login_check.php", {
    "mb_id": userId,
    "mb_password": password
})

response = session.get(url)
soup = BeautifulSoup(response.text, "html.parser")

userList = []

i: BeautifulSoup
for i in soup.select("table td"):
    if i.attrs.get("valign") != "top":
        continue

    name = i.select_one("a").text.strip()
    content = i.select("div")[2].text.strip()

    if "[신청]" in content:
        userList.append({"name": name, "content": content})

userListCount = len(userList)

if lotteryCount > userListCount:
    print(f"신청 댓글의 수인 {userListCount}개를 초과하여 입력할 수 없습니다. 입력 값: {lotteryCount}")
    exit()


def choice_user_comment():
    rnd = random.SystemRandom().randint(0, len(userList) - 1)
    winner = userList[rnd]

    userList.remove(winner)

    print(f"""{winner["name"]}님이 당첨되었습니다.""")


if lotteryCount == 1:
    choice_user_comment()
    exit()

for j in range(lotteryCount):
    choice_user_comment()
