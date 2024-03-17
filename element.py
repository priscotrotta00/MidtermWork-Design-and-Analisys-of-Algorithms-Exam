from Collections.map.red_black_tree import RedBlackTreeMap

class Element():
        
    __slots__ = '__web_site', '__is_dir', '__name', '__content', '__url'

    def __init__(self, website, is_dir:bool, name:str, content, url:str):    
        self.__web_site = website       #Reference to the WebSite object to which it belongs
        self.__is_dir = is_dir          #flag is_dir: if True the Element is a directory, otherwise Element is a page
        self.__name = name              #name of directory or page
        self.__content = content        #content of the Element --> String if Element is a page or Reference to a RBTreeMap if Element is  a directory
        self.__url = url                #url of the Element directory/page

    #------------Type method------------

    def isDir(self):    
        '''Return True if Element is a directory, False otherwise'''
        return self.__is_dir

    def isPage(self):   
        '''Return True if Element is a page, False otherwise'''
        return not self.__is_dir

    #------------Getter methods------------

    def getWebSite(self):
        return self.__web_site

    def getName(self):
        return self.__name

    def getContent(self):
        return self.__content

    def getUrl(self):
        return self.__url

    #------------Setter methods------------

    def setContent(self, content):
        if(self.isDir() and not isinstance(content, RedBlackTreeMap)): raise Exception('Content must be a RedBlackTreepMap for an Element directory')
        if(self.isPage() and not isinstance(content, str)): raise Exception('Content must be a string for an Element page')
        self.__content = content