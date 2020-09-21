from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
import csv
import time
import wget
import codecs
import os
import random
import string
import shutil

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def run(file):
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
        except:
            #results.append({"original": link, "result": ""})
            fails.append({"original": link, "result": ""})

    parser.driver.close()

    with open(path + "/results.csv", "w", newline="") as csv_file:
        fieldnames = ['original', 'result']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)


    downloader = Downloader()

    for result in results:
        files.append(downloader.save_image(result['result']))

    shutil.make_archive(os.path.join('results', path), 'zip', path)
    shutil.rmtree(path)
    return os.path.join('results', path) + ".zip"
