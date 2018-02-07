#-*- coding:utf-8 -*-
#!/bin/python3

from selenium import webdriver

#driver = webdriver.PhantomJS(executable_path=r"D:\DevTools\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver = webdriver.PhantomJS()

driver.get("http://data.eastmoney.com/notices/detail/600660/AN201801081075113027,JWU3JWE2JThmJWU4JTgwJTgwJWU3JThlJWJiJWU3JTkyJTgz.html")

driver.set_window_size(1980,1140)

#print(driver.title)

#driver.get_screenshot_as_file(r"C:\Users\ALU\Downloads\p1.png")

#assert "No results found." not in driver.page_source

print("done")

driver.quit()
