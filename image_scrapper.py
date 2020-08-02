from selenium import webdriver
import time
from PIL import Image
import io
import hashlib
import requests
import os

options = webdriver.ChromeOptions()
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe' #For Example only. Use your Browser path.
path = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\chromedriver.exe' #For Example only. Use your Driver path.
#driver = webdriver.Chrome(executable_path=path,options=options)
#options.add_argument('--headless') #Remove the comment if you don't want to open the browser that's running in test mode.

def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):

    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    #....................................Build the Search Query.............................................
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img".format(q=query)
    wd.get(search_url)

    thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
    #wd.execute_script("console.log(document.getElementsByTagName('img').length)")

    #Click the more images button till the page has the required number of images
    while len(thumbnail_results)<max_links_to_fetch:
        load_more_button = wd.find_element_by_css_selector(".mye4qd")
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        if load_more_button :
            wd.execute_script("document.querySelector('.mye4qd').click();")
            time.sleep(sleep_between_interactions)
            #driver.execute_script("console.log(document.getElementsByTagName('img').length)")
            #print(f"Length of thumbnail images are : {len(thumbnail_results)}")
        else:
            #print(f"Maximum possible images are : {len(thumbnail_results)}....")
            print(f"Adjusting Number of Images from {max_links_to_fetch} to {len(thumbnail_results)}")
            max_links_to_fetch=len(thumbnail_results)
            break
    else:
        print(f"Webpage available for downloading {max_links_to_fetch}")
    
    image_urls = set()

    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)

        for img in thumbnail_results[0:min(max_links_to_fetch,number_results)]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
            #print(f" {len(image_urls)} Images added to set ")
            
            #Remove the images if the fetched images > images required
            if len(image_urls)>max_links_to_fetch:
                for rem in range(len(inage_urls)-max_links_to_fetch):
                    image_urls.discard(image_urls[len(image_urls)-rem])
                return image_urls

#Download the image from the URLs
def persist_image(folder_path: str, url: str):

    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, hashlib.sha1(
            image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

#Wrapper function for downloading the images
def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=5):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path, options=options) as wd:
        res = fetch_image_urls(search_term, number_images,wd=wd, sleep_between_interactions=0.5)
        #print("Image URLs fetched successfully!")
    for elem in res:
        persist_image(target_folder, elem)

if __name__=='__main__':
    
    search_queries = ['Person of Interest'] # Mention your queries as a list of queries
    #number_of_images=100
    number_of_images=int(input("Enter the number of images to be downloaded"))

    if not os.path.exists('./ScrapedImages'):
        os.mkdir('./ScrapedImages')
    
    #number_of_images=int(input("Enter the number of Images Required: "))
    for query in search_queries:
        search_and_download(query, driver_path=path,target_path=f'./ScrapedImages/{query}', number_images=number_of_images)
