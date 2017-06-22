from my_packages import credentials

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import pdb
#pdb.set_trace()


login_email = credentials.EMAIL_ADDRESS
login_password = credentials.PASSWORD
login_form_email_address_id = 'emailAddress'
login_form_password_id = 'password'
website = 'https://www.smithsfoodanddrug.com/onlineshopping/signin'
webiste_home = "https://www.smithsfoodanddrug.com/storecatalog/clicklistbeta/#/"
zip_code = credentials.ZIP_CODE

departments_children_left_side_selector = '#categoryList_column1 > li'
departments_children_right_side_selector = '#categoryList_column2 > li'
departments_drop_down_selector = '#departmentsButton > ng-transclude > div > span.desktop.label'
departments_parent_left_side_id = 'categoryList_column1'
departments_parent_right_side_id = 'categoryList_column2'
home_link_selector = '#widget_breadcrumb > ul > li:nth-child(1) > a'
next_page_arrow_id = 'WC_SearchBasedNavigationResults_pagination_link_right_categoryResults'
search_bar_selector = '[data-qa="pickup store search input"]'
search_button_selector = '[data-qa="pickup store submit button"]'
shop_this_store_button_selector = 'ol > li:nth-child(2) > input'
sort_by_drop_down_id = "products_sort_by"
sort_by_alphabetical_selector = '[value="name"]'


# Driver setup and opening browser:
driver = webdriver.Chrome()
driver.implicitly_wait(10) #seconds
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


    
# Click the Departments drop down at the top of the page
departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
departments_drop_down.click()

# Grab each of the links within each of the departments for future use
departments_parent_left_side = driver.find_element_by_id(departments_parent_left_side_id)
departments_children_left_side_list = departments_parent_left_side.find_elements_by_css_selector(
    departments_children_left_side_selector)

departments_parent_right_side = driver.find_element_by_id(departments_parent_right_side_id)
departments_children_right_side_list = departments_parent_right_side.find_elements_by_css_selector(
    departments_children_right_side_selector)

# Click the first item on the left side of the departments list
wait = WebDriverWait(driver, 10)
first_department_in_list = wait.until(EC.visibility_of(departments_children_left_side_list[0]))    
first_department_in_list.click()

# Sort the page alphabetically since relevance could change anytime
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

#   
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
