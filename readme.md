# Outfitless 👕👗👖👚

[Outfitless](https://www.outfitless.com) helps users organize their closet, choose outfits, and keep track of their clothes. Most notably, it keeps track of the cost per use for each piece of clothing.

Inspired by the trend towards zero waste, capsule wardrobes, and Mari Kondo of “The Life-Changing Magic of Tidying Up”, Outfitless hopes that its users will learn to do more with less.

## Table of Contents 📑
* [Tech Stack](#tech-stack)
* [Features](#features)
* [Setup/Installation](#installation)
* [Future Features](#future)
* [About the Developer](#about)
* [License](#license)

## <a name="tech-stack"></a>Tech Stack 💻

__Frontend:__ HTML5, CSS, Javascript, jQuery, Bootstrap
<br>
__Backend:__ Python, SQL, Flask, PostgresQL, SQLAlchemy
<br>
__APIs:__ Google OAuth 2.0, Clarifai

Deployed via Amazon Web Services LightSail

## <a name="Features"></a>Features ✨

See the app in action here:<br>
[![Outfitless demo](http://img.youtube.com/vi/mC_pL3Wx85U/0.jpg)](http://www.youtube.com/watch?v=mC_pL3Wx85U)

Register & log in via Google.<br><br>
![Login](https://github.com/janetanne/outfitless/blob/master/static/images/_readme-images/login.png)

Upload multiple files at once.<br><br>
![Upload](https://github.com/janetanne/outfitless/blob/master/static/images/_readme-images/upload.png)

Verify suggested piece details, or write in your own description.<br><br>
![Verify](https://github.com/janetanne/outfitless/blob/master/static/images/_readme-images/verifydetails.png)
![Verify2](https://github.com/janetanne/outfitless/blob/master/static/images/_readme-images/verifydetails2.png)

Choose an outfit with OOTD feature!<br><br>
![OOTD](https://github.com/janetanne/outfitless/blob/master/static/images/_readme-images/ootd.png)

Check out all pieces uploaded to closet, and their details.<br><br>
![Closet](https://github.com/janetanne/outfitless/blob/master/static/images/_readme-images/closet.png)

*Please note that although the site is live, these features will only work if you install the app locally. Everything past log-in has been disabled from the site.*

## <a name="installation"></a>Setup/installation 🛠

#### Requirements:
- Python 3+
- PostgresQL
- Google OAuth 2.0 keys 🔑
- Clarifai API keys 🔑

To run this app on your local computer, please follow the below steps:

Clone repository.
```
$ git clone https://github.com/janetanne/outfitless.git
```
Create and activate a virtual environment.
```
$ virtualenv env
$ source env/bin/activate
```

Install the dependencies:
```
$ pip install -r requirements.txt
```

Sign up to use the [Google OAuth API](https://developers.google.com/identity/protocols/OAuth2) and [Clarifai API](https://clarifai.com/developer). Obtain your secret keys 🔑, then save them to <kbd>secrets.sh</kbd>. The file should look like this:
```
export APP_SECRET_KEY="insert"
export CLARIFAI_API_KEY="keys"


export GOOGLE_CLIENT_ID="andotherstuff"
export GOOGLE_PROJECT_ID="here"
export GOOGLE_AUTH_URI="https://accounts.google.com/o/oauth2/auth"
export GOOGLE_TOKEN_URI="https://www.googleapis.com/oauth2/v3/token"
export GOOGLE_AUTH_PROVIDER="https://www.googleapis.com/oauth2/v1/certs"
export GOOGLE_CLIENT_SECRET="linksaboveshouldworkthough"
```

Source your keys from <kbd>secrets.sh</kbd> into your virtual environment.
```
$ source secrets.sh
```

Set up your database.
```
$ createdb outfitless
$ python model.py
```

Run the app from the command line.
```
$ python server.py
```

Navigate to 'localhost:5000/' to access Outfitless.

## <a name="future"></a>Future Features 🔮
- Data visualization of user's closets
- Reminders to wear, donate, or sell clothes not worn in a certain period of time
- Upload photos to Google Photos

## <a name="about"></a>About the Developer 👩🏻‍💻
This was created by Janet Anne Panen for her final project at [Hackbright Academy](https://www.hackbrightacademy.com), an engineering school for women.

She's located in San Francisco, and you can contact her via [Twitter](https://www.twitter.com/janetanne), [LinkedIn](https://www.linkedin.com/in/janetanne), or email 📧 janetpanen at gmail dot com.

This project was inspired by the annoyance of choosing what to wear every day, and the 90s classic film, *Clueless* (hence the name Outfitless 😉).

## <a name="license"></a>License 📝
The MIT License (MIT)
Copyright (c) 2016 Agne Klimaite

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
