#!/usr/bin/env python
# coding: utf-8

# # Web scraping Football English Premier League Data 

# Welcome to my web scraping project for the English Premier League! 
# 
# As a football enthusiast, I have always been fascinated by the performance of my favourite teams and players. But I wanted to take my analysis to the next level by gathering data from English Premier League website and using web scraping techniques to extract meaningful insights using Python programming language and the BeautifulSoup library. 
# 
# So let's get started! 

# Let's start with importing "requests" module.
# 
# The "requests" module in Python is a powerful tool for making HTTP requests to web servers and receiving responses. It provides a simple and user-friendly interface for sending HTTP requests and handling responses, making it an essential tool for web scraping, web development, and data analysis.

# In[1]:


#importing request module
import requests


# We are initializing and storing our desired web page into the variable "url", so that we can write "url" instead of the whole url of the webpage.

# In[2]:


#initializing the url of the web-page that we want to retrieve data from
url = "https://fbref.com/en/comps/9/Premier-League-Stats"


# Here, we are using the requests module to send an HTTP GET request to retrieve the contents of a webpage located at https://fbref.com/en/comps/9/Premier-League-Stats. 
# 
# The get() function of the requests module is used to send the request, and the response from the server is stored in the "data" variable.
# 
# By doing this we are making a request to the webpage.

# In[3]:


#sending HTML "get" request to the url and retrieving the data into "data"
data = requests.get(url)


# However, the response we get from the webpage is in the form of HTML which is no readable. So we want to parsh them into readable format by using BeautifulSoup library. 
# 
# If you haven't installed BeautifulSoup, you can install it using 'pip install beautifulsoup4' command.  

# In[4]:


#checking the html text we just retrieved. 
data.text


# We can see that there are lots of unwanted html text in our data. We need to filter out those to get the data we are actually looking for.
# 
# BeautifulSoup is a Python library that allows us to parse HTML and XML documents. It is a very popular library for web scraping and data extraction. 
# BeautifulSoup would help us navigate and search a parsed HTML or XML document, so that we can easily extract the data we need. 
# 
# So why not we use this powerful library!

# In[5]:


#importing beautifulsoup library
from bs4 import BeautifulSoup


# Parshing the html text of the webpage into variable "soup"

# In[6]:


#passing the html text into BeautifulSoup class
soup = BeautifulSoup(data.text)
soup


# BeautifulSoup has select() function which help us to find our desired element in the webpage using CSS (Cascading Style Sheets) selector. Here we are finding the table named "table.stats_table" in the webpage. For this we need to open the web-page and right click on to our desired table and go to the inspector to see the html codes. The table extracted is stored into the variable "table".

# In[7]:


#select uses css selector which gives lots of flexibility to select different elements, classes, IDs, etc..
table = soup.select("table.stats_table")[0]
table


# Now that we found our desired table, we can look into the tags we need by using find_all() function. Here we are extracting the links associated with the tag "a" and storing into the variable "links"

# In[8]:


#find_all finds only tags
links = table.find_all("a")
links


# As we are interested only the value of "href", we are trying to find those with get() function.  

# In[9]:


#getting the "href" values
links = [l.get("href") for l in links]
links


# We are now looking for the urls which contain "squads" 

# In[10]:


#getting only the links which contains squads
links = [l for l in links if "/squads/" in l]
links


# As we can see that the above urls are Relative links, we want their respective Absolute links. To convert relative links into absolute links we can simply append "https://fbref.com" just before the relative links.
# 
# Let's now convert them.

# In[11]:


#formatting url links so that we get the full (absolute links) urls
team_urls = [f"https://fbref.com{l}" for l in links]
#printing the extracted team_urls
team_urls


# Our desired absolute links are stored in the variable "team_urls" in the form of list, so we'll go to individual team_url to extract data from two of the tables.

# In[12]:


#considering only the first url in from the team_urls
team_url = team_urls[0]


# Like the way we did request the webpage to retrieve data, we again use the request.get() function to get into the team_url to extract data  then store the content into the variable "data".

# In[13]:


#requesting and storing the content from the first url into the variable "data". 
data = requests.get(team_url)


