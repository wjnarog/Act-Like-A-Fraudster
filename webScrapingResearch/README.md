## UPDATE AS OF 11/13/24
For this week, I'd like to say I got the basics of webscraping under my belt, and I am confident we can set up a webscraper to pull info from land websites and filter it down from there.
From my (kinda shallow) research I believe we can accomplish everything we need to in the way of webscraping with the python libraries
  - Beautiful Soup (https://beautiful-soup-4.readthedocs.io/en/latest/#)
  - Selenium (https://selenium-python.readthedocs.io/index.html)

### Explanation
**Beautiful Soup** is a library that is super helpful with html parsing.  Basically as long as you pass in a good html page it has no problem isolating elements 
based on pretty much any identifying characteristic. It also does really well at creating iterable objects off of a page like a list of listings

**Selenium** seems really useful for actual webscraping, and I think the idea of is is super cool.  Basically, instead of just using an http get request to grab 
the html of a page (which sucks cause you can only scrape static pages then), selenium actually loads up a whole browser instance and lets you get info from that 
browser instance.  There's probably a ton more you can do, but for know I know how to load a page with selenium, wait for it to fully load, and then grab the page
source and parse it from there.

### Documents Created
For now I've made 2 jupyter documents that show my process and testing with the libraries and hopefully are kinda useful to reference in the future

The first one uses requests and Beautiful Soup following an online tutorial

The second one was created after I struggled to scrape one of the land websites we found through research.  Using Selenium, I was able to scrape this website.

### Time Log
research/formatting/documentation ~1hr

example scraper ~2.5 hrs

### TLDR
I got a basic idea of how to web scrape, feel free to run the jupyter commands

