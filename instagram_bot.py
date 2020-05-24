from selenium import webdriver
from time import sleep
from secrets import username, email, password


class InstaBot:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get("https://instagram.com")
        sleep(2)

        # Get the login with fb btn
        self.driver.find_element_by_xpath("//span[text()='Log in with Facebook']") \
            .click()
        sleep(2)

        # Enter email and password and click login button
        self.driver.find_element_by_xpath("//input[@name=\"email\"]") \
            .send_keys(email)
        self.driver.find_element_by_xpath("//input[@name=\"pass\"]") \
            .send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]') \
            .click()
        sleep(4)

        # Close notification on popup
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
            .click()
        sleep(2)

    #  Go to your profile page
    def profile_page(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(username)) \
            .click()
        sleep(2)

    # Go to someone profile
    def goto_crush_profile_page(self):
        self.driver.get("https://www.instagram.com/gussi/")
        sleep(2)

    # Get followers list
    def get_followers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]") \
            .click()
        followers = self._get_names()
        return followers

    # Get followings list
    def get_following(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]") \
            .click()
        following = self._get_names()
        return following

    # Get the list of people who dont follow you back
    def get_unfollowers(self, following, followers):
        not_following_back = [user for user in following if user not in followers]
        print(not_following_back)

    # A bit of javascript code, while loop is use for scrolling through
    #  following/followers popup box
    def _get_names(self):
        sleep(2)
        # suggestions = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
        # self.driver.execute_script('arguments[0].scrollIntoView()', suggestions)
        # sleep(2)

        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        # close popup
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
            .click()
        return names


bot = InstaBot()
bot.login()
bot.profile_page()
bot.get_unfollowers(bot.get_following(), bot.get_followers())
