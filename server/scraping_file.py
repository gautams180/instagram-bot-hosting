from playwright.sync_api import sync_playwright
import time
import csv
import os
import random

class InstagramBot:
    def __init__(self, username, password, account_list):
        self.sp = None
        self.browser = None
        self.cursor = None
        self.username = username
        self.password = password
        self.account_list = account_list

    def input_csv(self, x, data):
        csv_file_path = f'{x}.csv'

        if not os.path.exists(csv_file_path):
            with open(csv_file_path, mode='w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(data)

        with open(csv_file_path, mode='a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(data)

    def login(self):
        self.cursor.wait_for_selector('//*[@id="loginForm"]/div/div[1]/div/label/input', timeout=50000)
        self.cursor.query_selector('//*[@id="loginForm"]/div/div[1]/div/label/input').fill(self.username)
        self.cursor.query_selector('//*[@id="loginForm"]/div/div[2]/div/label/input').fill(self.password)
        self.cursor.query_selector('//*[@id="loginForm"]/div/div[2]/div/label/input').press("Enter")

        try:
            check_tag = self.cursor.wait_for_selector('//*[@id="loginForm"]/span/div', timeout=5000)
            return False
        except:
            try:
                self.cursor.wait_for_selector('//div[@class="_a9-v"]', timeout=2000)
                self.cursor.click('//div[@class="_a9-v"]/div[last()]/*[contains(text(), "Not Now")]')
                self.cursor.wait_for_selector('//main[@class="x78zum5 xdt5ytf x1iyjqo2 x182iqb8 xvbhtw8"]')
                return True
            except:
                return True

    def search_account(self, account_to_search):
        time.sleep(random.randint(2, 4))
        self.cursor.wait_for_selector('//div[@class="x1iyjqo2 xh8yej3"]')
        self.cursor.click('//div[@class="x1iyjqo2 xh8yej3"]/div[2]/span')
        self.cursor.wait_for_selector('//div[@class="x78zum5 xdt5ytf x5yr21d"]')
        time.sleep(random.randint(2, 4))
        self.cursor.query_selector('//div[@class="x78zum5 xdt5ytf x5yr21d"]/div/div/div/input').fill("@"+account_to_search)
        self.cursor.query_selector('//div[@class="x78zum5 xdt5ytf x5yr21d"]/div/div/div/input').press("Enter")
        self.cursor.wait_for_selector(
            '//div[@class="x6s0dn4 x78zum5 xdt5ytf x5yr21d x1odjw0f x1n2onr6 xh8yej3"]/div/a[1]', timeout=10000)
        self.cursor.click('//div[@class="x6s0dn4 x78zum5 xdt5ytf x5yr21d x1odjw0f x1n2onr6 xh8yej3"]/div/a[1]')

        try:
            self.cursor.wait_for_selector('//main[@role="main"]/div', timeout=5000)
            return True
        except:
            return False

    def follower_status(self):
        self.cursor.wait_for_selector("//main/div/header", timeout=5000)

        try:
            self.cursor.wait_for_selector('//main/div/header/section/ul/li[2]//a', timeout=5000)
            self.cursor.click('//main/div/header/section/ul/li[2]//a', timeout=5000)
            return True
        except:
            return False

    def follower_scraping(self, x):
        time.sleep(3)
        self.cursor.wait_for_selector(
            '//div[@class="xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6"]',
            timeout=10000)
        count = 1
        count_status = True

        while count_status:
            last_node = self.cursor.query_selector(
                '//div[@class="x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe"]/div/div/div[last()]/div/div/div[last()]/div/div/div/div[2]/div/div/div[1]').inner_text()

            try:
                self.cursor.wait_for_selector(
                    f'//div[@class="x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe"]/div/div/div[last()]/div/div/div[{count}]',
                    timeout=10000)
                current_node = self.cursor.query_selector(
                    f'//div[@class="x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe"]/div/div/div[last()]/div/div/div[{count}]/div/div/div/div[2]/div/div/div[1]').inner_text()

                if current_node == last_node:
                    last_element = self.cursor.wait_for_selector(
                        '//div[@class="x7r02ix xf1ldfh x131esax xdajt7p xxfnqb6 xb88tzc xw2csxc x1odjw0f x5fp0pe"]/div/div/div[last()]/div/div/div[last()]')
                    self.cursor.evaluate('(element) => { element.scrollIntoView(); }', last_element)
                    self.input_csv(x, [current_node])
                else:
                    self.input_csv(x, [current_node])
                count = count + 1
            except:
                count_status = False

        if count_status:
            return False
        else:
            return True

    def start_bot(self):
        with sync_playwright() as self.sp:
            self.browser = self.sp.chromium.launch(headless=False)
            self.cursor = self.browser.new_page()
            self.cursor.goto("https://www.instagram.com/accounts/login/")
            login_status = self.login()

            if login_status:
                print("Logged In")
                account_to_search = self.account_list

                for x in account_to_search:
                    search_status = self.search_account(x)

                    if search_status:
                        print("Account Search Successfully")
                        follower_click_status = self.follower_status()

                        if follower_click_status:
                            print("Follower Section Clickable")
                            scraping_status = self.follower_scraping(x)

                            if scraping_status:
                                print("Follower Scraping Completed")
                            else:
                                print('Follower Scraping Incomplete')
                                time.sleep(3)
                        else:
                            print('Follower Section Not Clickable')
                    else:
                        print("Account didn't searched")
            else:
                print("UnLogged In")


if __name__ == "__main__":
    username = "yourusername"
    password = "yourpassword"
    bot = InstagramBot(username, password)
    bot.start_bot()
