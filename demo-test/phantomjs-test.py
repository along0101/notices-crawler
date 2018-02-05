#coding utf-8
#!/bin/python3

from selenium import webdriver

driver = webdriver.PhantomJS()

driver.get("http://baidu.com")

#file = driver.get_screenshot_as_png()

print(driver.find_element_by_tag_name("title"))

driver.quit()
