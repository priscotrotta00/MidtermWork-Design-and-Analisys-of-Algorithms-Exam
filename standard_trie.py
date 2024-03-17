from Collections.hash_table.probe_hash_map import ProbeHashMap

class standardTrie:
    '''
    Trie data structure implemented using hash table
    
    Attributes
    ----------
    trie : hash table
    hash table with nested hash table representing branches of trie. Presence of
    key '/' with value 'REF' represents termination node.
    REF is a referement to a ProbeHashMap
    
    Examples
    --------
    Dictionary containing dad, dab, and pila
    Trie View:
             ()
             /\
            d  p
           /    \
          a      i
         / \      \
        d   b      l
       /     \      \
     '/'     '/'     a      
      |       |       \
     list    list     '/'
      of      of       |
     page    page     list
                       of
                      page

    Dict View: {'d': {'a': {'d': {'/': REF}, 'b': {'/': REF}}}, 'p': {'i': {'l': {'a' : {'/': REF}}}}}  
    '''
    __slots__ = '__trie'

    def __init__(self):
        self.__trie = ProbeHashMap()

    def insert(self, word:str):
        current_level = self.__trie
        for letter in word:                                                     #For each letter in the word
            current_level = current_level.setdefault(letter, ProbeHashMap())    #I create/retrieve the hash associated with it 
        current_level.setdefault('/', ProbeHashMap())                           #the character / represents the string terminator
                                                                                #An hash is associated with it: the occurrence list of the word
    def search(self, word:str):
        current_level = self.__trie
        for letter in word:
            try:
                current_level = current_level[letter]
            except KeyError:
                return False            #return False if letter isn't in the current level hash --> word isn't in the trie
        return '/' in current_level     #At the end of the word, if I have the '/' then the word is found
                                        #Otherwise the word represented only a prefix, so I can return False

    def get(self, word:str):           
        current_level = self.__trie
        for letter in word:
            try:
                current_level = current_level[letter]
            except KeyError as ex:
                raise ex
        return current_level['/']       #return the value associated with the word if it exists

    #Remember: setdefault(k, v) returns:
    #-Value of the key if it is in the dictionary. 
    #-None if key is not in the dictionary and default_value is not specified. 
    #-default_value if key is not in the dictionary and default_value is specified.