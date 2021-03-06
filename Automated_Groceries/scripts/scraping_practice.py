from my_packages import credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from decimal import Decimal
import pdb
import re
import os
import sys

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Automated_Groceries.settings")
import django
django.setup()
from main.models import Product


# Regex Pattern:
reg = re.compile("\d.+")

# Credentials:
login_email = credentials.EMAIL_ADDRESS
login_password = credentials.PASSWORD
login_form_email_address_id = 'emailAddress'
login_form_password_id = 'password'

# Urls:
website = 'https://www.smithsfoodanddrug.com/onlineshopping/signin'
website_home = "https://www.smithsfoodanddrug.com/storecatalog/clicklistbeta/#/"

# Selectors
add_to_cart_button_selector = '[ng-click="vm.addToCart()"]'
categories_children_left_side_selector = '#categoryList_column1 > li > a'
categories_children_right_side_selector = '#categoryList_column2 > li > a'
categories_parent_left_side_selector = '#categoryList_column1'
categories_parent_right_side_selector = '#categoryList_column2'
delivery_popup_close_button_selector = 'body > dialog > div'
departments_drop_down_selector = '#departmentsButton > ng-transclude > div > span.desktop.label'
departments_selector = '#departmentsMenu > [ng-repeat="department in vm.departments"] > a'
home_link_selector = '#widget_breadcrumb > ul > li:nth-child(1) > a'
instructions_id = "instructions_"
next_page_arrow_id = 'WC_SearchBasedNavigationResults_pagination_link_right_categoryResults'
product_info_class = 'product_info'
product_name_class = 'product_name'
product_price_class = 'product_price'
product_uom_class = 'product_uom'
product_upc_selector = '.product_name > a'
search_bar_selector = '[data-qa="pickup store search input"]'
search_button_selector = '[data-qa="pickup store submit button"]'
single_product_name_id = "PageHeading_"
single_product_price_selector = "cl-product-card-price"
single_product_right_column_selector = "#content > ui-view > cl-product-details > div > div > div.right-col > cl-product-details-info > div.slot5"
single_product_sku_class = "sku"
single_product_uom_id = "uom_price_sizing_display_"
shop_this_store_button_selector = 'ol > li:nth-child(1) > input'
sort_by_drop_down_id = "products_sort_by"
sort_by_alphabetical_selector = '[value="name"]'


def get_departments(return_list):
    # Click the departments drop down at the top of the page
    departments_drop_down_clickable = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, departments_drop_down_selector)))
    departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
    departments_drop_down.click()

    # Grab each of the department elements and store number of departments
    if return_list == True: 
        list_of_department_ids = []
        departments_list = driver.find_elements_by_css_selector(departments_selector)
        for element in departments_list:
            department_id = element.get_attribute('id')
            list_of_department_ids.append(department_id)
        return list_of_department_ids


def get_categories(department_id):
    sibling_selector = "#" + department_id + " + div"
    categories_dict = {}
    categories_left_id_list = []
    categories_right_id_list = []
    right_categories = None

    # Wait until the correct categories are displayed:
    categories_parent = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, sibling_selector)))

    # Grab the category elements from left and right sides:
    categories_parent_left_side = driver.find_element_by_css_selector(categories_parent_left_side_selector)
    left_categories = categories_parent_left_side.find_elements_by_css_selector(
        categories_children_left_side_selector)
    
    # Not every department has right side categories:
    try:
        categories_parent_right_side = driver.find_element_by_css_selector(categories_parent_right_side_selector)
        right_categories = categories_parent_right_side.find_elements_by_css_selector(
            categories_children_right_side_selector)
    except:
        pass

    # Save the ids for each of the categories:
    for category in left_categories:
        category_id = category.get_attribute("id")
        categories_left_id_list.append(category_id)
        categories_dict['left ids'] = categories_left_id_list
    if right_categories != None:
        for category in right_categories:
            category_id = category.get_attribute("id")
            categories_right_id_list.append(category_id)
            categories_dict['right ids'] = categories_right_id_list
    else:
        categories_dict['right ids'] = []

    return categories_dict


