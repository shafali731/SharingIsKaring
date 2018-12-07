# SharingIsKaring
## Shafali Gupta, Karen Li, Jabir Chowdhury

## SharingIsKaring?
SharingIsKaring is a website where you can find information on any movie or book you would like, and then get a series of recommendations
based on what you searched.


## How do you run this?
### First you need to activate your virtual environment
Go to the folder containing your virtual environment.

Linux and Mac:
```
$source my_folder/bin/activate
```
Windows:
```
> \path\to\env\Scripts\activate
```
### Clone the repository
```
git clone https://github.com/shafali731/SharingIsKaring.git
```

### Install packages
```
(venv)$pip install -r <path-to-file>requirements.txt
```
### Run app.py from within the repository
```
python3 app.py
```
### Check out our website
Go to localhost:5000 on the web browser of your choice

## Close
Deactivate your virtual environment
```
deactivate
```

## Dependencies
To run our program, you need to have python3 or higher installed.

### packages required:

- urllib

`urllib` is used to get the JSON files from each of the APIs. It is a standard Python library and you do not need to install anything extra for this functionality.

- pip

`pip` is used to install other modules like `flask` and `virtualenv`.Pip is installed automatically with your Python download.

- venv

`venv` creates a buffer that protects your current computer state by on a separate, isolated environment. If you are using Python3 or higher, it is already installed.

For Python3 or higher, run the following in your terminal, replacing Name_Of_Environment with your desired name of the environment:
```bash
python -m venv Name_Of_Environment
```
- json

The `json` library is used to parse through the JSON files returned by the API calls. It is a standard library from Python/

- flask

`flask` is the library that runs the app and allows it to be hosted on `localhost`. It is required for this project. Install flask using this command:
```bash
pip install flask
```
- wheel

`wheel` goes hand in hand with `flask`. To install wheel, run the following command:

```bash
pip install wheel
```
- Jinja2

`jinja2` is used to set up templates for the multiple HTML files. It is required by `flask`. Install Jinja2 using this command:

```bash
pip install jinja2
```
- passlib

`passlib` provides the password hashing and encrpyting services required to store passwords. Install passlib using this command:

```bash
pip install passlib
```

## API Keys
To use this application you must generate API keys from the tastedive API and OMDb API.

Click [here](http://www.omdbapi.com/apikey.aspx) and follow the instructions to get your OMDb API key.

Click [here](https://tastedive.com/read/api) and follow the instructions to get your tastedive API key.

Once you have your keys, replace the placeholder keys in the keys.JSON file in the root directory. You will notice that there are two tastedive API keys in the JSON file. Fear not. You may use the same key for tastedive_movie and tastedive_book. The reason there are two is to prevent using up the API key limit.

The application is now ready to be used!
