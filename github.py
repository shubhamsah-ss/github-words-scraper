# pip -m install selenium
# pip webdriver_manager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def process_repository(repoUrl, choice):
    profileUrl = repoUrl.split("?")[0] if choice == 2 else  repoUrl
    
    driver.get(repoUrl)
    time.sleep(2)
    
    res1 = driver.find_elements(By.CLASS_NAME, "repo") if choice == 1 else driver.find_elements(By.XPATH, "//a[@itemprop='name codeRepository']")
    
    links = [i.text for i in res1]
    
    for repo in links:
        print(f"Current repository: {repo}")
        next_page = f"{profileUrl}/{repo}"
        repository_page(next_page)
        print("\n")



def repository_page(pageUrl):
    stack = [(pageUrl, 0)]
    
    while stack:
        current_url, tab = stack.pop()
        
        driver.get(current_url)
        time.sleep(2)
        branch = driver.find_element(By.CLASS_NAME, "Text-sc-17v1xeu-0").text.strip()
        res2 = driver.find_elements(By.CLASS_NAME, "Link--primary")
        
        for a in res2:
            title_ = a.get_attribute("title")
            if title_ and title_.strip() == a.text.strip():
                aria_label = a.get_attribute("aria-label")
                if aria_label and aria_label.strip().split()[1] != "(Directory)":
                    file_extension = "." + a.text.split(".")[-1]
                    if file_extension not in non_raw_extensions:
                        if "tree" not in current_url:
                            second_page = f"{current_url}/blob/{branch}/{a.text}"
                        else:
                            path = current_url.replace("tree","blob")
                            second_page = f"{path}/{a.text}"
                        try:
                            driver.execute_script("window.open();")
                            driver._switch_to.window(driver.window_handles[-1])
                            raw_file(second_page)
                        except Exception as e: 
                            print(f"Error in {current_url}: {e}")
                        finally: 
                            driver.close()
                            driver._switch_to.window(driver.window_handles[tab])
                else:
                    if "tree" not in current_url:
                        new_url = f"{current_url}/tree/{branch}/{a.text}"
                    else:
                        new_url = f"{current_url}/{a.text}"
                    stack.append((new_url, tab))






def raw_file(file_url):
    global fileScan
    
    driver.get(file_url)
    time.sleep(2)

    raw = driver.find_element(By.XPATH, "//a[@data-testid='raw-button']")
    raw.click()

    time.sleep(5)

    html = f"{driver.page_source}"

    fileScan += 1

    for keyword in keywords:
        if keyword in html:
            print(f"Found {keyword} in {file_url}")






repoUrl = input("Target user github profile url: ")
choice = int(input("Select any one:\n1. Popular repositories\n2. All repositories\nEnter choice: "))
repo_profile_url = ""

if choice == 1:
    repo_profile_url = repoUrl
elif choice == 2:
    repo_profile_url = f"{repoUrl}?tab=repositories"

if choice != 1 and choice != 2:
    print("Invalid input.")
else:    
    keywords = input("Enter keywords to search (separated by comma(,)): ").strip().split(",")
    non_raw_extensions = [".png", ".jpg", ".jpeg", ".pdf", ".gif", ".mp4", ".avi", ".mkv", ".mp3", ".wav"]



    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)


    fileScan = 0

    process_repository(repo_profile_url, choice)

    driver.quit()
    print(f"\nTotal files scanned: {fileScan}")