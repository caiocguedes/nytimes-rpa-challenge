from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from selenium.common.exceptions import *
from functions import RPADataProcessor
import time
import configparser

class RPADataExtractorApp:
    def __init__(self, config_path='config.ini'):
        #creating configparser instance and reading file
        self.config = configparser.ConfigParser() 
        self.config.read(config_path)
        
        #creating http instance to download images
        self.http = HTTP() 
        #importing selenium
        self.browser = Selenium(auto_close=False)
        
        #instanciating the functions
        self.data_processor = RPADataProcessor()
        
        #counters
        self.count_in_title = 0
        self.count_in_description = 0

    def run(self):
        self.setup_browser()
        self.data_processor.create_worksheet()
        self.data_processor.create_pictures_folder()
        self.navigate_site()
        self.apply_filters()
        self.extract_data()
        self.save_data_in_spreadsheet()
        self.close_browser()

    def setup_browser(self):
        self.browser.open_available_browser("nytimes.com", maximized=True)
        
        #setting config.ini file values to local variables
        self.phrase = self.config.get('Settings', 'phrase')
        self.category = self.config.get('Settings', 'category', fallback="Any") #fallback == exception treatment to cover the absensce of a category in config.ini
        self.category = self.data_processor.format_categories(self.category)

    def navigate_site(self):
        #going through privacy pop-up
        try:
            self.browser.click_button_when_visible('//*[@id="fides-banner-button-primary"]')
        except ElementClickInterceptedException as x:
            self.browser.click_button_when_visible('//*[@id="fides-banner-button-primary"]')
        finally:
            #navigating through the main page        
            self.browser.wait_and_click_button('//*[@id="app"]/div[2]/div/header/section[1]/div[1]/div[2]/button') #clicks on search button (magnifier)
            self.browser.input_text("class:css-1u4s13l", self.phrase) #input phrase
            self.browser.click_button('//*[@type="submit"]') #search     
          
    def apply_filters(self):         
        #section button
        self.browser.wait_and_click_button('class:css-4d08fs')
        checkboxes = self.browser.find_elements('class:css-16eo56s')
        
        #clicks on checkbox according to the amount of categories
        for checkbox in checkboxes:
            for item in self.category:
                if item in checkbox.text:
                    self.browser.click_element(checkbox)

        #filtering by latest news
        self.browser.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[2]/div/div/button') #clicks on section to collapse the dropdown menu
        self.browser.click_element('class:css-v7it2b') #clicks on 'sort' dropdown menu
        self.browser.press_keys('class:css-v7it2b', 'ARROW_DOWN') #selects 'sort by newest'

        #waiting for the filters...
        time.sleep(2)

    def extract_data(self):
        self.descriptions = []
        self.dates = self.browser.find_elements('class:css-17ubb9w') #search for dates
        self.news_list = self.browser.find_elements('class:css-e1lvw9') #search for the elements containing news
        
        for news in self.news_list:
            try:
                #tries to locate an description web element inside every news
                self.description = self.browser.get_webelement('class:css-16nhkrn', parent=news)
                self.descriptions.append(self.description)
            except Exception as e:
                #if the news does not contain a description, append an empty string to the list
                self.descriptions.append("")
            
        self.titles = self.browser.find_elements('//h4[@class="css-2fgx4k"]')
        self.pictures = self.browser.find_elements('class:css-rq4mmj')
    
    def save_data_in_spreadsheet(self):
        #for every title found in news, count the phrases in title, verify if there is any amount of money and add those data to the .xlsx file
        for title in range(len(self.titles)):
            self.count_in_title += self.data_processor.count_search_phrases(self.phrase, self.titles[title].text)
            bool_money_in_title = self.data_processor.verify_money_in_text(self.titles[title].text)
            self.data_processor.add_data_to_worksheet('A%s' % str(title+2), self.titles[title].text)
            self.data_processor.add_data_to_worksheet('E%s' % str(title+2), str(self.count_in_title))
            self.data_processor.add_data_to_worksheet('G%s' % str(title+2), str(bool_money_in_title))
        
        #adding news dates to spreadsheet
        for date in range(len(self.dates)):
            self.data_processor.add_data_to_worksheet('B%s' % str(date+2), self.dates[date].text)
            
        #for every description found in news, if the description contains any text, count the phrases in description, verify if there is any amount of money and add those data to the .xlsx file
        for description in range(len(self.descriptions)):
            if self.descriptions[description] != "":
                self.count_in_description += self.data_processor.count_search_phrases(self.phrase, self.descriptions[description].text)
                bool_money_in_title = self.data_processor.verify_money_in_text(self.descriptions[description].text)
                self.data_processor.add_data_to_worksheet('C%s' % str(description+2), self.descriptions[description].text)
                self.data_processor.add_data_to_worksheet('F%s' % str(description+2), str(self.count_in_description))
        
        #gets every picture full address, downloads it, adds to a list, and formats it to get only the filename, then adds it to the spreadsheet     
        for picture in range(len(self.pictures)):
            filename = str(self.browser.get_element_attribute(self.pictures[picture], "src"))
            self.http.download(filename, self.data_processor.pictures_path)
            self.data_processor.pictures_list.append(filename)
            picture_name = self.data_processor.format_pictures_filename(self.data_processor.pictures_list)
            self.data_processor.add_data_to_worksheet('D%s' % str(picture+2), picture_name)    
    
    
    def close_browser(self):
        self.browser.close_browser()

    
if __name__ == "__main__":
    app = RPADataExtractorApp()
    app.run()
