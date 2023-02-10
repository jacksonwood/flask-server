import requests
from io import BytesIO
from PIL import Image

# Download the two images from the URLs
url1 = 'https://gateway.pinata.cloud/ipfs/Qmc3z8LknwWpYJdakPsmuHZ6zZtCXowkqJmHbFFzxTyvKV'
url2 = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-bXP14wni5DJxa1XtsOFCcYzu/user-go3LXjqgDQmRsWT8H6hQRNqt/img-h1eSvwZv5ZwzDBwDwGHSPHBM.png?st=2023-02-10T13%3A21%3A51Z&se=2023-02-10T15%3A21%3A51Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-02-09T21%3A37%3A15Z&ske=2023-02-10T21%3A37%3A15Z&sks=b&skv=2021-08-06&sig=9WOanZ8OLdOQSxQzS24MqT6LUExTMKC8%2BvFO5fZuMgc%3D'
response1 = requests.get(url1)
response2 = requests.get(url2)

# Open the two images using PIL
img1 = Image.open(BytesIO(response1.content))
img2 = Image.open(BytesIO(response2.content))


# Scale up the second image
scale_factor = 1.55
img2 = img2.resize((int(img2.width * scale_factor), int(img2.height * scale_factor)), Image.ANTIALIAS)
# Paste image2 onto image1 at position (0, 0)
img1.paste(img2, (225, 140))

# Convert the image to RGB mode
img1 = img1.convert("RGB")

# Save the result as a JPEG file
img1.save('result.jpg', 'JPEG')

print(img1)

from flask import Flask, Response

app = Flask(__name__)

@app.route('/image')
def image():
    with open('result.jpg', 'rb') as f:
        image_data = f.read()
    return Response(image_data, content_type='image/jpeg')

if __name__ == '__main__':
    app.run()