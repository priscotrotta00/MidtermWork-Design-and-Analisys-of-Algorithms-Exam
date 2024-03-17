import os      
from time import time
from web_site import WebSite
from inverted_index import InvertedIndex
from Collections.priority_queue.heap_priority_queue import *
from Collections.hash_table.probe_hash_map import ProbeHashMap

class SearchEngine:

    __slots__ = '__inv_ind', '__hosts_map'

    def __init__(self, namedir:str):
        """This method initializes the SearchEngine, by taking in input a
        directory in which there are multiple files each representing a different webpage.
        Each file contains in the first line the URL (including the hostname) and in the next
        lines the content of the webpage. This function populates the database of the search
        engine, by initializing and inserting values in all the necessary data structures."""

        self.__inv_ind = InvertedIndex()
        self.__hosts_map = ProbeHashMap()

        for file in os.listdir(namedir):                                            #For each file in the directory
            f = open(namedir + "/" + file, 'r')                                     #I open the file
            url = f.readline().rstrip()                                             #I read the first line containing the url. rstrip() toglie spazi e \n dopo la stringa
            host_name = url.split('/')[0]                                           #I retrieve the host name of the page from the url
            web_site = self.__hosts_map.setdefault(host_name, WebSite(host_name))   #I create a new WebSite object if it doesn't already exists, otherwise I retrieve it
            content = f.read()                                                      #I read the remaining text
            page = web_site.insertPage(url, content)                                #I insert the page in the WebSite object associated whit it
            #La insert potrebbe lanciare un'eccezione se l'host name dell'oggetto WebSite è diverso dall'host contenuto nell'url.
            #Nel mio caso questa eccezione non verrà mai lanciata perché l'host name è recuperato proprio dall'url! 
            self.__inv_ind.addPage(page)                                            #I add the page to the Inverted Index
            f.close()                                                               #I close the file

    def search(self, keyword:str, k:int):
        """it searches the k web pages with the maximum number of
        occurrences of the searched keyword. It returns a string s built as follows: for each
        of these k pages sorted in descending order of occurrences, the site strings (as
        defined above) of the site hosting that page is added to s, unless this site has been
        already inserted."""

        string = str()                                                                  #I initialize the return string

        try:
            pages_list = self.__inv_ind.getList(keyword)                                #I retrieve the occurrence list associated with the keyword
        except KeyError: #Voglio accedere all'occurrence list di una parola che non è mai stata inserita nell'inverted index
            return string.rstrip()

        heap = HeapPriorityQueue()                                                      #I create an heapPriorityQueue

        for key, value in pages_list.items():                                           #For each tuple in the hash map
            heap.add((-1)*value.getNumOcc(), (value.getPage(), key))                    #I put the number of occurrence (negative) of the word in a heap like keys
                                                                                        #and the couple Element page, url of the page like values

        for i in range(k):                                                              #For k times
            #remove_min() ritorna una tupla oppure un'eccezione se la coda è vuota
            try:
                num_occ,page_url = heap.remove_min()                                    #I remove the minimum tuple (key, value)
                #page_url is a couple of two elements
                #page_url[0] is the Element page associated with the page 
                #page_url[1] is the url of the page
            except Empty:   #quindi la coda era vuota
                return string.rstrip()
            web_site = WebSite.getSiteFromPage(page_url[0]) #page_url[0] is the Element page
            if web_site.getHost() not in string:                                        #If this WebSite has not been added to the return string yer
                string += web_site.getSiteString()                                      #I add its site string
            
        return string.rstrip()                                                          #and I return the string