import requests
from bs4 import BeautifulSoup

def handel_cookies( ):
    url= "https://asolgiza.blogspot.com/2024/01/blog-post.html"
    # Send a GET request to the blog post URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the blog post content
        post_content = soup.find('div', class_='post-body')  # Adjust the class based on the structure of the blog post

        # Check if the content is empty
        if post_content and post_content.get_text(strip=True):  # Check if content is not empty
            return post_content.get_text().strip()  # Use strip() to remove leading and trailing spaces
        else:
            return None  # Return None if content is empty

    else:
        return None  # Return None if the request was unsuccessful

