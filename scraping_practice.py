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

departments_count = 0

categories_children_left_side_selector = '#categoryList_column1 > li'
categories_children_right_side_selector = '#categoryList_column2 > li'
categories_parent_left_side_id = 'categoryList_column1'
categories_parent_right_side_id = 'categoryList_column2'
departments_selector = '#departmentsMenu > [ng-repeat="department in vm.departments"]'
departments_drop_down_selector = '#departmentsButton > ng-transclude > div > span.desktop.label'
home_link_selector = '#widget_breadcrumb > ul > li:nth-child(1) > a'
next_page_arrow_id = 'WC_SearchBasedNavigationResults_pagination_link_right_categoryResults'
search_bar_selector = '[data-qa="pickup store search input"]'
search_button_selector = '[data-qa="pickup store submit button"]'
shop_this_store_button_selector = 'ol > li:nth-child(2) > input'
sort_by_drop_down_id = "products_sort_by"
sort_by_alphabetical_selector = '[value="name"]'


def get_departments():
    # Click the departments drop down at the top of the page
    departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
    departments_drop_down.click()

    # Grab each of the department elements and store number of departments
    departments_list = driver.find_elements_by_css_selector(departments_selector)
    return departments_list

def get_categories():
    # Grab each of the categories of a department
    categories_dict = {}
    categories_parent_left_side = driver.find_element_by_id(categories_parent_left_side_id)
    categories_dict['left categories'] = categories_parent_left_side.find_elements_by_css_selector(
        categories_children_left_side_selector)
    categories_parent_right_side = driver.find_element_by_id(categories_parent_right_side_id)
    categories_dict['right categories'] = categories_parent_right_side.find_elements_by_css_selector(
        categories_children_right_side_selector)
    return categories_dict



# Driver setup and opening browser:
driver = webdriver.Chrome()
driver.implicitly_wait(10) #seconds
wait = WebDriverWait(driver, 10)
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
departments_count = len(get_departments())
driver.get(website_home)

pdb.set_trace()

i = 0
while i < departments_count:
    # Get the department for this iteration:
    departments_list_for_iteration = get_departments()
    departments_list_for_iteration[i].click()

    # Grab each of the categories of a department and store number of categories
    categories = get_categories()
    categories_left_count = len(categories['left categories'])
    categories_right_count = len(categories['right categories'])

    i+= 1
# # Click the first department
# first_department_in_list = wait.until(EC.visibility_of(departments_list[0]))
# first_department_in_list.click()



# Grab each of the categories of a department and store number of categories
categories_parent_left_side = driver.find_element_by_id(categories_parent_left_side_id)
categories_children_left_side_list = categories_parent_left_side.find_elements_by_css_selector(
    categories_children_left_side_selector)
categories_left_count = categories_children_left_side_list.len()

categories_parent_right_side = driver.find_element_by_id(categories_parent_right_side_id)
categories_children_right_side_list = categories_parent_right_side.find_elements_by_css_selector(
    categories_children_right_side_selector)
categories_right_count = categories_children_right_side_list.len()

# Click the first item on the left side of the categories list
first_category_in_list = wait.until(EC.visibility_of(categories_children_left_side_list[0]))    
first_category_in_list.click()

# Sort the page alphabetically since I don't trust relevance to give me everything
sort_by_drop_down = driver.find_element_by_id(sort_by_drop_down_id)
sort_by_drop_down.click()
sort_by_alphabetical = driver.find_element_by_css_selector(sort_by_alphabetical_selector)
sort_by_alphabetical.click()

# Click the next pagination arrow at the bottom of the page
next_page_arrow = driver.find_element_by_id(next_page_arrow_id)
next_page_arrow.click()

# Click the home page link
home_link = driver.find_element_by_css_selector(home_link_selector)
home_link.click()

#   -For each of the links:
#      -When visiting each link:
#         1. Scrape the data from the page
#               a. Figure out how to store the scraped data
#               b. Need to research implications of grabbing images as well
#         2. Click the next page of the link using the pagination at the bottom of the page
#         3. Scrape the date from each paginated page
#   -Using Pandas, organize and clean data
#   -Export data to .csv to be consumed by web app


driver.close()
