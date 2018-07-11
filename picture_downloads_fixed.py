from multiprocessing import cpu_count
import multiprocessing
from multiprocessing import Pool
import csv
import math
import urllib.request
import pandas as pd
import os, errno


# start date 1750
def send_pix(csv_file, cell_range, increment, save_folder):
    name = multiprocessing.current_process().name
    starting_pos = cell_range + 1
    page_num = 0
    page = 0
    god_damnit = 0
    print('{} scraping from {} to {}'.format(name, starting_pos, starting_pos + increment))
    df = pd.read_csv(csv_file)
    urls = [x for y in df.values.tolist() for x in y]
    links = urls[4::6]
    names = urls[0::6]
    location = urls[1::6]
    date = urls[2::6]
    gale = urls[5::6]
    links1 = links[starting_pos:starting_pos + increment]
    names1 = names[starting_pos:starting_pos + increment]
    location1 = location[starting_pos:starting_pos + increment]
    date1 = date[starting_pos:starting_pos + increment]
    names1 = names[starting_pos:starting_pos + increment]
    for picture in links1:
        print('{} working on page {} in article {}'.format(name, page_num + 1, god_damnit + 1))
        page = page + 1
        try:
            os.makedirs("Articles_names/{}/{}/{}".format(location1[page_num],names1[page_num], date1[page_num]))
            god_damnit = god_damnit + 1
            page = 1
            urllib.request.urlretrieve(picture, "Articles_names/{}/{}/{}/{}/{}{}.jpg".format(save_folder, location1[page_num],names1[page_num], date1[page_num], names1[page_num], page))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            urllib.request.urlretrieve(picture, "Articles_names/{}/{}/{}/{}/{}{}.jpg".format(save_folder,location1[page_num],names1[page_num], date1[page_num], names1[page_num], page))
        page_num = page_num + 1
        print('progress worker {}: {}%'.format(name, (page_num/len(names1))*100))
    print('done with one csv file')

if __name__ == "__main__":
    for csv_file in os.listdir('.'):
        if csv_file.startswith('driver'):
            df = pd.read_csv(csv_file)
            urls = [x for y in df.values.tolist() for x in y]

            save_folder = csv_file.split('_')[-1]
            save_folder = save_folder.split('.')[0]

            links = urls[4::6]
            slave_names = ["driver{}".format(i+1) for i in range(multiprocessing.cpu_count()-1)]
            increment = math.ceil(len(links) / (multiprocessing.cpu_count()-1))
            print(increment)
            procs = []
            for i in range(multiprocessing.cpu_count()-1):
                cell_range = increment * i
                new_process = multiprocessing.Process(name=slave_names[i], target=send_pix, args = (csv_file,cell_range, increment, save_folder))
                procs.append(new_process)
            for proc in procs:
                proc.start()
            for proc in procs:
                proc.join()
