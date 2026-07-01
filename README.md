The script html_excel.py is intended to facilitate the editing of the list of tools.  
* Run `python html_excel.py index.html tools_list.xlsx` to obtain an excel file with all the URLs, tool names, and descriptions.
* Add the desired tool names, URLs, and descriptions.
* Run `python html_excel.py tools_list.xlsx index_updated.html`.
* Verify the file by opening with your browser.
* Replace index.html (`mv index_updated.html index.html`)

Commit and push.
NB. the gitignore is set to ignore any .xlsx file