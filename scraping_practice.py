from my_packages import credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import pdb


login_email = credentials.EMAIL_ADDRESS
login_password = credentials.PASSWORD
login_form_email_address_id = 'emailAddress'
login_form_password_id = 'password'
website = 'https://www.smithsfoodanddrug.com/onlineshopping/signin'
website_home = "https://www.smithsfoodanddrug.com/storecatalog/clicklistbeta/#/"
zip_code = credentials.ZIP_CODE

categories_children_left_side_selector = '#categoryList_column1 > li'
categories_children_right_side_selector = '#categoryList_column2 > li'
categories_parent_left_side_selector = '#categoryList_column1'
categories_parent_right_side_selector = '#categoryList_column2'
departments_selector = '#departmentsMenu > [ng-repeat="department in vm.departments"]'
departments_drop_down_selector = '#departmentsButton > ng-transclude > div > span.desktop.label'
home_link_selector = '#widget_breadcrumb > ul > li:nth-child(1) > a'
next_page_arrow_id = 'WC_SearchBasedNavigationResults_pagination_link_right_categoryResults'
search_bar_selector = '[data-qa="pickup store search input"]'
search_button_selector = '[data-qa="pickup store submit button"]'
shop_this_store_button_selector = 'ol > li:nth-child(2) > input'
sort_by_drop_down_id = "products_sort_by"
sort_by_alphabetical_selector = '[value="name"]'


def get_departments(return_list):
    # Click the departments drop down at the top of the page
    departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
    departments_drop_down.click()

    # Grab each of the department elements and store number of departments
    departments_list = driver.find_elements_by_css_selector(departments_selector)
    if return_list == True:
        return departments_list

def get_categories():
    # need to figure out how to grab the right categories.
    # thinking i might need to do a switch on the iterator
    # value and tie that to the uniqie ids of each category
    # lists.




    # Grab each of the categories of a department
    categories_dict = {}
    categories_parent_left_side = driver.find_element_by_css_selector(categories_parent_left_side_selector)
    categories_dict['left categories'] = categories_parent_left_side.find_elements_by_css_selector(
        categories_children_left_side_selector)
    categories_parent_right_side = driver.find_element_by_css_selector(categories_parent_right_side_selector)
    categories_dict['right categories'] = categories_parent_right_side.find_elements_by_css_selector(
        categories_children_right_side_selector)
    return categories_dict

def sort_scrape_and_click_home():
    # Sort the page alphabetically since I don't trust relevance to give me everything:
    sort_by_drop_down = driver.find_element_by_id(sort_by_drop_down_id)
    sort_by_drop_down.click()
    sort_by_alphabetical = driver.find_element_by_css_selector(sort_by_alphabetical_selector)
    sort_by_alphabetical.click()

    while True:
        # Scrape the product information:

        # Click the next pagination arrow at the bottom of the page:
        try:
            is_next_page_arrow_clickable = wait.until(EC.element_to_be_clickable((By.ID, next_page_arrow_id)))
            next_page_arrow = driver.find_element_by_id(next_page_arrow_id)
            next_page_arrow.click()
        except:
            break   

    # Click the home page link
    home_link = driver.find_element_by_css_selector(home_link_selector)
    home_link.click()
    get_departments(False)

# Driver setup and opening browser:
driver = webdriver.Chrome()
driver.implicitly_wait(5) #seconds
wait = WebDriverWait(driver, 5)
driver.get(website)

# Logging in to website:
login_email_field = driver.find_element_by_id(login_form_email_address_id)
login_email_field.clear()
login_email_field.send_keys(login_email)
login_password_field = driver.find_element_by_id(login_form_password_id)
login_password_field.clear()
login_password_field.send_keys(login_password)
login_password_field.submit()

# Selecting the right store:
shop_this_store_button = driver.find_element_by_css_selector(shop_this_store_button_selector)
shop_this_store_button.click()

# Get count of departments:
departments_count = len(get_departments(True))
department_counter = 0

# Get count of categories:
categories = get_categories()
categories_left_count = len(categories['left categories'])
categories_right_count = len(categories['right categories'])
category_left_counter = 0
category_right_counter = 0

driver.get(website_home)

# pdb.set_trace()

while department_counter < departments_count:
    # Get and click the department for this iteration:
    departments_list_for_iteration = get_departments(True)
    department_to_click = departments_list_for_iteration[department_counter]
    try:
        department_to_click.click()
    except: # try again:
        departments_list_for_iteration = get_departments(True)
        department_to_click = departments_list_for_iteration[department_counter]
        department_to_click.click()
    finally:
        pass
    

    while category_left_counter < categories_left_count:
        # Click department dropdown to fix issue with wrong categories being grabbed:
        departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
        departments_drop_down.click()
        departments_drop_down.click()
        # Get and click the category for this iteration:
        category_for_iteration = get_categories()
        category_for_iteration['left categories'][category_left_counter].click()
        sort_scrape_and_click_home()
        category_left_counter += 1 
    
    while category_right_counter < categories_right_count:
        # Click department dropdown to fix issue with wrong categories being grabbed:
        departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
        departments_drop_down.click()
        departments_drop_down.click()
        #Get and click the category for this iteration:
        category_for_iteration = get_categories()
        category_for_iteration['right categories'][category_right_counter].click()
        sort_scrape_and_click_home()
        category_right_counter += 1    

    department_counter += 1
    category_left_counter = 0
    category_right_counter = 0

driver.close()
