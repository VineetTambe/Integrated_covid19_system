import pyrebase
from datetime import datetime

config = {
    # Add your firebase project config
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

def firebase_upload(img):
    # This function will upload the passed image to the dir of the current date
	today = datetime.now()
	path_cloud = str(today.date())+"/"+str(today.strftime('%Y-%m-%d %H:%M:%S'))+" "+str(img)
	storage.child(path_cloud).put(img)

def get_images_urls(date_str):
    # This function will return urls of images from the passed date 
    urls = []
    all_files = storage.list_files()
    for file in all_files:
        try:
            link = storage.child(file.name).get_url(None)
            if date_str in link:
                urls.append(link)
        except:
            print('Download Failed')
    return urls

image = "" # local path of image  
firebase_upload(image)
date = "" # date in 'YYYY-MM-DD' format
url_list = get_images_urls(date)
for url in url_list:
    print(url)