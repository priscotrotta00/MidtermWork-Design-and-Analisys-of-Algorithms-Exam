from element import Element
from Collections.hash_table.probe_hash_map import ProbeHashMap
from Collections.priority_queue.heap_priority_queue import HeapPriorityQueue
from standard_trie import standardTrie

class InvertedIndex():

    class __Node():
        
        __slots__ = '__page', '__num_occ'

        def __init__(self, page:Element, num_occ:int):
            self.__page = page
            self.__num_occ = num_occ

        #------------Getter methods------------

        def getPage(self):
            return self.__page

        def getNumOcc(self):
            return self.__num_occ

        #------------Setter methods------------

        def setPage(self, page:Element):
            self.__page = page

        def setNumOcc(self, num_occ:int):
            self.__num_occ = num_occ


    __slosts__ = '__inv_ind'

    def __init__(self): #Complexity required: O(1)
        """it creates a new empty InvertedIndex"""
        self.__inv_ind = standardTrie()#
        #self.__inv_ind = ProbeHashMap()            

    def addWord(self, keyword:str): #Complexity required: O(len(keyword))
        """it adds the string keyword into the InvertedIndex"""
        self.__inv_ind.insert(keyword)#
        #self.__inv_ind.setdefault(keyword, ProbeHashMap())


    def addPage(self, page:Element):    #Complexity required: O(len(word) + log(list(word)))
        """it processes the Element page, and for each word in its content,
        this word is inserted in the inverted index if it is not present, and the page is inserted
        in the occurrence list of this word. The occurrence lists also saves the number of
        occurrences of the word in the page"""
        if (not isinstance(page, Element) or (not page.isPage())): raise TypeError(f'Error with the parameter {page}: Must be an Element page')
        content_page = page.getContent().split()                    #content_page contains all the words contained in the page
        url_page = page.getUrl()
        for word in content_page:
            try:        
                occurrence_list = self.__inv_ind.get(word)#         #I try to retrieve the occurrence list associated with the word
                #occurrence_list = self.__inv_ind[word]
            except KeyError:                                        #If a KeyError is thrown, then the word does not belong to the inverted index
                self.addWord(word)                                  #I add the word to the Inverted Index          
                occurrence_list = self.__inv_ind.get(word)#         #I retrieve the occurrence list associated with that word -- sicuro non lancio eccezioni perché l'ho appena inserita
                #occurrence_list = self.__inv_ind[word]  
                occurrence_list[url_page] = self.__Node(page, 1)    #and I initialize it with the Element page and the number of occurrence of the word for the current page        
            else:   #l'occurrence list associata alla parola già esisteva!
                try:
                    num_occ = occurrence_list[url_page].getNumOcc() #I try to retrieve the num_occ of the word in the current page
                except KeyError:                                    #If a KeyError is thrown, then the page does not belong to the occurrence list
                    occurrence_list[url_page] = self.__Node(page, 1)#I add the couple url_page-(Element page, num_occ) to the hash map
                else:   #all'interno dell'occurrence list già esisteva un riferimento a quella pagina per quella parola
                    occurrence_list[url_page].setNumOcc(num_occ + 1) #I increase the num_occ value for the current page

    def getList(self, keyword:str): #Complexity required: O(len(keyword))
        """it takes in input the string keyword, and it returns the
        corresponding occurrence list. It throws an Exception if there is no occurrence list
        associated with the string keyword."""
        return self.__inv_ind.get(keyword)#                         #I return the occurrence list associated with the keyword, it will be raise an 
        #ritorna KeyError se la chiave non esiste                   #exception if the list doesn't exist
        #return self.__inv_ind[keyword]