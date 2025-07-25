from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

''' The Below Block is for Testing Purpose

def scrape_website(website):
    print("Launching Browser ....")

    driver_path = "./geckodriver"
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=Service(driver_path),options=options)

    # driver_path = "./chromedriver"  # Remove Comment If Using Chrome 
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Chrome(service=Service(driver_path),options=options)  

    try:
        driver.get(website)
        print("Loading Site")
        html = driver.page_source
        time.sleep(10)

        return html
    finally:
        driver.quit()

'''


def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content



def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]