# Let's import Pandas, an open-source Python library that provides powerful and flexible tools for data analysis and manipulation.  

# In[14]:


#importing pandas as pd so that we can address it with its abbreviation each time we used.
import pandas as pd


# We now use the read_html() function of pandas to retrieve the data from the table "Scoring & Fixtures" and store the content into variable "matches" as a dataframe.

# In[15]:


#using the pandas read_html() function we store the webpage content into the variable "matches" as a dataframe.
matches = pd.read_html(data.text, match="Scores & Fixtures")


# Let's now print matches to see the content we just retrieved.

# In[16]:


#printing matches
matches[0].head()


# Walah! we finally completed first part of web scraping where we extracted data from the table "Scores & Fixtures" and stored in the variable "matches".
# 
# Now in the second part of our web scraping session we'll repeat the above steps to extract data from another table from the same webpage. So we'll quickly repeat the steps and extract data from the table "Shooting" then store it to the variable "shooting".

# In[17]:


#parshing the html text into variable "soup" using BeautifulSoup class
soup = BeautifulSoup(data.text)

#pointing into the tag "a" using find_all function
links = soup.find_all("a")

#getting the "href" values using get() function and storing the urls into variables "links"
links = [l.get("href") for l in links]

#extrating only the links which contains "shooting"
links = [l for l in links if l and "shooting/" in l]

#requesting the "https://fbref.com" to retrieve the content of the links[0] and store them into the variable "data"
data = requests.get(f"https://fbref.com{links[0]}")

#using pandas read_html() function we store the webpage content into the variable "shooting" as a dataframe.
shooting = pd.read_html(data.text, match="Shooting")[0]

#dropping the secondary column name using droplevel() function.
shooting.columns = shooting.columns.droplevel()

#printing the shooting dataframe
shooting.head()


# Let's look into the summary of our "shooting" dataframe.

# In[18]:


#"info()" function is a method in pandas library for getting concise information about a DataFrame or Series.
shooting.info()


# We can see that there are 26 columns but we dont need them all, we need only the "Date", "Sh", "SoT", "Dist", "FP", "PK", and "PKatt" columns. We want to combine these columns of "shooting" with the dataframe "matches". So to do this we use the "merge()" function to form a new dataframe "team_data"

# In[19]:


#combining the chosen columns of "shooting" with "matches" dataframe on column "Date" to form a new dataframe "team_data".
team_data = matches[0].merge(shooting[["Date","Sh","SoT","Dist","FK","PK","PKatt"]], on="Date")


# Let's check out "team_data" with "head()" method of pandas library which is used to display the first n rows of a DataFrame. 

# In[20]:


#The default number of rows displayed is 5.
team_data.head()


# Here we are done with the extraction of data for the first team in the "team_urls" (if you recall we had a list of team urls). We have extracted data from tables "Scores & Fixtures" and "Shooting" for the most recent session (i.e. 2023). We need to do a lot more data extraction work for each team in the "Premier League" for some number of sessions. Instead of repeating the above steps multiple times for multiple teams we want to form a loop where the extraction of data keep on repeating for all the teams in the Squads. 
# 
# Before we do that we'll import the "time" module which is a built-in Python module that provides various functions to handle time-related tasks, such as measuring time elapsed, pausing code execution, and formatting time values.

# In[21]:


#importing time module
import time


# Let's make a list of years for which we want to extract data. You can add any number of desired sessions in the list, here I've for 3 sessions- 2021 to 2023.    

# In[22]:


#creating list of desired years
years = list(range(2023,2020,-1))
years


# In order to store all our extracted data, we want to initialize a list. 

# In[23]:


#initializing an empty list to store all the data to be extracted
all_matches = []

#assigning the main url of the webpage to a variable "standings_url"
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"


# Now let's begin the "for" loop

# In[24]:


