import time
import datetime
import csv
import pandas
import multiprocessing
import math

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import logging


__all__ = [
    "initialize_driver",
    "run_thru_pages",
    "burney_scraper",
    "get_page_count"
]


def get_page_count(start_date, end_date, search_method, browser_option, *searchterms, driver_name="Chrome"):
    search_methods = {'all' : 0, 'before' : 1, 'on' : 2, 'after' : 3, 'between' : 4}
    if start_date != "":
        d1,m1,y1 = start_date.split("/")
    if end_date != "":
        d2,m2,y2 = end_date.split("/")

    options = webdriver.ChromeOptions()
    options.add_argument(browser_option)
    print("getting page count")
    driver = webdriver.Chrome()
    driver = getattr(webdriver, driver_name)(chrome_options=options)
    driver.implicitly_wait(10)
    driver.get("http://find.galegroup.com/bncn/dispAdvSearch.do?prodId=BBCN&userGroupName=new64731")
    driver.find_element_by_xpath('//*[@id="la_dynamicLimiterField"]/option[3]').click()

    time.sleep(5)

    searchterm_count = 0
    for searchterm in searchterms:
        searchterm_count +=1
        search_field = driver.find_elements_by_css_selector('#inputFieldValue')[searchterm_count]
        search_field.click()
        search_field.send_keys(str(searchterm))



    select = Select(driver.find_element_by_name('operator(1)'))
    select.select_by_visible_text("Or")
    select = Select(driver.find_element_by_name('operator(2)'))
    select.select_by_visible_text("Or")
    date_buttons = (driver.find_elements_by_xpath('//*[@id="dateMode"]'))
    if search_methods[search_method] == 0:
        pass

    else:
        driver.execute_script("arguments[0].click();", date_buttons[search_methods[search_method]])

    if search_methods[search_method] > 0:

        #value from 1604 - 1804
        year1 = driver.find_element_by_xpath('//*[@id="year1"]')
        year1.find_element_by_xpath("//*[contains(text(), {})]".format(y1)).click()

        month1 = driver.find_element_by_xpath('//*[@id="month1"]')
        select = Select(month1)
        select.select_by_value('{}'.format(m1))

        day1 = driver.find_element_by_xpath('//*[@id="day1"]')
        select = Select(day1)
        select.select_by_value('{}'.format(d1))

    if search_methods[search_method] > 3:

        #value from 1604 - 1804
        year2 = driver.find_element_by_xpath('//*[@id="year2"]')
        select = Select(year2)
        select.select_by_value('{}'.format(y2))

        month2 = driver.find_element_by_xpath('//*[@id="month2"]')
        select = Select(month2)
        select.select_by_value('{}'.format(m2))

        day2 = driver.find_element_by_xpath('//*[@id="day2"]')
        select = Select(day2)
        select.select_by_value('{}'.format(d2))

    advanced_search = driver.find_element_by_name("inputFieldValue(0)")
    advanced_search.send_keys(Keys.RETURN)
    print('initialized')

    pages = driver.find_elements_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[3]/form/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/b[2]/span')
    pages = [page for page in pages]
    pages = pages[0].text.split(' ')[-1]
    return int(pages)
    driver.close()



def initialize_driver(page, start_date, end_date, search_method, browser_option, *searchterms, driver_name="Chrome"):

    search_methods = {'all' : 0, 'before' : 1, 'on' : 2, 'after' : 3, 'between' : 4}
    if start_date != "":
        d1,m1,y1 = start_date.split("/")
    if end_date != "":
        d2,m2,y2 = end_date.split("/")

    print('testing 1')

    options = webdriver.ChromeOptions()
    options.add_argument(browser_option)
    name = multiprocessing.current_process().name
    print(name, "initializing driver")
    # driver = webdriver.Chrome()
    driver = getattr(webdriver, driver_name)(chrome_options=options)
    driver.implicitly_wait(10)
    driver.get("http://find.galegroup.com/bncn/dispAdvSearch.do?prodId=BBCN&userGroupName=new64731")
    driver.find_element_by_xpath('//*[@id="la_dynamicLimiterField"]/option[3]').click()

    time.sleep(5)

    searchterm_count = 0
    for searchterm in searchterms:
        searchterm_count +=1
        search_field = driver.find_elements_by_css_selector('#inputFieldValue')[searchterm_count]
        search_field.click()
        search_field.send_keys(str(searchterm))



    select = Select(driver.find_element_by_name('operator(1)'))
    select.select_by_visible_text("Or")
    select = Select(driver.find_element_by_name('operator(2)'))
    select.select_by_visible_text("Or")
    date_buttons = (driver.find_elements_by_xpath('//*[@id="dateMode"]'))
    if search_methods[search_method] == 0:
        pass

    else:
        driver.execute_script("arguments[0].click();", date_buttons[search_methods[search_method]])

    if search_methods[search_method] > 0:

        #value from 1604 - 1804
        year1 = driver.find_element_by_xpath('//*[@id="year1"]')
        year1.find_element_by_xpath("//*[contains(text(), {})]".format(y1)).click()

        month1 = driver.find_element_by_xpath('//*[@id="month1"]')
        select = Select(month1)
        select.select_by_value('{}'.format(m1))

        day1 = driver.find_element_by_xpath('//*[@id="day1"]')
        select = Select(day1)
        select.select_by_value('{}'.format(d1))

    if search_methods[search_method] > 3:

        #value from 1604 - 1804
        year2 = driver.find_element_by_xpath('//*[@id="year2"]')
        select = Select(year2)
        select.select_by_value('{}'.format(y2))

        month2 = driver.find_element_by_xpath('//*[@id="month2"]')
        select = Select(month2)
        select.select_by_value('{}'.format(m2))

        day2 = driver.find_element_by_xpath('//*[@id="day2"]')
        select = Select(day2)
        select.select_by_value('{}'.format(d2))

    advanced_search = driver.find_element_by_name("inputFieldValue(0)")
    advanced_search.send_keys(Keys.RETURN)
    print(name, 'initialized')

    #wait for the website to load, then click on "Page"
    print(name, 'waiting for elements to load')

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[3]/form/table[3]/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/a[1]').click()
    time.sleep(5)
    select = Select(driver.find_element_by_xpath('//*[@id="fascimileForm"]/table/tbody/tr/td[5]/font/select'))
    select.select_by_visible_text("100%")
    time.sleep(5)


    page_selector = driver.find_element_by_xpath('//*[@id="currPosTop"]')
    page_selector.click()
    page_selector.clear()
    page_selector.send_keys(page)
    go_button = driver.find_element_by_css_selector('#go')
    driver.execute_script("arguments[0].click();", go_button)


    return driver


