import json
import urllib2
import urllib
import os

if __name__ == '__main__':
    directory = ""
    image_dir = os.path.expandvars("$GIMP_PROJECT/images")
    downloaded_files = 0
    iterations = 0
    categories = ["", "fashion", "nature", "backgrounds", "science", "education", "people",
                  "feelings", "religion", "health", "places", "animals", "industry", "food",
                  "computer", "sports", "transportation", "travel", "buildings", "business",
                  "music"]
    while downloaded_files < 10000:
        for page in range(1, 26):
            print "iteration:", iterations, "page:", page
            url = "https://pixabay.com/api/?key=7434716-4bb57af4b0adeb8e15fe1ef80&page={}&safesearch=true&q={}".format(page, categories[iterations])
            data = json.load(urllib2.urlopen(url))
            for hit in data["hits"]:
                image_url = hit["webformatURL"]
                file_format = str(image_url).split(".")[-1:][0]
                urllib.urlretrieve(image_url, "{}/{}.{}".format(image_dir, hit["id"], file_format))
        downloaded_files = len([name for name in os.listdir(image_dir)])
        print downloaded_files
        iterations += 1

