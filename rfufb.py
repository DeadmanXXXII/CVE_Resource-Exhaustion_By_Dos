import requests

# Define your list of URLs
post_urls = [
    "https://www.facebook.com/864455789052895/posts/873939801446986",
    "https://www.facebook.com/864455789052895/posts/315592389183630",
    "https://www.facebook.com/265591767945727",
    "https://www.facebook.com/864455789052895/posts/613227426369606",
    "https://www.facebook.com/344000970619547",
    "https://www.facebook.com/864455789052895/posts/206127476497249",
    "https://www.facebook.com/708528740902572",
    "https://www.facebook.com/681699459556345",
    "https://www.facebook.com/076185106885704",
    "https://www.facebook.com/490057925221740",
    "https://www.facebook.com/468365502953642",
    "https://www.facebook.com/713101438277691",
    "https://www.facebook.com/864455789052895/posts/530644607747663",
    "https://www.facebook.com/864455789052895/posts/371021353772777",
    "https://www.facebook.com/657485721534045",
    "https://www.facebook.com/864455789052895/posts/583761788504853",
    "https://www.facebook.com/864455789052895/posts/139830859256098",
    "https://www.facebook.com/864455789052895/posts/444180979100096",
    "https://www.facebook.com/864455789052895/posts/720756894979782",
    "https://www.facebook.com/864455789052895/posts/070175605624798",
    "https://www.facebook.com/864455789052895/posts/628056698113279",
    "https://www.facebook.com/864455789052895/posts/180687491821298"
]

put_urls = [
    "https://www.facebook.com/864455789052895/posts/012040285637335",
    "https://www.facebook.com/864455789052895/posts/203812655972948",
    "https://www.facebook.com/864455789052895/posts/526377864893232",
    "https://www.facebook.com/864455789052895/posts/371021353772777",
    "https://www.facebook.com/140335557780651",
    "https://www.facebook.com/657485721534045",
    "https://www.facebook.com/864455789052895/posts/583761788504853",
    "https://www.facebook.com/864455789052895/posts/520546885054471",
    "https://www.facebook.com/514074107316928",
    "https://www.facebook.com/864455789052895/posts/906034991337830",
    "https://www.facebook.com/423080392064897",
    "https://www.facebook.com/854290872124814",
    "https://www.facebook.com/006248768145606",
    "https://www.facebook.com/011286980656315",
    "https://www.facebook.com/146993536352768",
    "https://www.facebook.com/656679546107214"
]

# Function to upload a file via POST or PUT
def upload_file(file_path, post_message, endpoint_url, method='POST'):
    with open(file_path, 'rb') as file:
        payload = {'message': post_message}
        files = {'file': (file_path, file, 'application/octet-stream')}
        try:
            if method == 'POST':
                response = requests.post(endpoint_url, data=payload, files=files)
            else:
                response = requests.put(endpoint_url, data=payload, files=files)

            # Log the result
            if response.status_code == 200:
                print(f"Successfully uploaded to {endpoint_url} with {method}")
                print(f"Response content: {response.content.decode()}")  # Check the actual response
            else:
                print(f"Failed to upload to {endpoint_url} with {method}. Status Code: {response.status_code}")
                print(f"Response content: {response.content.decode()}")
        except requests.RequestException as e:
            print(f"Error uploading to {endpoint_url} - {e}")

# Main script to loop through all URLs
file_path = '/root/meta/sd.py'  # Replace with the actual path to your .py file
post_message = "Uploading a .py file"

# Loop through POST URLs and attempt to upload the file
for url in post_urls:
    upload_file(file_path, post_message, url, method='POST')

# Loop through PUT URLs and attempt to upload the file
for url in put_urls:
    upload_file(file_path, post_message, url, method='PUT')