#initializing "for" loop to iterate into each year
for year in years:
    #extracting the urls of each and every team    
    #sending HTTP GET request to "standings_url" and retrieving the content of the webpage. 
    data = requests.get(standings_url)
    #passing "data" (string) as an argument to BeautifulSoup constructor to create a BeautifulSoup object "soup".
    soup = BeautifulSoup(data.text)
    #extracting elements from HTML document ("table.stats_table") based on CSS selectors.
    standings_table = soup.select("table.stats_table")[0]
    #extracting "href" value from an HTML document that has tag "a". 
    links = [l.get("href") for l in standings_table.find_all("a")]
    #extracting links which contain "/squads/"
    links = [l for l in links if "/squads/" in l]
    #converting relative links into absolute links
    team_urls = [f"https://fbref.com{l}" for l in links]

    #extracting previous session's data
    #extracting "href" value from HTML document ("a.prev") based on CSS selectors.
    previous_session = soup.select("a.prev")[0].get("href")
    #updating "standings_url" with the "previous_session" link
    standings_url = f"https://fbref.com{previous_session}"
    
    #initializing "for" loop to iterate into each "team_url"
    for team_url in team_urls:
        #extracting team name from its url and storing into variable "team_name"
        team_name = team_url.split("/")[-1].replace("-Stats","").replace("-"," ")
     
        #extracting data from the table "Scores & Fixtures"
        #sending HTTP GET request to "team_url" and retrieving the content of the webpage.
        data = requests.get(team_url)
        #parsing HTML table ("Score & Fixtures") into pandas DataFrames.
        matches = pd.read_html(data.text, match="Scores & Fixtures")[0]
        
        #extracting data from the table "Shooting"
        #passing "data" (string) as an argument to BeautifulSoup constructor to create a BeautifulSoup object "soup".
        soup = BeautifulSoup(data.text)
        #extracting "href" value from an HTML document that has tag "a".
        links = [l.get("href") for l in soup.find_all("a")]
        #extracting links which contain "all_comps/shooting/"
        links = [l for l in links if l and "all_comps/shooting/" in l]
        #converting relative link into absolute link and 
        #sending HTTP GET request the url and retrieving the content of the webpage.
        data = requests.get(f"https://fbref.com{links[0]}")
        #parsing HTML table ("Shooting") into pandas DataFrames.
        shooting = pd.read_html(data.text, match="Shooting")[0]
        #droping second level column index
        shooting.columns = shooting.columns.droplevel()
        
        #controlling flow statements to handle errors arise due to missing data.
        try:
            #merging the selected columns from the table "Shooting" with the table "matches" and
            #forming a new dataframe "team_data"
            team_data = matches.merge(shooting[["Date","Sh","SoT","Dist","FK","PK","PKatt"]], on="Date")
        except ValueError:
            continue
        
        #filtering in type of the competition with "Premier League"
        team_data = team_data[team_data["Comp"] == "Premier League"]
        #forming new column "Session" in team_data
        team_data["Session"] = year
        #forming new column "Team" 
        team_data["Team"] = team_name
        #adding "team_data" into the list "all_matches"
        all_matches.append(team_data)
        
        #pausing the execution for a second
        #this is ensure not to trigger traffic conjestion to the website due to these data extraction requests
        time.sleep(1)


# We can see that "all_matches" is a list of mulitple dataframes so we concatenate all the list to form a dataframe 

# In[25]:


all_matches


# In[26]:


#concatenating all the dataframes of "all_matches" to form a DataFrame
match_df = pd.concat(all_matches)


# Let's look into the DataFrame we just formed

# In[27]:


match_df


# In[29]:


match_df.shape


# We successfully extracted 2088 rows of data with 28 columns. Before we conclude our web scraping session I just want to do a minor cleaning onto the name of columns by making them lower_case. This is an optional step you can skip it if you are comfortable typing headline styles of column names. 

# In[30]:


#converting headline style column names into lower_case
match_df.columns = [c.lower() for c in match_df.columns]


# Let's check it out the final look of our DataFrame

# In[31]:


#printing dataframe "match_df"
match_df


# We've come so far to form this dataframe with match details. It is time to save our data for future. We'll export the dataframe into CSV file with the method "to_csv()". This method will save our dataframe in the current working directory in CSV format.

# In[32]:


#extracting dataframe into CSV file
match_df.to_csv("matches.csv")


# Now that we know how to scrape data from webpage, we can extract any data we want from any webpages for our upcoming projects. With this we conclude our web scraping session.
# 
# Happy Learning!
