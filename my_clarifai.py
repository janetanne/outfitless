import os
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

c_app = ClarifaiApp()

model = c_app.models.get('apparel')
image = ClImage(file_obj=open('./test_images/Snapseed.jpg', 'rb'))
test_image_info = model.predict([image])

print(test_image_info)