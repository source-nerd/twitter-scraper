# Twitter Scraper
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Updates](https://pyup.io/repos/github/source-nerd/twitter-scraper/shield.svg)](https://pyup.io/repos/github/source-nerd/twitter-scraper/)

A simple Python based Twitter Scraper with the ability of scripng tweets either by username or by a search query (Supports other search params as well). This program supports `STOP / RESUME` operation as it keeps a log of all the previous position id's. 
This project was created inorder to bypass twitter's 7 day policy since it doesn't allow to fetch tweets which are more than 7 days old as I needed some data for my research project. 
**Please Note: This is not an alternative for the official API's provided by the twitter**

This project is intented for students, researchers & all those who abide by twitter's data terms and conditions.

## Contents
1. scraper.py
2. searchParams.py
3. tweets.py
4. main.py
5. requirements.txt

## Usage
1. `Scraper.py` contains all the essential code required to grab tweets and store in the csv file
2. `searchParams.py` is a class for initializing seach parameters
3. `tweets.py` is a class whose object for each tweet
4. `main.py` - The main class required for calling all the above code. This file takes multiple arguments and is responsible for initializing all other files.
**HELP**
`python main.py --help`
 
## Prerequisites & Installation Instructions
This Project is intented to be used with Python `3.x` but feel free to convert it inorder to use it for Python `2.x`.
A **requirements.txt** file is provided with the project, which contains all the essential packages to run this project.
```
pip install -r requirements.txt
```

## Running the code
Use `main.py` to run the code
For help: -> `python main.py --help`

Example:
Search for **github** keyword between **2018-06-15 to 2018-06-20** and save it to **test.csv** with log file as **test.log**.
```
python main.py --searchquery github --since 2018-06-15 --until 2018-06-20 --op test.csv --log test.log
```

## Output
The output of the scraper is saved in the output file provided in the parameters. By default the outpfile file is `op.csv`.
The program also keeps a log of all the previous search positions, and writes it to the logger file provided in the params. By default, the log file is `def_log.log`. This file is required inorder to resume the scraping operation if interrupted in between.
**Note: If you want to `RESUME` your previous incomplete scrape operation, make sure to provide the same log file as you did in the first instance.**

## Feedback & Final Thoughts
Again, this project is intended for Education use. Feel free to use it. You may face cookies problem wherein running your code for the first time will work perfectly fine, but every other time it will fail. So, inorder to fix this, try to use `PROXY`. 
`--proxy` parameter can be used to pass proxy ip and port.
E.G: `0.0.0.0:80`
There are lots of free proxy sites out there that you can use.

The code may not be very optimized, so if you tend to find any bug fixes, feature requests, pull requests, feedback, etc., are welcome... If you like this project, please do give it a star.
