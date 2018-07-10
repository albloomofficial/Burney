from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import datetime
import csv
import multiprocessing
from multiprocessing import cpu_count
import math
from selenium.webdriver.support.ui import Select


def get_page_count(term):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = getattr(webdriver, 'Chrome')(chrome_options=options)
        driver.implicitly_wait(10)
        driver.get("http://find.galegroup.com/bncn/dispAdvSearch.do?prodId=BBCN&userGroupName=new64731")
        driver.find_element_by_xpath('//*[@id="la_dynamicLimiterField"]/option[3]').click()
        sleep(5)
        search_field = driver.find_elements_by_css_selector('#inputFieldValue')[1]
        search_field.click()
        search_field.send_keys(term)

        date_buttons = (driver.find_elements_by_xpath('//*[@id="dateMode"]'))
        driver.execute_script("arguments[0].click();", date_buttons[4])


        year1 = driver.find_element_by_xpath('//*[@id="year1"]')
        select = Select(year1)
        select.select_by_value('{}'.format('1783'))

        month1 = driver.find_element_by_xpath('//*[@id="month1"]')
        select = Select(month1)
        select.select_by_value('{}'.format('01'))

        day1 = driver.find_element_by_xpath('//*[@id="day1"]')
        select = Select(day1)
        select.select_by_value('{}'.format('01'))


        #value from 1604 - 1804
        year2 = driver.find_element_by_xpath('//*[@id="year2"]')
        select = Select(year2)
        select.select_by_value('{}'.format('1787'))

        month2 = driver.find_element_by_xpath('//*[@id="month2"]')
        select = Select(month2)
        select.select_by_value('{}'.format('12'))

        day2 = driver.find_element_by_xpath('//*[@id="day2"]')
        select = Select(day2)
        select.select_by_value('{}'.format('31'))

        advanced_search = driver.find_element_by_name("inputFieldValue(0)")
        advanced_search.send_keys(Keys.RETURN)

        pages = driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[3]/form/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/b[2]/span').text
        pages = pages.split(' ')[-1]
        pages = int(pages)

        driver.close()
        return pages


def initialize_driver(page, term):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    name = multiprocessing.current_process().name
    print(name, "initializing driver")
    driver = getattr(webdriver, 'Chrome')(chrome_options=options)

    driver.get("http://find.galegroup.com/bncn/dispAdvSearch.do?prodId=BBCN&userGroupName=new64731")
    driver.find_element_by_xpath('//*[@id="la_dynamicLimiterField"]/option[3]').click()
    sleep(5)
    search_field = driver.find_elements_by_css_selector('#inputFieldValue')[1]
    search_field.click()
    search_field.send_keys(term)

    date_buttons = (driver.find_elements_by_xpath('//*[@id="dateMode"]'))
    driver.execute_script("arguments[0].click();", date_buttons[4])


    year1 = driver.find_element_by_xpath('//*[@id="year1"]')
    select = Select(year1)
    select.select_by_value('{}'.format('1783'))

    month1 = driver.find_element_by_xpath('//*[@id="month1"]')
    select = Select(month1)
    select.select_by_value('{}'.format('01'))

    day1 = driver.find_element_by_xpath('//*[@id="day1"]')
    select = Select(day1)
    select.select_by_value('{}'.format('01'))


    #value from 1604 - 1804
    year2 = driver.find_element_by_xpath('//*[@id="year2"]')
    select = Select(year2)
    select.select_by_value('{}'.format('1787'))

    month2 = driver.find_element_by_xpath('//*[@id="month2"]')
    select = Select(month2)
    select.select_by_value('{}'.format('12'))

    day2 = driver.find_element_by_xpath('//*[@id="day2"]')
    select = Select(day2)
    select.select_by_value('{}'.format('31'))

    advanced_search = driver.find_element_by_name("inputFieldValue(0)")
    advanced_search.send_keys(Keys.RETURN)
    print(name, ' initialized')

    #wait for the website to load, then click on "Page"
    print(name, 'waiting for elements to load')

    sleep(5)
    driver.find_element_by_xpath('//*[@id="content"]/table[1]/tbody/tr/td[3]/form/table[3]/tbody/tr[1]/td[2]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/a[1]').click()
    sleep(5)
    select = Select(driver.find_element_by_xpath('//*[@id="fascimileForm"]/table/tbody/tr/td[5]/font/select'))
    select.select_by_visible_text("200%")
    sleep(5)


    page_selector = driver.find_element_by_xpath('//*[@id="currPosTop"]')
    page_selector.click()
    page_selector.clear()
    page_selector.send_keys(page)
    go_button = driver.find_element_by_css_selector('#go')
    driver.execute_script("arguments[0].click();", go_button)
    return driver


def run_thru_pages(term, page_range, increment):
    filename_date = str(datetime.date.today())
    name = multiprocessing.current_process().name
    with open('{}_{}_{}.csv'.format(name, filename_date, term),
    'w') as f:
            writer = csv.writer(f)
            writer.writerow(['origin',
            'location',
            'date',
            'source',
            'image_link',
            'gale_number'])
    page = page_range + 1
    driver = initialize_driver(page, term)
    print(name, ' scanning pages ', page_range, " to ", page_range + increment)
    while page < page_range + increment:
        print(name, 'I am on article : ', page)
        if page != 0:
            if page % 100 == 0:
                print(name, " : Trying to not overload the server")
                sleep(60)

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

            sleep(1)
            next_button = driver.find_elements_by_xpath('//img[@src="images/b_next.gif"]')

            page += 1
            print(name, ": Moving onto article {}".format(page))
            next_button[0].click()

            #append information to a list and print it as a new row in the csv
            final_data = zip(*[author,location, date, sources, src_links, gale_number])
            with open('Srcs_Burney_{}_{}.csv'.format(filename_date, term), 'a') as f:
                writer = csv.writer(f)
                writer.writerows(final_data)
        except:
            sleep(60*60)
            driver = initialize_driver(page)


if __name__ == "__main__":

    list_of_terms = ['african',
    'slave',
    'slavery',
    'african trade'
    ]

    for term in list_of_terms:
        print(term)
        filename_date = str(datetime.date.today())


        pages = get_page_count(term)
        print(pages)

        driver_names = ["driver{}".format(i+1) for i in range(int(cpu_count()))]

        increment = math.ceil(pages / int(cpu_count()))
        print(increment)
        procs = []
        for i in range(int(cpu_count())):
            url_range = increment * i
            new_process = multiprocessing.Process(name=driver_names[i], target=run_thru_pages, args = (term, url_range, increment))
            procs.append(new_process)
        for process in procs:
            process.start()
        for process in procs:
            process.join()
