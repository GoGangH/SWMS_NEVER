from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from sqlalchemy import false
import os
import time
import string
import re

class Crow:

    def __init__(self):
        print("------- Crome open -------")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        time.sleep(2)

    def __del__(self):
        print("------- Crome close -------")
        self.driver.quit()


    def word_pretreatment(self, word): #제목과 가수에서 불필요 문제 제거
        pattern = r'\([^)]*\)'

        text = re.sub(pattern=pattern, repl='', string= word)
        text = text.replace(",", "")
        text = text.replace(" ", "")

        return text

    def crowling_review(self, query, query2):

        query = self.word_pretreatment(query)
        query2 = self.word_pretreatment(query2)

        print()
        print("[입력 데이터] 제목:",query," 가수:", query2)

        #크롬드라이버로 원하는 url로 접속
        url = 'http://izm.co.kr/searchLists.asp?search_tp=8&keywordid=&keyword='+query
        self.driver.get(url)
        time.sleep(3)

        ''' 제목과 가수에 맞는 설명 페이지 이동 '''

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        music_list = self.driver.find_elements(By.CSS_SELECTOR, '#summary1 > li > table > tbody > tr')

        chk_M = False

        # 페이지 이동
        try :
            for i in range(1, len(music_list)+1):
                Music_name = self.driver.find_element(By.CSS_SELECTOR, f"#summary1 > li.contents4 > table > tbody > tr:nth-child({i}) > td > table > tbody > tr > td:nth-child(1)").text.replace("\n","")
                Music_singer = self.driver.find_element(By.CSS_SELECTOR, f"#summary1 > li.contents4 > table > tbody > tr:nth-child({i}) > td > table > tbody > tr > td:nth-child(3)").text.replace("\n","")
                if Music_name == query and Music_singer == query2 :
                    self.driver.find_element(By.XPATH, f"/html/body/ul/li[3]/ul/li[1]/div/ul/li[2]/table/tbody/tr[{i}]/td/table/tbody/tr/td[1]/a").click()
                    chk_M=True
        except Exception as error:
            print("Error : Not found data.")
            self.driver.quit()
            return ""

        time.sleep(3)

        '''페이지 리뷰 설명 가져오기'''

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        review_list = self.driver.find_element(By.CSS_SELECTOR, f"#summary1 > li.contents3 > article").text.replace("\n", " ")
        print("Success : Reveiw data crowling.")
        return review_list