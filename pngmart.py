import requests
from bs4 import BeautifulSoup

# Define the URL of the sitemap
site_map = 'https://www.pngmart.com/sitemap.xml'

# Get the sitemap XML content
response = requests.get(site_map)
xml = response.text

# Parse the XML content using BeautifulSoup
soup = BeautifulSoup(xml, 'xml')

# Extract all URLs from the sitemap that contain 'posts'
site_maps = []
for loc in soup.find_all('loc'):
    if 'posts' in loc.text:
        site_maps.append(loc.text)

# Get the content of the site map URL
for site_map in site_maps[0]:              # Parse the first site map to prevent overloading the computer's memory
                                           # You can modify the range to include more or fewer site maps, depending on your memory and processing requirements.        
    response = requests.get(site_map)
    soup = BeautifulSoup(response.text, 'xml')

    # Create a master list to store all the URLs from the site map
    master_list = []
    for loc in soup.find_all('loc'):
        master_list.append(loc.text)

    # Loop through the master list, fetching PNG images and saving them locally
    for image_url in master_list[0:20:2]:  # Parse the first 10 image URLs to prevent overloading the computer's memory
                                           # The step size of '2' ensures that we skip every other URL, effectively processing every other image in the subset. 
                                           # You can modify the range to include more or fewer URLs, depending on your memory and processing requirements.
        response = requests.get(image_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if the response status code is 200 (successful)
        if response.status_code == 200:
            try:
                # Find the URL of the PNG image to download
                png_url = soup.find('a', {'class':'download'})['href']
                
                # Fetch the PNG image
                image = requests.get(png_url)
                
                # Create a unique filename for the downloaded image
                image_title = image_url.split('/')[-1] + '-' + png_url.split('/')[-1]
                
                # Save the image locally in binary mode
                with open(image_title, 'wb') as file: 
                    file.write(image.content)
                
                # Print the filename for reference
                print(image_title)
            except:
                # If any error occurs (e.g., missing 'download' class), skip to the next image URL
                continue
