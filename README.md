# Burney
Using this repository you will be able to specify the time range you are working with and then download images accordingly

## Understanding the files in the folder
This folder includes the following files:

### Berlin_Scraper:
The berlin scraper file is a shell script. On a Mac OSX or Linux computer it will run all the commands necessary to set up the
project and begin looking for image links and then download them.
The goal with this file is to maintain the file so that you can double click it and immediately start downloading pictures.

### Pipfile.lock and Pipfile:
Without getting technical, these files belong to the *pipenv* package manager. Generally speaking, to keep project folders and the computer
as a whole more organized, it is common practice to set up *virtual environments*.


Virtual environments allow you to install modules and packages specifically to this project folder and run scripts from the environment
without changing any of the folders outside of it. A bonus that comes with this, is knowing which modules and packages are actually used
by the scripts in this project. This brings us to the two files:

These two files are used by pipenv to set up and maintain a list of packages for this project. We do not ever need to alter
them manually (**ideally**), but whenever a new package is installed, pipenv will take care of them.


### berlin_staats.py and berlin_image.py:
These are our python scripts. Techincally, these do everything. After Berlin_Scraper calls pipenv to set up our project it will first run
berlin_staats and then berlin_image.

berlin_staats first looks through the database for relevant newspapers and links to their image files and writes them to a csv file.
berlin_image then reads the csv file and downloads the images sequentially and places them in folders.

## How to use this repo
**Ideally**, (henceforth assume every sentence starts with "**Ideally**,) you will open berlin_staats, change the time range of the search, save
the file, then double click Berlin_Scraper and everything else should happen on its own.
But first you should have python set up and a way to download the repo:

### DISCLAIMER:
If you are **not** clear yet about how github works (I am not familiar either) pls do not save your own changes to the files.

### Downloading the repo from GitHub:
- Open the [Terminal](http://blog.teamtreehouse.com/introduction-to-the-mac-os-x-command-line) on Mac or Linux.
- Navigate to the folder where you would like to place the project. (I recommend
  just putting it in your home folder but sometimes that gets clunky)
- Enter the following line into the Terminal.
```
git clone https://github.com/albloomofficial/Berlin.git
```

Once this process is done you should have a folder called "Berlin" with the contents of this repo

### Downloading [Python](http://docs.python-guide.org/en/latest/starting/installation/):
The above link might seem a little daunting but it contains a very good explanation of why we are installing it this way and does a much
better job than I ever would. Essentially:

- We will install Python 3 not the, earlier, Python 2.
- Install XCode if you are on a Mac
- Install Homebrew from the Terminal
- Use Homebrew to install Python

## Running the Scripts:
I have annotated the python scripts to leave an idea of what each part does and why I wrote it this way. The steps
should be:

- Open berlin_staats.py and edit the numbers after the start_date and end_date variable.
- Save the changes to berlin_staats.py
- Double click on the Berlin Scraper file

The two chunks of code you are editing should look like this:

### Chunk 1:
```
    list_of_terms = ['african',
    'slave',
    'slavery',
    'african trade'
    ]
```
Here you will put as many terms as you would like to search for 1 by 1 separated by commas. It is important to put each word in quotes 
in order to specify to python that this is a string and not a variable.


### Chunk 2:
```
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
    ```
    
    The first three chunks "year1", "month1" and "day1" are the starting date of the search. The only part that needs editig is the part 
    in between quotes
    (the string) after the ".format" part. 
    
    The second part "year2", "month2" and "day2" are the end date of the search. The only part that needs editig 
    is the part in between quotes
    (the string) after the ".format" part. 
    
   This is still a little rough. But in the stamascraper version of this it's a little less complicated but I can't get it to work 
   as a larger function. In later versions this could be made a lot more elegant
