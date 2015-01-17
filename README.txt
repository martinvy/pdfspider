=====================
ISJ project 2013/2014
=====================

Variant:  Finding and downloading reports of research projects
Language: Python 3.4.0
Author:   Martin Veselovsky, xvesel60

Usage via terminal
------------------
Get all links from specified website, finally print all
gathered reports as couple - name of report and url

python3 spider.py [-h] [-d] url

  url             Url of website
  -h, --help      show this help message and exit
  -d, --download  Immediate downloading

Usage via Graphical user interface - GUI
----------------------------------------
Specify url of main website and search. GUI contains two boxes,
one for printing of all visited sites, second for reports.
Gathered reports are separated by main website.

python3 gui.py

