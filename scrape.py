#NAME - ANSH AGARWAL


from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import subprocess, traceback, sys, json
from subprocess import Popen
import importlib as imp
import time
import os

class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.BFSorder = []
        self.DFSorder = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        if node in self.visited:
            return        
        self.visited.add(node)
        for child in self.go(node):
            self.dfs_search(child)

    def bfs_search(self, node):
        if node in self.visited:
            return 
        todo = [node]
        self.visited.add(node)
        while len(todo) > 0:
            curr = todo.pop(0)
            for child in self.go(curr):
                if not child in self.visited:
                    todo.append(child)
                    self.visited.add(child)
           

        
class FileScraper(GraphScraper):
    def __init__(self):
        super().__init__()
        if not os.path.exists("Files"):
            with zipfile.ZipFile("files.zip") as zf:
                zf.extractall()

    def go(self, node):      
        with open("Files/" + node + ".txt") as f:
            data = f.read()
        lines = data.split("\n")
        node_name = lines[0].split(" ")
        node_childern = lines[1].split(" ")
        node_BFSstr = lines[2].split(" ")[1]
        node_DFSstr = lines[3].split(" ")[1]
        self.BFSorder.append(node_BFSstr)
        self.DFSorder.append(node_DFSstr)
       
        return node_childern
    
    
class WebScraper(GraphScraper):
    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver

    def go(self, url):
        self.driver.get(url)
        todo = [url]
        self.visited.add(url)
        while len(todo) > 0:
            
            link = todo.pop(0)
            self.driver.get(link)
            
            btn1 = self.driver.find_element_by_id('BFS')
            btn2 = self.driver.find_element_by_id('DFS')
            btn1.click()
            btn2.click()
            self.BFSorder.append(btn1.text)
            self.DFSorder.append(btn2.text)
            
        links = self.driver.find_elements_by_tag_name('a')
        return [link.get_attribute('href') for link in links]
    
    def dfs_pass(self, start_url):
        password = ''
        self.visited = set()
        self.DFSorder = []
        self.dfs_search(start_url)
        return password.join(self.DFSorder)
    
    def bfs_pass(self, start_url):
        password = ''
        self.visited = set()
        self.BFSorder = []
        self.bfs_search(start_url)
        return password.join(self.BFSorder)

    def protected_df(self, url, password):
      
        old_tr_count = 0
        rows = []
        header = []
        self.driver.get(url)
        pwd = self.driver.find_element_by_id('password-input')
        pwd.clear()
        pwd.send_keys(password)
        btn = self.driver.find_element_by_id('attempt-button')
        btn.click()
        time.sleep(1.5)
        
        
        doc = BeautifulSoup(self.driver.page_source)
        new_tr_count = len(doc.find_all('tr'))
        while old_tr_count != new_tr_count:
            old_tr_count = new_tr_count
            load_btn = self.driver.find_element_by_id('more-locations-button')
            load_btn.click()
            time.sleep(1.5)
            doc_1 = BeautifulSoup(self.driver.page_source)
            new_tr_count = len(doc_1.find_all('tr'))
        
        for tr in doc_1.find_all('tr'):
            if len(tr.find_all('td')) != 0:
                rows.append([td.get_text() for td in tr.find_all('td')])
                
        for th in doc_1.find_all('th'):
            header.append(th.get_text())
       
        df = pd.DataFrame(rows, columns = header)
        return df