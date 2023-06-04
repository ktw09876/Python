from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

import time
import pyautogui
import pyperclip

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러메시지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

#웹 브라우저 띄우기
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

#웹페이지 해당 주소로 이동
# driver.implicitly_wait(15) #웹페이지가 로딩 될때까지 5초는 기다린다 적용 안되는 이유 찾기
driver.maximize_window() #화면 최대화
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

#아이디 입력창
id = driver.find_element(By.CSS_SELECTOR, '#id') #아이디 입력창을 찾아서
id.click() #입력창을 클릭하고
# id.send_keys('ktw09876')
pyperclip.copy('ktw09876') #클립보드에 아이디를 복사
pyautogui.hotkey('ctrl', 'v') #복사한 아이디 붙여넣기
time.sleep(2) #2초를 기다린다 --> 너무 빨리하면 네이버가 봇이라고 의심한다 --> 보안문자 입력창이 뜨는 것을 방지

#비밀번호 입력창
pw = driver.find_element(By.CSS_SELECTOR, '#pw') #비밀번호 입력창을 찾아서
pw.click() #입력창을 클릭하고
# pw.send_keys('xodnr12!@')
pyperclip.copy('xodnr12!@') #클립보드에 비밀번호를 복사 
pyautogui.hotkey('ctrl', 'v') #복사한 비밀번호 붙여넣기
time.sleep(2) #2초를 기다린다 --> 너무 빨리하면 네이버가 봇이라고 의심한다 --> 보안문자 입력창이 뜨는 것을 방지

#로그인 버튼
login_btn = driver.find_element(By.CSS_SELECTOR, '#log\.login') #로그인 버튼을 찾아서 
login_btn.click() #버튼 클릭

