from bs4 import BeautifulSoup
import requests 
from time import time

# links = [ "https://github.com/TonikX/ITMO_ICT_WebDevelopment_tools_2023-2024/"  ]

urls = [
    "https://www.example.com",
    "https://www.wikipedia.org",
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.github.com",
    "https://www.stackoverflow.com",
    "https://www.medium.com",
    "https://www.quora.com",
    "https://www.bbc.com",
    "https://www.nytimes.com",
    "https://www.cnn.com",
    "https://www.reddit.com",
    "https://www.apple.com",
    "https://www.dropbox.com",
    "https://www.paypal.com",
    "https://www.ebay.com",
    "https://www.netflix.com",
    "https://www.spotify.com",
    "https://www.airbnb.com",
    "https://www.booking.com",
    "https://www.tumblr.com",
    "https://www.pinterest.com",
    "https://www.yelp.com",
    "https://www.zillow.com",
    "https://www.tripadvisor.com",
    "https://www.walmart.com",
    "https://www.target.com",
]


def parse_and_save(url :str):
  r = requests.get(url)
  html = BeautifulSoup(r.text, features="html.parser")
  title = html.title.string 
  if title:
    print(title)


# start_time = time()
# for url in urls:
#   parse_and_save(url)

# print(time() - start_time )

print(len(urls))