def scrape_and_click_home(multiple_products):
    if multiple_products == False:
        # Handle the single item in a category case
        get_product_information_for_single_product()
        driver.get(website_home)
    else:
        # Multiple products are present on the page:
        try:
            is_next_page_arrow_clickable = wait.until(EC.element_to_be_clickable((By.ID, next_page_arrow_id)))
            # A clickable arrow at this point means we are not on the last pagination page and there are multiple products present:
            if is_next_page_arrow_clickable:
                # Scrape the product information:
                get_product_information_for_multiple_products()
                next_page_arrow = driver.find_element_by_id(next_page_arrow_id)
                next_page_arrow.click()
                multiple_products_again = number_of_products_on_category_page_more_than_one()
                scrape_and_click_home(multiple_products_again)
        # A non-clickable arrow at this point means we are on the last pagination page with multiple products present:
        except:
            # Scrape the product information:
            get_product_information_for_multiple_products
            # Click the home page link:
            home_link = driver.find_element_by_css_selector(home_link_selector)
            home_link.click()


def sort_page():
    # Sort the page alphabetically since I don't trust relevance to give me everything:
    sort_by_drop_down_clickable = wait.until(EC.element_to_be_clickable((By.ID, sort_by_drop_down_id)))
    sort_by_drop_down = driver.find_element_by_id(sort_by_drop_down_id)
    sort_by_drop_down.click()
    sort_by_alphabetical = driver.find_element_by_css_selector(sort_by_alphabetical_selector)
    sort_by_alphabetical.click()


def get_product_information_for_multiple_products():
    # Wait for each product to be loaded on page:
    are_products_loaded = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, product_info_class)))
    # Retrieve information for each product:
    all_products_on_page = driver.find_elements_by_class_name(product_info_class)
    # Create new Product objects in database. Using upc on get_or_create since that value should be unique:
    for product in all_products_on_page:
        product_name = product.find_element_by_class_name(product_name_class).text
        product_price_list = product.find_element_by_class_name(product_price_class).text.split("$")
        # Calling split in the previous line will always create an array of at least 2 items
        # unless the split is called on an empty string. Empty strings should only ever show
        # up if the product does not have a price.
        if len(product_price_list) > 1:
            product_price = reg.match(product_price_list[-1]).group()
        else:
            product_price = 0
        product_price_decimal = Decimal(product_price)
        product_unit = product.find_element_by_class_name(product_uom_class).text
        product_upc = product.find_element_by_css_selector(product_upc_selector).get_attribute('data-upc')
        # Save data:
        store_product_information(product_upc, product_name, product_price_decimal, product_unit)


def get_product_information_for_single_product():
    # Ensure the product is loaded on the page:
    is_product_loaded = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, single_product_right_column_selector)))
    product_information = driver.find_element_by_css_selector(single_product_right_column_selector)
    # Retrive unique upc number for product by stripping "SKU:" from text of sku element:
    product_upc = product_information.find_element_by_class_name(single_product_sku_class).text.strip("SKU:")
    # Can use upc number to find other needed information:
    product_name = product_information.find_element_by_id(single_product_name_id + product_upc).text
    product_unit = product_information.find_element_by_id(single_product_uom_id + product_upc).text
    product_price_list = product_information.find_element_by_css_selector(single_product_price_selector).text.split("$")
    # See explanation in get_product_information_for_multiple_products() for what's going on here:
    if len(product_price_list) > 1:
        product_price = reg.match(product_price_list[-1]).group()
    else:
        product_price = 0
    product_price_decimal = Decimal(product_price)
    # Save data:
    store_product_information(product_upc, product_name, product_price_decimal, product_unit)


def number_of_products_on_category_page_more_than_one():
    try:
        single_product_on_category_page = wait.until(EC.visibility_of_element_located((By.ID, instructions_id)))
        return False
    except:
        return True