def run_thru_pages(filename, page_range, increment, start_date, end_date, search_method, browser_option, *searchterms):

    name = multiprocessing.current_process().name
    print(page_range)
    page = page_range + 1
    driver = initialize_driver(page, start_date, end_date, search_method, browser_option, *searchterms)
    print(name, ' scanning pages ', page_range, " to ", page_range + increment)
    while page < (page_range + increment):
        print("is {} smaller than {}".format(page, page_range + increment))
        print(name, 'I am on article : ', page)
        if page != 0:
            if page % 100 == 0:
                print(name, " : Trying to not overload the server")
                time.sleep(60)

        # reset lists
        author = []
        location = []
        date = []
        sources = []
        src_links = []
        article_nm = []
        gale_number = []

        try:
            #retrieve article title
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span/b[1]/i')
            author_date = input_element.text
            author.append(author_date)

            #retrieve city of origin
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span').text
            location_date = input_element.split(')')
            dity = location_date[-2].split(' (')
            location.append(dity[-1])

            #retrieve date
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span').text
            dirty = input_element.split('), ')[1]
            time_of_publishing = dirty.split('.')[0]
            date.append(time_of_publishing)

            #retrieve source of file (mostly burney)
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/hits[1]/table/tbody/tr/td/table/tbody/tr[1]/td/span/i')
            sources.append(input_element.text)

            #retrieve img link
            image = driver.find_element_by_id("fascimileImg")
            img_src = image.get_attribute("src")
            src_links.append(img_src)

            #retrieve gale number
            input_element = driver.find_element_by_xpath('//*[@id="documentTable"]/tbody/tr/td[3]/div[2]')
            gale_number.append(input_element.text.split(': ')[1])

            final_data = list(zip(*[author,location, date, sources, src_links, gale_number]))
            write_to_file(output_list, filename)

            time.sleep(1)
            page += 1
            print(name, ": Moving onto article {}".format(page))

            next_button = driver.find_elements_by_xpath('//img[@src="images/b_next.gif"]')
            next_button[0].click()

        except:
            time.sleep(60*60)
            driver = initialize_driver(page, start_date, end_date, search_method, browser_option, *searchterms)

def write_to_file(final_data, filename):
    final_data.to_csv(filename, mode='a', header=False)
    # with open(filename, 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(final_data)

def burney_scraper(*searchterms, start_date = "", end_date = "", search_method = "all", browser_option = "start-maximized"):
    filename_date = datetime.date.today()

    filename = 'Srcs_Burney_{}_slave.csv'.format(str(filename_date))
    slave_names = ["driver{}".format(i+1) for i in range(int(multiprocessing.cpu_count()*3/4))]
    pages = get_page_count(start_date, end_date, search_method, browser_option, *searchterms)
    increment = math.ceil(pages / (multiprocessing.cpu_count()*3/4))
    print(increment)

    # pool = multiprocessing.Pool()
    procs = []
    for i in range(int(multiprocessing.cpu_count()*3/4)):
        url_range = increment * i

        new_process = multiprocessing.Process(name=slave_names[i],
        target=run_thru_pages,
        args = (filename, url_range, increment,
        start_date, end_date,
        search_method, browser_option, *searchterms))

        procs.append(new_process)
    for new_process in procs:
        new_process.start()
    for new_process in procs:
        new_process.join()
        new_process.close()
