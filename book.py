class Book:
    
    def __init__(self, book_id: int, book_name: str, book_author: str, published_year: int, book_type: int = 3):
        
        self._book_id = book_id
        self._book_name = book_name
        self._book_author = book_author
        self._published_year = published_year
        self._book_type = book_type
        
    def get_book_info(self):
        return f"[{self._book_id}] Book: `{self._book_name}` Author: {self._book_author}"   
        
    def get_book_id(self):
        return self._book_id
    
    def get_book_name(self):
        return self._book_name
        
    def get_book_author(self):
        return self._book_author
    
    def get_book_publish_year(self):
        return self._published_year
    
    def get_book_type(self):
        return self._book_type
    
    def set_book_type(self, new_book_type):
        self._book_type = new_book_type
        
    def __str__(self):
        return f"[{self._book_id}] Book name: `{self._book_name}`. Author: {self._book_author}."
    