def store_product_information(upc, name, price, uof):
    new_product, created = Product.objects.get_or_create(upc=upc)
    new_product.name = name
    new_product.price = price
    new_product.unit_of_measurement = uof
    new_product.save()


def fix_category_id(list_of_category_ids):
    # There is an issue with how the ids of categories are being generated that I need to work around:
    fixed_list_of_ids = []
    for category_id in list_of_category_ids:
        new_list = list(category_id)
        new_list[14] = new_list[17]
        fixed_id = "".join(new_list)
        fixed_list_of_ids.append(fixed_id)
    return fixed_list_of_ids


# Driver setup and opening browser:
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)
driver.get(website)

# Logging in to website:
login_email_field_clickable = wait.until(EC.element_to_be_clickable((By.ID, login_form_email_address_id)))
login_email_field = driver.find_element_by_id(login_form_email_address_id)
login_email_field.clear()
login_email_field.send_keys(login_email)
login_password_field = driver.find_element_by_id(login_form_password_id)
login_password_field.clear()
login_password_field.send_keys(login_password)
login_password_field.submit()

# Selecting the right store:
shop_this_store_button_clickable = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, shop_this_store_button_selector)))
shop_this_store_button = driver.find_element_by_css_selector(shop_this_store_button_selector)
shop_this_store_button.click()

# Close delivery popup:
delivery_popup_close_button_clickable = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, delivery_popup_close_button_selector)))
delivery_popup_close_button = driver.find_element_by_css_selector(delivery_popup_close_button_selector)
delivery_popup_close_button.click()

# Get count of departments:
departments = get_departments(True)
departments_count = len(departments)
department_counter = 0

# Navigation loop:
while department_counter < departments_count:
    driver.get(website_home)
    # Get and click the department for this iteration:
    departments_ids = get_departments(True)

    is_department_to_click_clickable = wait.until(EC.element_to_be_clickable((By.ID, departments_ids[department_counter])))
    department_to_click = driver.find_element_by_id(departments_ids[department_counter])
    department_to_click.click()

    # Get count of categories:
    categories = get_categories(departments_ids[department_counter])
    categories_left_count = len(categories['left ids'])
    categories_right_count = len(categories['right ids'])
    category_left_counter = 0
    category_right_counter = 0

    while category_left_counter < categories_left_count:
        # Get and click the category for this iteration:
        categories = get_categories(departments_ids[department_counter])
        categories['left ids'] = fix_category_id(categories['left ids'])

        is_category_to_click_clickable = wait.until(EC.element_to_be_clickable((By.ID, categories['left ids'][category_left_counter])))
        category_to_click = driver.find_element_by_id(categories['left ids'][category_left_counter])
        category_to_click.click()

        multiple_products = number_of_products_on_category_page_more_than_one()
        if multiple_products == True:
            # If there is only one product, we shouldn't call sort_page()
            sort_page()
            scrape_and_click_home(multiple_products)
        else:
            scrape_and_click_home(multiple_products)
        # Click the departments drop down at the top of the page
        departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
        departments_drop_down.click()
        category_left_counter += 1 
    
    while category_right_counter < categories_right_count:
        # Get and click the category for this iteration:
        categories = get_categories(departments_ids[department_counter])
        categories['right ids'] = fix_category_id(categories['right ids'])
        
        is_category_to_click_clickable = wait.until(EC.element_to_be_clickable((By.ID, categories['right ids'][category_right_counter])))
        category_to_click = driver.find_element_by_id(categories['right ids'][category_right_counter])
        category_to_click.click()

        multiple_products = number_of_products_on_category_page_more_than_one()
        if multiple_products == True:
            # If there is only one product, we shouldn't call sort_page()
            sort_page()
            scrape_and_click_home(multiple_products)
        else:
            scrape_and_click_home(multiple_products)
        # Click the departments drop down at the top of the page
        departments_drop_down = driver.find_element_by_css_selector(departments_drop_down_selector)
        departments_drop_down.click()
        category_right_counter += 1    

    department_counter += 1

driver.close()
