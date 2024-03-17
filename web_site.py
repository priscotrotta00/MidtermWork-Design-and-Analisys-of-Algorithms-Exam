from Collections.map.red_black_tree import RedBlackTreeMap
from Collections.hash_table.probe_hash_map import ProbeHashMap
from element import Element

class WebSite():

    '''    
    Class representing a web site. The structure of this class is the follow:

           Element (host name: RBTreeMap)               
                                /    \                
                               /      \
                              /        \
            Node (ndir: Element (ndir: RBTreeMap)) if node is a directory
            Node (npag: Element (npag: content)) if node is a page
    Attributes:
                           __host   -->   host name 
                      __home_page   -->   home page (initially set to None)
                 __home_directory   -->   Element(host, RebBlackTreeMap())

    '''
    __slots__ = '__host', '__home_page', '__home_directory'

    def __init__(self, host:str):   #Complexity required: O(1)
        """it creates a new WebSite object for saving the website hosted at
        host, where host is a string;"""
        self.__host = host                                                                  #Reference to the host name (e.g. www.unisa.it)
        self.__home_page = None                                                             #Reference to home page (index.html)
        self.__home_directory = Element(None, True, host, RedBlackTreeMap(), host)          #Reference to the home directory of the web site
    #Alla creazione di un oggetto WebSite, avrò un oggetto Element che ha come nome l'host del sito web
    #e come valore un RedBlackTreeMap (ovvero un albero che implementa una Map). Tutti gli altri nodi
    #saranno inseriti all'interno di questo RedBlackTreeMap

    def __isDir(self, elem:Element):    #Complexity required: O(1)
        """if the object Element referenced by elem is a directory returns True,
        otherwise it returns False. The format of elem is not constrained."""
        return isinstance(elem, Element) and elem.isDir()   #Check the type of the elem and return if this is a directory

    def __isPage(self, elem:Element):   #Complexity required: O(1)
        """if the object Element referenced by elem is a web page returns
        True, otherwise it returns False. The format of elem is not constrained."""
        return isinstance(elem, Element) and elem.isPage()  #Check the type of the elem and return if this is a page
    
    def __hasDir(self, ndir:str, cdir:Element):     #Complexity required: O(log k)
        """if in the current directory cdir there is a directory whose name
        is ndir, then it returns a reference to this directory, otherwise it throws an exception.
        An exception must be thrown even if the cdir is not a directory. Here ndir is a string,
        while cdir and the return value are objects of the class Element;"""
        if(not self.__isDir(cdir)):                 #If cdir is not a directory --> cdir is not an Element or cdir is a page
            if(not isinstance(cdir, Element)): raise TypeError(f'Parameter {cdir} must be an Element')    
            raise TypeError(f'Element {cdir.getName()} is not a directory')     #In both cases a key error will be thrown
        treeMap = cdir.getContent()                         #I retrieve the RedBlackTreeMap contained in the Element cdir
        try:
             ref = treeMap[ndir.swapcase()]                 #and I retrieve the value (Element) associated with the key ndir
        except KeyError:
            raise KeyError(f"In the directory {cdir.getName()} there isn't any directory called {ndir}")    #If the key doesn't exist, it will be raise an exception
        return ref                                          #otherwise I return this ref (Element)

    def __newDir(self, ndir:str, cdir:Element):     #Complexity required: O(k)
        """if in the current directory cdir there is a directory whose name
        is ndir, then it returns a reference to this directory, otherwise it creates such a
        directory and returns a reference to it. An exception must be thrown even if the cdir
        is not a directory. Here ndir is a string, while cdir and the return value are objects of
        the class Element;"""
        if(not self.__isDir(cdir)):                 #If cdir is not a directory --> cdir is not an Element or cdir is a page
            if(not isinstance(cdir, Element)): raise TypeError(f'Parameter {cdir} must be an Element')    
            raise TypeError(f'Element {cdir.getName()} is not a directory')     #In both cases a key error will be thrown
        treeMap = cdir.getContent()                 #I retrieve the RedBlackTreeMap contained in the Element cdir
        return treeMap.setdefault(ndir.swapcase(), Element(self, True, ndir, RedBlackTreeMap(), cdir.getUrl() + '/' + ndir)) 
    #Con questo metodo torno un riferimento all'Element directory ndir. Se già esiste ne torno il riferimento.
    #Se non esiste già, la creo! --> Creo un oggetto Element che ha come nome il nome della directory
    #e come content un riferimento ad un nuovo RedBlackTreeMap

    def __hasPage(self, npag:str, cdir:Element):    #Complexity required: O(log k)
        """if in the current directory cdir there is a webpage whose
        name is npage, then it returns a reference to this page, otherwise it throws an
        exception. An exception must be thrown even if the cdir is not a directory. Here
        npage is a string, while cdir and the return value are objects of the class Element;"""
        if(not self.__isDir(cdir)):                     #If cdir is not a directory --> cdir is not an Element or cdir is a page
            if(not isinstance(cdir, Element)): raise TypeError(f'Parameter {cdir} must be an Element')
            raise TypeError(f'Element {cdir.getName()} is not a directory') #In both cases a key error will be thrown
        treeMap = cdir.getContent()                         #I retrieve the RedBlackTreeMap contained in the Element cdir
        try:
            ref = treeMap[npag.swapcase()]                  #and I retrieve the value (Element) associated with the key npag
        except KeyError:
            raise KeyError(f"In the directory {cdir.getName()} there isn't any page called {npag}") #If the key doesn't exist, it will be raise an exception
        return ref                                          #otherwise I return this ref (Element)

    def __newPage(self, npag:str, cdir:Element):    #Complexity required: O(k)
        """if in the current directory cdir there is a webpage whose
        name is npage, then it returns a reference to this page, otherwise it creates such a
        page and returns a reference to it. An exception must be thrown even if the cdir is
        not a directory. Here ndir is a string, while cdir and the return value are objects of the
        class Element;"""
        if(not self.__isDir(cdir)):                     #If cdir is not a directory --> cdir is not an Element or cdir is a page
            if(not isinstance(cdir, Element)): raise TypeError(f'Parameter {cdir} must be an Element')
            raise TypeError(f'Element {cdir.getName()} is not a directory') #In both cases a key error will be thrown
        treeMap = cdir.getContent()                     #I retrieve the RedBlackTreeMap contained in the Element cdir
        return treeMap.setdefault(npag.swapcase(), Element(self, False, npag, None, cdir.getUrl() + '/' + npag))
    #Con questo metodo torno un riferimento all'Element page npag. Se già esiste ne torno il riferimento.
    #Se non esiste già, la creo! --> Creo un oggetto Element che ha come nome il nome della pagina
    #e come content None

    def getHomePage(self):  #Complexity required: O(1)
        """it returns the home page of the website at which the current object              
        refers or it throws an exception if an home page does not exist;"""
        if(self.__home_page is None): raise Exception(f"The homepage of {self.getHost()} doesn't exist")    #If the home page doesn't exists, it will be raise an exception
        return self.__home_page                                                                             #Otherwise I return its referement
        
    def getSiteString(self):    #Complexity required: O(n)
        """it returns a string showing the structure of the website."""
        def getSiteSubString(self, subString, elem, j):                         
            treeMap = elem.getContent()                                                 #I retrievey the treeMap contained in the Element
            for key,value in treeMap.items():                                           #For each (k,v) tuple in the tree
                subString += j*'-' + ' ' + key.swapcase() + "\n"                        #I add the name of page/directory to the string
                if(value.isDir()):                                                      #If value is a directory
                    subString = getSiteSubString(self, subString, value, int(j+3))      #I recall the same method with the next Element
            return subString                                                            #Then I return the string
    #START READING HERE        
        string = self.__host + "\n"                                                     #I initialize the final string whit the first line containing the host name            
        return getSiteSubString(self, string, self.__home_directory, 3)                 #I call the method getSiteSubString with the string,
                                                                                        #the referement to the next Element and the number of '-' that
                                                                                        #I have to print
    #Devo stampare prima l'attributo host dell'oggetto WebSite e poi fare una visita in order di tutti gli Element. 
    #Quando trovo un Element che rappresenta una directory, ne stampo prima il nome, per rispettare il vincolo sulla stampa,
    #e poi richiamo la funzione ricorsivamente sul nuovo Element 
    #--> funzione ricorsiva

    def insertPage(self, url:str, content:str): #Complexity required: O(l*k)
        """it saves and returns a new page of the website, where url
        is a string representing the URL of the page, and content is a string representing the
        text contained in the page."""
        
        path_array = url.split('/')                 #I create an array path_array with all strings contained in the url
        if '' in path_array: raise Exception('URL contains empty strings')   #I check that no one string is empty     
        if(self.__host != path_array[0]): raise Exception('Host is not correct!') #If the host of the url is different from WebSite's host, it will be raise an exception
        if(len(path_array) <= 1): raise Exception('URL must contains other words besides the host')
        
        elem = self.__home_directory                #elem is the Element that contains the home directory (remember that the content 
                                                    #of this Element is the tree representing the entire structure )
        
        for dir in path_array[1:-1]:                #Starting from the second word of the url (because the first word is the host!)                      
            try:
                elem = self.__hasDir(dir, elem)     #I call hasDir() method
            except:
                elem = self.__newDir(dir,elem)      #If it raises an exception, I call newDir() method
                                                    #Escludo l'ultima parola perché questa è la pagina da dovere creare
                                   
        dir = path_array[-1]                        #dir contains the name of the page
        try:
            page = self.__hasPage(dir, elem)        #I call hasPage() method
        except:
            page = self.__newPage(dir, elem)        #If it raises an exception, I call newPage() method
        page.setContent(content)                    #Now I can set the content of the new page
        if(elem is self.__home_directory and dir == "index.html"):  #If the page is the home page I initailize the attribute self.__home_page with the 
            self.__home_page = page                 #referement to this Element page
        return page                                 #Then I return the referement to this Element page
    #Per inserire una pagina, recupero in un array le cartelle e la pagina da creare
    #Verifico che l'url abbia come host proprio l'host dell'oggetto web site su cui l'inserimento viene richiamato
    #e che non contenga stringhe vuote.
    #Mi costruisco il percorso con newDir() che ricordo tornare il riferimento alla directory se già esiste oppure
    #la crea se non esiste e ne ritorna il riferimento.
    #Quando arrivo nell'ultima cartella inserisco la pagina con newPage() --> ha lo stesso comportamento di newDir()
    #A questo punto posso inserirne il contenuto e verificare se la pagina inserita è l'home page --> nel caso inizializzo self.__home_page
        
    def getSiteFromPage(page:Element):    #Complexity required: O(1)
        """that given an Element page returns the WebSite object at
        which that page belongs."""
        if (not isinstance(page, Element) or (not page.isPage())): raise TypeError(f'Error with the parameter {page}: Must be an Element page')
        return page.getWebSite()                                                    #I return the referement of the WebSite to which it belongs
    #Mi conviene avere un oggetto WebSite e non una stringa --> Complessità O(1)

    #------------Getter methods------------

    def getHost(self):
        return self.__host