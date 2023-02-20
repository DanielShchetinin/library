import datetime


class Loan:
    
    def __init__(self, customer_id: int, book_id: int, return_date: datetime.date, loan_date: datetime = datetime.datetime.today(), loan_status: str = "Undetected"):
        
        self._customer_id = customer_id
        self._book_id = book_id
        self._return_date = return_date
        self._loan_date = loan_date
        self._loan_status = loan_status
    
    def get_loaned_customer_id(self):
        return self._customer_id
    
    def get_loaned_book_id(self):
        return self._book_id
    
    def get_loaned_return_date(self):
        return self._return_date
    
    def get_loaned_loan_date(self):
        return self._loan_date
    
    def get_loaned_loan_status(self):
        return self._loan_status
    
    def __str__(self):
        return f"Customer ID: {self._customer_id}, Book ID: {self._book_id}, Loaned: {self._loan_date}, Return: {self._return_date} | Status: {self._loan_status}"
    
    def __repr__(self):
        return self.__str__()