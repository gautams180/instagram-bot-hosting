from playwright.sync_api import sync_playwright
import time
import csv
import random


class FollowerBot:
    def __init__(self, username, password, account_list):
        self.sp = None
        self.browser = None
        self.cursor = None
        self.username = username
        self.password = password
        self.account_list = account_list
        print(account_list)

    def bot_login(self):
        self.cursor.wait_for_selector('//*[@id="loginForm"]/div/div[1]/div/label/input', timeout=50000)
        self.cursor.query_selector('//*[@id="loginForm"]/div/div[1]/div/label/input').fill(self.username)
        self.cursor.query_selector('//*[@id="loginForm"]/div/div[2]/div/label/input').fill(self.password)
        self.cursor.query_selector('//*[@id="loginForm"]/div/div[2]/div/label/input').press("Enter")

        try:
            self.cursor.wait_for_selector('//*[@id="loginForm"]/span/div', timeout=50000)
            return False
        except:
            return True

    def post_follow(self, name):
        time.sleep(random.randint(2, 4))
        self.cursor.goto(f'https://www.instagram.com/{name}')
        self.cursor.wait_for_selector('//main/div/header')

        try:
            self.cursor.wait_for_selector(
                '//main/div/header/section/div[1]/div//*[contains(text(), "Follow") and not (contains(text(), "Following"))]',
                timeout=2000)
            self.cursor.click('//main/div/header/section/div[1]/div//*[contains(text(), "Follow")]')
            return True
        except:
            return False

    def bot_start(self):
        with sync_playwright() as self.sp:
            self.browser = self.sp.chromium.launch(headless=False)
            self.cursor = self.browser.new_page()
            self.cursor.goto("https://www.instagram.com/accounts/login/")
            login_status = self.bot_login()

            if login_status:
                print("Logged In")
                account_to_follow = self.account_list
                print(account_to_follow)

                
                for x in account_to_follow:
                    following_status = self.post_follow(x)

                    if following_status:
                        print("Account Gets Followed")
                    else:
                        print("Account Already Followed")
            else:
                print("UnLogged In")


if __name__ == "__main__":
    username = ""
    password = ""
    bot = FollowerBot(username, password)
    bot.bot_start()
