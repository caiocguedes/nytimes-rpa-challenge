from openpyxl import Workbook
import re
import os

class RPADataProcessor:
    def __init__(self):
       self.pictures_list = []
       self.worksheet = Workbook()
       self.active_worksheet = self.worksheet.active
       self.worksheet_filepath = os.path.join(os.getcwd(), "rpa-challenge.xlsx")
       self.pictures_path = os.path.join(os.getcwd(), 'pictures')

    #creates worksheet
    def create_worksheet(self):
        self.active_worksheet['A1'] = 'Title'
        self.active_worksheet['B1'] = 'Date'
        self.active_worksheet['C1'] = 'Description'
        self.active_worksheet['D1'] = 'Picture Filename'
        self.active_worksheet['E1'] = 'Count of search phrases in title'
        self.active_worksheet['F1'] = 'Count of search phrases in description'
        self.active_worksheet['G1'] = 'Any amount of money in title/description?'

        self.worksheet.save(self.worksheet_filepath)

    #adds data to worksheet
    def add_data_to_worksheet(self,position, data):
        self.active_worksheet[position].value = data
        
        self.worksheet.save(self.worksheet_filepath)

    #categories treatment
    def format_categories(self, categories):
        if categories == "":
            categories = "Any"
        else:
            categories = categories.replace(", ",",").split(",")
            for item in range(len(categories)):
                if "u.s." in categories[item]:
                    categories[item] = categories[item].upper()
                else:
                    categories[item] = categories[item].title()
        return categories

    #formats img src to get only the picture filename
    def format_pictures_filename(self, pictures_src_list):
        for src in pictures_src_list:
            src = src.split("/")
            for i in range(len(src)):
                if "jpg" in src[i]:
                    position = src[i].find("jpg")
                    new_picture_name = src[i][0:(position+3)]
        return new_picture_name

    #counts phrases in a given text    
    def count_search_phrases(self, phrase, full_text):
        count = full_text.lower().count(phrase.lower())
        return count

    #regex to verify if there are any money patterns in a given text
    def verify_money_in_text(self, text):
        pattern1 = r'\$\d+(\.\d+)?' #$11.1 format
        pattern2 = r'\$\d{1,3}(,\d{3})*(\.\d+)?' #$111,111.11 format
        pattern3 = r'\b\d+(\.\d+)?\s*dollars?\b' #11 dollars format
        pattern4 = r'\b\d+(\.\d+)?\s*USD\b' #11 USD format
        
        full_pattern = f'({pattern1}|{pattern2}|{pattern3}|{pattern4})'
        check_money = re.findall(full_pattern, text)
        return bool(check_money)

    #creates a folder to store the downloaded pictures
    def create_pictures_folder(self):
        if not os.path.exists(self.pictures_path):
            os.makedirs(self.pictures_path)