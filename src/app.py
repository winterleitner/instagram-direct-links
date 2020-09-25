from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
import csv
import time
import wget
import codecs
import os
import random
import string
import shutil
import sys

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

#uses selenium to update links in an elfsight gallery
def update_gallery(file, gallery, email, password, append=False):
    #driver = webdriver.Safari()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    # self.driver = webdriver.Safari()
    driver = webdriver.Chrome(options=chrome_options)

    links = []
    stream = codecs.iterdecode(file.stream, 'utf-8')
    csv_reader = csv.reader(stream, delimiter=',')
    for row in csv_reader:
        links.append(row[0])

    #driver.set_window_size(1800, 724)
    driver.get("https://apps.elfsight.com/panel/applications/instashow/")
    mail = driver.find_element_by_name("email")
    mail.send_keys(email)
    passsword = driver.find_element_by_name("password")
    passsword.send_keys(password)
    passsword.send_keys(Keys.RETURN)
    time.sleep(3)
    driver.get(f"https://apps.elfsight.com/panel/applications/instashow/edit/{gallery}/")
    time.sleep(2)

    if not append:
        # remove all existing entries for gallery
        driver.execute_script("""
            while (document.getElementsByClassName("ea-editor-property-control-tags-item-remove").length > 0) {
                document.getElementsByClassName("ea-editor-property-control-tags-item-remove").forEach(e => e.click())
            }
        """)

    input = driver.find_element_by_class_name("ea-editor-property-control-tags-input")
    for link in links:
        input.send_keys(link)
        input.send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element_by_class_name("widgets-edit-header-actions-item-apply").send_keys(Keys.ENTER)
    driver.close()
    return True


def scrape(file):
    path = get_random_string(8)

    try:
        os.mkdir(path)
        os.mkdir(path + "/downloads")
    except OSError:
        print("Creation of the directory %s failed" % path)

    links = []
    stream = codecs.iterdecode(file.stream, 'utf-8')
    csv_reader = csv.reader(stream, delimiter=',')
    for row in csv_reader:
        links.append(row[0])

    class Parser:
        def __init__(self):
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_prefs = {}
            chrome_options.experimental_options["prefs"] = chrome_prefs
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            #self.driver = webdriver.Safari()
            self.driver = webdriver.Chrome(options=chrome_options)

        def process_post(self, url):
            self.driver.get(url)
            time.sleep(1)

            # Parse the html content
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            print(soup, file=sys.stderr)
            url = soup.article.find_all('div', recursive=False)[1].img['src']
            return url


    class Downloader:
        def save_image(self, url):
            # Use wget download method to download specified image url.
            image_filename = wget.download(url, out=path+"/downloads")
            return image_filename

    results = []
    fails = []
    files = []

    parser = Parser()

    for link in links:
        try:
            results.append({"original": link, "result": parser.process_post(link)})
        except Exception as ex:
            #results.append({"original": link, "result": ""})
            fails.append({"original": link, "failure": ex})

    parser.driver.close()

    with open(path + "/results.csv", "w", newline="") as csv_file:
        fieldnames = ['original', 'result']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    with open(path + "/fails.csv", "w", newline="") as csv_file:
        fieldnames = ['original', 'failure']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in fails:
            writer.writerow(result)


    downloader = Downloader()

    for result in results:
        files.append(downloader.save_image(result['result']))

    shutil.make_archive(os.path.join('results', path), 'zip', path)
    shutil.rmtree(path)
    return os.path.join('results', path) + ".zip"
