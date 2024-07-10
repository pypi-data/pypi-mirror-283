import os
import re
import time
import random
import psutil
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pdf_crawler.report_generator import ReportGenerator
#from report_generator import ReportGenerator
import tkinter
import shutil
import tempfile
import concurrent.futures
import json
from retry import retry
import string

class SeleniumCrawler:
    def __init__(self, initial_link, console_text):
        self.debug = False # Set to True to debug to the console

        self.max_workers = 5
        self.files_to_convert = []
        self.initial_link = initial_link
        self.console_text = console_text
        self.chrome_processes = []
        self.report_name = None
        self.witness_evidence_folder = "Witness Evidence"
        self.published_evidence_folder = "Published Evidence"
        self.temp_evidence_folder = "temp_evidence"
        self.report_trimmed_pdf = "report-trimmed.pdf"
        self.combined_merged_evidence = "combined_merged_evidence.pdf"
        self.numbered_evidence ="numbered_evidence.pdf"
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
        ]

    def debug_message(self, message):
        if self.debug:
            print(message)

    def console_message(self, message):
        """
        Log updates to the console instance defined in ui.py for the client to see
        the crawler and pdf generator progress.

        Args:
            message (str): Text to be displayed to the console.
        """

        self.console_text.configure(state='normal')
        self.console_text.insert(tkinter.END, message + '\n')
        self.console_text.configure(state='disabled')
        self.console_text.yview(tkinter.END)

    def create_selenium_driver(self, download_dir):
        """
        Creates a webdriver to run an instance of Selenium.

        Args:
            download_dir (str): The directory for which this instance of the driver should download files to.

        Returns:
            tuple: A tuple containing the driver instance and a dictionary with the main PID and child PIDs.
        """

        options = Options()
        options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--window-size=1920,1080')

        download_abs_path = str(Path.cwd() / download_dir)

        preferences = {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.stylesheets": 2,
            "download.default_directory": download_abs_path,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        
        options.add_experimental_option("prefs", preferences)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        main_pid = driver.service.process.pid
        self.debug_message(f"Main Chrome process PID: {main_pid}")

        child_pids = []
        try:
            main_process = psutil.Process(main_pid)
            child_pids = [child.pid for child in main_process.children(recursive=True)]
            self.debug_message(f"Child processes PIDs: {child_pids}")
        except psutil.NoSuchProcess:
            self.debug_message("Main process not found, couldn't fetch child processes.")

        process_info = {'main_pid': main_pid, 'child_pids': child_pids}

        self.chrome_processes.append(process_info)
        self.debug_message(f"Tracked processes: {self.chrome_processes}")


        self.debug_message(f"Process Info = {process_info}")
        return driver, process_info

    def kill_chrome_process(self, pid_dict):
        """
        Terminate the specified Chrome process and its child processes by dictionary.

        Args:
            pid_dict (dict): A dictionary containing the main PID and child PIDs of the Chrome process to terminate.
        """


        main_pid = pid_dict.get('main_pid')
        child_pids = pid_dict.get('child_pids', [])

        if not main_pid or not isinstance(child_pids, list):
            self.debug_message(f"Invalid PID dictionary: {pid_dict}")
            return

        self.chrome_processes = [proc for proc in self.chrome_processes if proc['main_pid'] != main_pid]

        pids_to_kill = [main_pid] + child_pids
        self.debug_message(f"Terminating PIDs: {pids_to_kill}")

        for process_pid in pids_to_kill:
            try:
                self.debug_message(f"Killing process with PID {process_pid}")
                psutil.Process(process_pid).terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.debug_message(f"Error killing process {process_pid}: {e}")

        self.debug_message(f"Removed terminated process with main PID {main_pid}.")
        self.debug_message(f"Remaining tracked processes: {self.chrome_processes}")

    def fetch_page(self, url):
        """
        Creates an instance of Selenium to fetch the HTML content of the specified URL, returns it
        for parsing and then kills that instance of Selenium.

        Args:
            url (str): The web address of the page to be fetched.

        Returns:
            html_content (str): The HTML of the webpage if given a valid URL, None otherwise.
        """

        driver = None
        try:
            driver, pids = self.create_selenium_driver(self.temp_evidence_folder)
            driver.get(url)
            html_content = driver.page_source
            if not html_content:
                self.debug_message(f"No HTML content fetched for URL: {url}")
                return None
            return html_content
        
        except Exception as e:
            self.debug_message(f"Exception occurred while fetching {url} using Selenium: {e}")
            return None
        
        finally:
            if driver:
                driver.quit()
                driver.service.stop()
            self.kill_chrome_process(pids)

    @retry(tries=3, delay=2, backoff=2, jitter=(1, 3))
    def download_pdf(self, url, download_folder=None, file_name=None, evidence_type=None, count=None):
        """
        Downloads a file from the given URL, saves it to a temporary folder first, converts it to PDF if necessary,
        and then moves it to the specified folder.

        Args:
            url (str): The URL to download the file from.
            download_folder (str): The folder where the file should be moved to after downloading.
            file_name (str): The desired name for the file.
            evidence_type (str): The type of evidence ('published_written_evidence' or 'witness_evidence').
            count (int): The count number for the evidence to be used in naming.

        Returns:
            final_path (str): The path to the downloaded file if successful, None otherwise.
        """

        with tempfile.TemporaryDirectory(prefix=f"temp-{count}_") as temp_dir:
            self.debug_message(f"Temporary download directory: {temp_dir}")

            if evidence_type and count is not None:
                if evidence_type == "published_written_evidence":
                    download_folder = os.path.join(self.report_name, self.published_evidence_folder)
                    file_name = f"{count:03d}.pdf"
                elif evidence_type == "witness_evidence":
                    download_folder = os.path.join(self.report_name, self.witness_evidence_folder)
                    file_name = f"0-{count}.pdf"

            if not download_folder:
                download_folder = self.temp_evidence_folder
            if not file_name:
                file_name = "downloaded_file"

            self.debug_message(f"Download URL: {url}")
            self.debug_message(f"Target Download Folder: {download_folder}")
            self.debug_message(f"File Name: {file_name}")

            os.makedirs(download_folder, exist_ok=True)

            driver = None
            temp_file_path = None

            try:
                driver, pid = self.create_selenium_driver(temp_dir)
                driver.get(url)

                self.debug_message("Waiting for download to complete...")
                download_complete = False
                max_attempts = 30
                attempts = 0

                while not download_complete and attempts < max_attempts:
                    time.sleep(1)
                    attempts += 1
                    downloaded_files = os.listdir(temp_dir)
                    self.debug_message(f"Files in temporary folder '{temp_dir}': {downloaded_files}")

                    for file in downloaded_files:
                        if file.lower().endswith(('.crdownload', '.part', '.tmp')):
                            download_complete = False
                            break
                        else:
                            download_complete = True
                            temp_file_name = file
                            temp_file_path = os.path.join(temp_dir, temp_file_name)
                            break

                if download_complete:
                    self.debug_message(f"Download complete. File downloaded to temporary path: {temp_file_path}")

                    if not temp_file_path.lower().endswith('.pdf'):

                        conversion_folder = os.path.join(self.report_name, "Files To Be Converted")
                        os.makedirs(conversion_folder, exist_ok=True)

                        if evidence_type == "published_written_evidence":
                            bracketed_name = f"{count:03d}"
                        elif evidence_type == "witness_evidence":
                            bracketed_name = f"0-{count}"
                        else:
                            bracketed_name = f"{evidence_type}-{count}"

                        base_name, original_extension = os.path.splitext(temp_file_name)
                        new_file_name = f"{base_name} ({bracketed_name}){original_extension}"
                        new_conversion_path = os.path.join(conversion_folder, new_file_name)

                        self.debug_message(f"Moving file to conversion folder with new name: {new_conversion_path}")
                        shutil.move(temp_file_path, new_conversion_path)
                        self.debug_message(f"File moved to conversion folder: {new_conversion_path}")

                        self.append_to_files_to_convert(self.report_name, new_conversion_path)
                        
                        final_path = new_conversion_path
                    else:
                        final_path = os.path.join(download_folder, file_name)
                        self.debug_message(f"Moving final file to: {final_path}")
                        shutil.move(temp_file_path, final_path)
                        self.debug_message(f"File moved to evidence folder: {final_path}")

                else:
                    self.debug_message("No file found in temporary directory after download attempt.")
                    raise Exception("Download did not complete within the expected time frame.")

            finally:
                if driver:
                    driver.quit()
                    driver.service.stop()
                    self.kill_chrome_process(pid)

            self.debug_message(f"Download completed and moved to final path: {final_path}")

            if not os.path.isfile(final_path):
                self.debug_message(f"File download failed or path is incorrect: {final_path}")
                raise Exception("Final file does not exist.")

            return final_path

    def append_to_files_to_convert(self, report_name, file_path):
        """
        Appends a file path to the self.files_to_convert dictionary under the given report name.

        Args:
            report_name (str): The name of the report.
            file_path (str): The file path to be appended.
        """

        if not hasattr(self, 'files_to_convert'):
            self.local_files_to_convert = []
        
        report_entry = next((entry for entry in self.local_files_to_convert if report_name in entry), None)

        if report_entry:
            report_entry[report_name].append(file_path)
        else:
            self.local_files_to_convert.append({report_name: [file_path]})

    def parse_page(self, html_content, is_report_page=False):
        """
        Parses the given HTML content and extracts the page title and all links.

        If `is_report_page` is True, it also attempts to find and store the report title.

        Args:
        html_content (str): The HTML content of the page to parse.
        is_report_page (bool): A flag indicating if the page is a report page. Defaults to False.

        Returns:
            dict: A dictionary containing:
                - 'title' (str): The title of the page. If no title is found, it returns 'No title'.
                - 'links' (list): A list of all hyperlinks (href) found in the HTML content.
        """

        if not html_content:
            self.debug_message("HTML content is None or empty.")
            return {'title': '', 'links': []}

        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else 'No title'
        links = [a['href'] for a in soup.find_all('a', href=True)]

        if is_report_page:
            report_title_element = soup.find('h1', id='report-title')
            if report_title_element:
                report_title = report_title_element.get_text()
                report_title = report_title.translate(str.maketrans('', '', string.punctuation))
                self.report_name = report_title
                self.debug_message(f"Report Name: {self.report_name}")
            else:
                self.debug_message("Report title element not found.")
        return {'title': title, 'links': links}
    
    def search_parse(self, data, search_string):
        return [link for link in data.get('links', []) if search_string in link]

    def extract_links(self, report_html):
        """
        Extracts different types of evidence links from the provided HTML content of a report.

        Args:
            report_html (str): The HTML content of the report.

        Returns:
            tuple: A tuple containing four lists:
                - written_evidence_links (list): Links to published written evidence.
                - witness_evidence_links (list): Links to witness evidence.
                - missing_witness_evidence_links (list): Links where witness evidence is missing.
                - missing_published_evidence_links (list): Evidence codes where published evidence link is missing.
        """        

        if not isinstance(report_html, str) or not report_html.strip():
            self.debug_message("Invalid or empty HTML input.")
            return [], [], [], []

        try:
            soup = BeautifulSoup(report_html, 'html.parser')
        except Exception as e:
            self.debug_message(f"Failed to parse HTML: {e}")
            return [], [], [], []

        published_evidence_links = []
        witness_evidence_links = []
        missing_witness_evidence_links = []
        missing_published_evidence_links = []
        seen_links = set()
        seen_dates = set()
        written_count = 0
        witness_count = 0

        self.debug_message("Extracting Published Written Evidence Links from Report.html")
        for evidence in soup.find_all('p', class_='EvidenceList1'):
            for a_tag in evidence.find_all('a'):
                try:
                    link = a_tag.get('href', '')
                    if link:
                        if '/html/' in link:
                            link = link.replace('/html/', '/pdf/')
                        if link not in seen_links:
                            written_count += 1
                            published_evidence_links.append({"link": link, "count": written_count})
                            seen_links.add(link)
                    else:
                        evidence_text = evidence.get_text(strip=True)
                        match = re.search(r'\b[A-Z]+\d+\b', evidence_text)
                        if match:
                            evidence_code = match.group(0)
                            if evidence_code not in seen_links:
                                written_count += 1
                                missing_published_evidence_links.append({"code": evidence_code, "count": written_count})
                                seen_links.add(evidence_code)
                except (TypeError, KeyError) as e:
                    self.debug_message(f"Error extracting written evidence link: {e}")

            if not evidence.find('a'):
                evidence_text = evidence.get_text(strip=True)
                match = re.search(r'\b[A-Z]+\d+\b', evidence_text)
                if match:
                    evidence_code = match.group(0)
                    if evidence_code not in seen_links:
                        missing_published_evidence_links.append({"code": evidence_code})
                        seen_links.add(evidence_code)

        self.debug_message("Extracting Witness Evidence Links from Report.html")
        date_pattern = re.compile(r'\b\d{1,2} \w+ \d{4}\b')
        for evidence in soup.find_all('p', class_='WitnessDetails'):
            try:
                a_tag = evidence.find('a')
                date_heading = evidence.find_previous('h3', class_='WitnessHeading')
                date = "Unknown Date"
                if date_heading:
                    date_text = date_heading.get_text(strip=True)
                    match = date_pattern.search(date_text)
                    if match:
                        date = match.group(0)

                if a_tag:
                    link = a_tag.get('href', '')
                    if link:
                        if '/html/' in link:
                            link = link.replace('/html/', '/pdf/')
                        if link not in seen_links:
                            witness_count += 1
                            witness_evidence_links.append({"link": link, "count": witness_count})
                            seen_links.add(link)
                            seen_dates.add(date)
                    else:
                        if date not in seen_dates:
                            witness_count += 1
                            missing_witness_evidence_links.append({"date": date, "count": witness_count})
                            seen_dates.add(date)
                else:
                    if date not in seen_dates:
                        witness_count += 1
                        missing_witness_evidence_links.append({"date": date, "count": witness_count})
                        seen_dates.add(date)
            except (TypeError, KeyError) as e:
                self.debug_message(f"Error extracting oral evidence link: {e}")

        return witness_evidence_links, published_evidence_links, missing_witness_evidence_links, missing_published_evidence_links

    def search_witness_evidence_page(self, witness_html, date):
        """
        Searches for a witness evidence link in the given HTML content based on the specified date.

        Args:
            witness_html (str): The HTML content of the witness evidence page.
            date (str): The date to search for within the HTML content.

        Returns:
            a_tag['href'] (str): The URL of the PDF link if found, otherwise None.
        """

        try:
            soup = BeautifulSoup(witness_html, 'html.parser')
            primary_info_divs = soup.find_all('div', class_='primary-info')
            for primary_info_div in primary_info_divs:
                if date in primary_info_div.get_text(strip=True):
                    card_div = primary_info_div.find_parent('div', class_='card')
                    if card_div:
                        a_tag = card_div.find('a', class_='dropdown-item', href=True)
                        if a_tag and '/pdf/' in a_tag['href']:
                            return a_tag['href']
            return None
        
        except Exception as e:
            self.debug_message(f"Error searching for witness evidence link: {e}")
            return None

    def process_missing_witness_evidence(self, report_html_parsed, missing_witness_evidence_links):
        """
        Processes missing witness evidence by searching for and downloading the missing PDFs.

        Args:
            report_html_parsed (str): The parsed HTML content of the report.
            missing_witness_evidence_links (list): A list of dictionaries containing 'date' and 'count' for missing witness evidence.
            missing_pdfs (list): A list to append the paths of downloaded missing PDFs.
        """

        witness_evidence_dict = []

        self.witness_evidence_page = self.search_parse(report_html_parsed, "/oral-evidence/")
        base_url = "https://committees.parliament.uk"
        self.debug_message(self.witness_evidence_page)

        witness_html = self.fetch_page(self.witness_evidence_page[0])

        if not witness_html:
            self.debug_message("Failed to fetch the initial page")
            return witness_evidence_dict

        page_urls = self.get_page_numbers(witness_html)
        
        all_pages_html = witness_html

        for page_url in page_urls:
            full_url = f"{base_url}{page_url}"
            page_html = self.fetch_page(full_url)
            if page_html:
                all_pages_html += page_html
            else:
                self.debug_message(f"Failed to fetch page: {full_url}")

        for missing_link in missing_witness_evidence_links:
            date = missing_link['date']
            count = missing_link['count']
            found_link = self.search_witness_evidence_page(all_pages_html, date)

            if found_link:
                missing_witness_link = base_url + found_link
                witness_evidence_dict.append({"link": missing_witness_link, "count": count})

        return witness_evidence_dict
    
    def search_published_evidence_page(self, html, evidence_code):
        soup = BeautifulSoup(html, 'html.parser')
        results_sections = soup.find_all('div', {'id': 'results'})
        
        for results_section in results_sections:
            cards = results_section.find_all('div', class_='card-publication')
            
            for card in cards:
                evidence_label = card.find('span', class_='label internal-ref')
                if evidence_label and evidence_code in evidence_label.text:
                    pdf_link = None
                    html_link = None
                    default_link = None
                    dropdown_items = card.find_all('a', class_='dropdown-item')
                    for item in dropdown_items:
                        if 'Open PDF' in item.text:
                            pdf_link = item.get('href')
                        elif 'Open HTML' in item.text:
                            html_link = item.get('href')
                        elif 'default' in item.get('href'):
                            default_link = item.get('href')
                    if pdf_link:
                        return pdf_link
                    elif default_link:
                        return default_link
        return None

    def get_page_numbers(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        page_links = soup.select('ul.pagination a[href*="?page="]')
        page_urls = []
        for a in page_links:
            href = a['href']
            if href not in page_urls:
                page_urls.append(href)
        return page_urls

    def process_missing_published_evidence(self, report_html_parsed, missing_published_evidence_links):
        """
        Processes missing published evidence by searching for and downloading the missing PDFs.

        Args:
            report_html_parsed (str): The parsed HTML content of the report.
            missing_published_evidence_links (list): A list of dictionaries containing 'code' and 'count' for missing published evidence.

        Returns:
            list: A list of dictionaries with 'link' and 'count' for found evidence PDFs.
        """

        published_evidence_dict = []

        self.published_evidence_page = self.search_parse(report_html_parsed, "/written-evidence/")
        base_url = "https://committees.parliament.uk"
        self.debug_message(self.published_evidence_page)

        published_html = self.fetch_page(self.published_evidence_page[0])

        if not published_html:
            self.debug_message("Failed to fetch the initial page")
            return published_evidence_dict

        page_urls = self.get_page_numbers(published_html)
        
        all_pages_html = published_html

        for page_url in page_urls:
            full_url = f"{base_url}{page_url}"
            page_html = self.fetch_page(full_url)
            if page_html:
                all_pages_html += page_html
            else:
                self.debug_message(f"Failed to fetch page: {full_url}")

        for missing_link in missing_published_evidence_links:
            code = missing_link['code']
            count = missing_link['count']
            found_link = self.search_published_evidence_page(all_pages_html, code)
            self.debug_message(f"{found_link}, {code}")
            if found_link:
                missing_published_link = base_url + found_link
                published_evidence_dict.append({'link': missing_published_link, 'count': count})

        return published_evidence_dict

    def crawl(self):
        print(self.current_dir)

        """
        Crawls the given initial link to fetch, parse, and process reports and related evidence documents.
        """
        initial_link = self.initial_link

        self.console_message(""); self.console_message("-- Running Selenium Crawler --")
        self.debug_message(f"Crawling: {initial_link}\n")
        self.console_message(""); self.console_message(f"Crawling: {initial_link}\n")

        downloaded_reports_path = os.path.join(self.current_dir, 'data/downloaded_reports.json')
        if os.path.exists(downloaded_reports_path):
            with open(downloaded_reports_path, 'r') as f:
                downloaded_reports = json.load(f)
        else:
            downloaded_reports = {}

        try:
            fetched_initial_link = self.fetch_page(initial_link)
            if fetched_initial_link is None:
                raise Exception("Failed to fetch the initial link.")
        except Exception as e:
            self.debug_message(f"Exception fetching initial link: {str(e)}")
            return

        parsed_initial_link = self.parse_page(fetched_initial_link)
        report_pdf_link = self.search_parse(parsed_initial_link, "summary.html")
        report_links = self.search_parse(parsed_initial_link, "report.html")

        valid_links = [link.replace('summary.html', 'report.html') for link in report_pdf_link] + report_links

        self.console_message(f"Found {len(valid_links)} suitable report(s)")

        self.debug_message("Valid links (report.html):")
        for link in valid_links:
            self.debug_message(link)
        self.debug_message("")

        published_pdfs = []
        written_pdfs = []
        missing_witness_pdfs = []
        missing_published_pdfs = []

        for index, link in enumerate(valid_links, start=1):
            self.console_message(f"Searching report {index}")
            self.debug_message(f"Current link: {link}")

            self.local_files_to_convert = []

            if link in downloaded_reports.keys():
                self.console_message(""); self.console_message(f"Link '{link}' already processed. Skipping link."); self.console_message("")
                self.debug_message(f"Skipping already processed link: {link}")
                continue

            try:
                report_html = self.fetch_page(link)
                if report_html is None:
                    raise Exception(f"Failed to fetch the report page for link: {link}")

                report_html_parsed = self.parse_page(report_html, is_report_page=True)

                self.console_message("")
                report_name_length = len(self.report_name)
                max_length = 90
                hyphen_length = (max_length - report_name_length - 2) // 2
                hyphens = '-' * hyphen_length
                console_msg = f"{hyphens} {self.report_name} {hyphens}"

                if len(console_msg) < max_length:
                    console_msg += '-' * (max_length - len(console_msg))

                self.console_message(console_msg); self.console_message("")

                os.makedirs(self.report_name, exist_ok=True)
                os.makedirs(f"{self.report_name}/{self.witness_evidence_folder}", exist_ok=True)
                os.makedirs(f"{self.report_name}/{self.published_evidence_folder}", exist_ok=True)

                self.console_message("    ----- Finding and Downloading PDFs -----"); self.console_message("")
                self.console_message(f"    Created '{self.report_name}',")
                self.console_message(f"    '{self.witness_evidence_folder}' and '{self.published_evidence_folder}' folders.")

                try:
                    report_pdf_links = self.search_parse(report_html_parsed, "/default/")
                    if not report_pdf_links:
                        raise Exception(f"No '/default/' links found in the report page for link: {link}")

                    report_pdf_link = report_pdf_links[0]
                    self.debug_message(f"Found link containing '/default/' in {link}")
                    full_link = urljoin(link, report_pdf_link)
                    self.debug_message(full_link); self.debug_message("")

                    pdf_path = self.download_pdf(full_link, download_folder=self.report_name, file_name="report.pdf")
                    if pdf_path is None:
                        raise Exception("Failed to download PDF.")

                    self.debug_message("PDF downloaded successfully."); self.console_message("")
                    self.console_message(f"    Downloaded 'report.pdf' at '{pdf_path}'")

                    witness_evidence_links, published_evidence_links, missing_witness_evidence_links, missing_published_evidence_links = self.extract_links(report_html)

                    if not (witness_evidence_links or published_evidence_links or missing_witness_evidence_links or missing_published_evidence_links):
                        shutil.rmtree(self.report_name, ignore_errors=True)
                        self.debug_message(f"No evidence found for report at {link}. Deleting folder and returning.")
                        continue

                    self.console_message(""); self.console_message("    Found:")
                    self.console_message(f"    {len(witness_evidence_links)} - Witness Evidence")
                    self.console_message(f"    {len(published_evidence_links)} - Published Written Evidence")
                    self.console_message(f"    {len(missing_witness_evidence_links)} - Missing Witness Evidence")
                    self.console_message(f"    {len(missing_published_evidence_links)} - Missing Published Evidence"); self.console_message("")

                    if witness_evidence_links:
                        self.console_message(f"    Downloading {len(witness_evidence_links)} Witness Evidence")
                        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                            futures = [
                                executor.submit(
                                    self.download_pdf, 
                                    item['link'], 
                                    evidence_type="witness_evidence", 
                                    count=item['count']
                                )
                                for item in witness_evidence_links
                            ]

                            for future in concurrent.futures.as_completed(futures):
                                pdf_path = future.result()
                                if pdf_path:
                                    written_pdfs.append(pdf_path)
                                else:
                                    self.debug_message("Failed to download a Witness Evidence PDF")

                        self.console_message(f"    Downloaded {len(witness_evidence_links)} Witness Evidence"); self.console_message("")


                    if published_evidence_links:
                        self.console_message(f"    Downloading {len(published_evidence_links)} Published Written Evidence")
                        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                            futures = [
                                executor.submit(
                                    self.download_pdf, 
                                    item['link'], 
                                    evidence_type="published_written_evidence", 
                                    count=item['count']
                                )
                                for item in published_evidence_links
                            ]

                            for future in concurrent.futures.as_completed(futures):
                                pdf_path = future.result()
                                if pdf_path:
                                    published_pdfs.append(pdf_path)
                                else:
                                    self.debug_message("Failed to download a Published Written Evidence PDF")

                        self.console_message(f"    Downloaded {len(published_evidence_links)} Published Written Evidence"); self.console_message("")

                    if missing_witness_evidence_links:
                        self.console_message(f"    Finding and Downloading {len(missing_witness_evidence_links)} Missing Witness Evidence")
                        missing_witness_evidence = self.process_missing_witness_evidence(report_html_parsed, missing_witness_evidence_links)
                        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                            futures = [
                                executor.submit(
                                    self.download_pdf, 
                                    item['link'], 
                                    evidence_type="witness_evidence", 
                                    count=item['count']
                                )
                                for item in missing_witness_evidence
                            ]
                    
                            for future in concurrent.futures.as_completed(futures):
                                pdf_path = future.result()
                                if pdf_path:
                                    missing_witness_pdfs.append(pdf_path)
                                else:
                                    self.debug_message("Failed to download a Published Written Evidence PDF")

                            self.console_message(f"    Downloaded {len(witness_evidence_links)} Missing Witness Evidence"); self.console_message("")

                    if missing_published_evidence_links:
                        self.console_message(f"    Finding and Downloading {len(missing_published_evidence_links)} Missing Published Written Evidence")
                        missing_published_evidence = self.process_missing_published_evidence(report_html_parsed, missing_published_evidence_links)
                        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                            futures = [
                                executor.submit(
                                    self.download_pdf, 
                                    item['link'], 
                                    evidence_type="published_written_evidence",
                                    count=item['count']
                                )
                                for item in missing_published_evidence
                            ]
                    
                            for future in concurrent.futures.as_completed(futures):
                                pdf_path = future.result()
                                if pdf_path:
                                    missing_published_pdfs.append(pdf_path)
                                else:
                                    self.debug_message("Failed to download a Published Written Evidence PDF")

                        self.console_message(f"    Downloaded {len(missing_published_evidence_links)} Missing Published Written Evidence"); self.console_message("")

                    report_pdf = f"{self.report_name}/report.pdf"
                    
                    downloaded_reports[link] = self.report_name
                    with open(downloaded_reports_path, 'w') as f:
                        json.dump(downloaded_reports, f, indent=4)

                    if self.local_files_to_convert:
                        self.files_to_convert.extend(self.local_files_to_convert)

                    if len(self.local_files_to_convert) == 0:
                        processor = ReportGenerator(
                            report_pdf, 
                            f"{self.report_name}/{self.published_evidence_folder}", 
                            f"{self.report_name}/{self.witness_evidence_folder}", 
                            self.console_text
                        )
                        processor.create_report()
                    else:
                        self.console_message(f"    There were files that needed converting... Aborted report generation."); self.console_message("")

                except Exception as e:
                    self.debug_message(f"Exception in extracting and downloading evidence from report: {e}")

            except Exception as e:
                self.debug_message(f"Failed to process report link: {link}")
                self.debug_message(str(e))

        self.console_message("Code Successfully Executed!"); self.console_message("")
        for item in self.files_to_convert:
            for report_name, links in item.items():
                self.console_message(f"The following report: '{report_name}'. Downloaded the following files but they were not PDFs"); self.console_message("")
                for link in links:
                    self.console_message(f"'{link}'")
            self.console_message(""); self.console_message("Please manually convert these to PDF, rename them after the name provided in the brackets of the file name, and then move them to their specific witness or published written evidence folder."); self.console_message("")