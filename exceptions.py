# Global Exceptions

class NoNumbersEntered(Exception):
    pass

class NoUsedNumbersEntered(Exception):
    pass

# Address Exceptions

class NegativeNumber(Exception):
    pass

class CantBeDigit(Exception):
    pass

# Database Exceptions

class DatabaseCreateError(Exception):
    pass

class DatabaseLoadError(Exception):
    pass
    
# Customers Exceptions

class UsedID(Exception):
    pass

class CustomerNotExist(Exception):
    pass

class CustomerHaveBooks(Exception):
    pass

# Books Exceptions

class BookNotExist(Exception):
    pass

class BookIDUsed(Exception):
    pass

# Loans Exceptions

class ToMuchBooksForCustomer(Exception):
    pass

class LoanedBook(Exception):
    pass