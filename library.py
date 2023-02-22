import datetime
import os
import pickle
import time

from address import Address
from book import Book
from customer import Customer
from exceptions import *
from loan import Loan
from visual_params import *

DB_URL = "Exams\\Library_Project\\library_database.pickle"

class Library: 
    
    def __init__(self, library_name: str, library_address: Address):
        
        self._library_name = library_name
        self._library_address = library_address
        
        self._loans: dict[int, Loan] = {}
        self._books: dict[int, Book] = {}
        self._customers: dict[int, Customer] = {}
        self._library: dict[str, Library] = {}
        self._loaned_for_customer: dict[int, list] = {}
        self._loaned_books: list[int] = []
        
    # Database System
    
    def save_library_to_dict(self, library):
        self._library["Library"] = library
        return True
    
    def save_to_picke(self, library):
        with open(DB_URL, "wb") as file:
            pickle.dump(library, file)
            file.close
            print("Saved")
            
    @staticmethod
    def load_from_pickle():
        with open(DB_URL, "rb") as file:
                library:Library = pickle.load(file)
                file.close
        return library            
    

    # Create func`s

    def add_customer(self, customer_id: int, customer_first_name: str, customer_last_name: str, address: Address, email: str, birth_date):
        if customer_id in self._customers:
            return False
        customer = Customer(customer_id, customer_first_name, customer_last_name, address, email, birth_date)
        self._customers[customer_id] = customer
        return True
    
    def add_book(self, book_id: int, book_name: str, book_autor: str, published_year: int, book_type: int = 3):
        if book_id in self._books:
            return False
        book = Book(book_id, book_name, book_autor, published_year, book_type)
        self._books[book_id] = book
        return True
    
    def create_loan_book(self, customer_id, book_id, return_date, loan_date, loan_status):
        loan_id = int(book_id)
        if customer_id not in self._loans:
            loan = Loan(customer_id, book_id, return_date, loan_date, loan_status)
            self._loans[loan_id] = loan

            
    # Read func`s
    
    def get_library(self): 
        return self._library["Library"]
    
    def get_library_name(self):
        return self._library_name
    
    def get_library_address(self):
        return self._library_address
    
    def get_library_full_information(self):
        print("Library Name:", self._library_name)
        print("Library Address:", self._library_address)
        return True
    
    def get_customer_by_id(self, customer_id):
        return self._customers.get(customer_id)
    
    def get_customers_dict(self):
        return self._customers
    
    def get_book_dict(self):
        return self._books
    
    def get_loans_dict(self):
        return self._loans
    
    def get_customer_full_info(self, customer_id):
        print("Customer ID:", customer_id)
        print("Full Name:", self._customers[customer_id].get_customer_full_name())
        print("Email:", self._customers[customer_id].get_customer_email())
        print("Full Address:", self._customers[customer_id].get_customer_address())
        print("Age:", self._customers[customer_id].get_customer_age(), "\n")
        if len(self._loaned_for_customer[customer_id]) == 0:
            print("No active loans for this Customer.")
        else:
            print("Active Loans:")
        
            loan:Loan = self._loans
            for key in loan:
                
                loaned:Loan = loan[key]
                customer_id = loaned.get_loaned_customer_id()
                status = loaned.get_loaned_loan_status()
                if int(customer_id) == int(customer_id) and status == "Loaned":
                    book_id = loaned.get_loaned_book_id()
                    book = self.get_book_by_id(int(book_id))
                    book_author = book.get_book_author()
                    loan_date = loaned.get_loaned_loan_date()
                    loan_date = datetime.date.strftime(loan_date, "%d.%m.%Y")
                    return_date_for_change = loaned.get_loaned_return_date()
                    return_date = datetime.date.strftime(return_date_for_change, "%d.%m.%Y")
                    if datetime.date.today() > return_date_for_change:
                        status = "Expired"
                    print(f"| Book: [{book_id}] `{book.get_book_name()}` by {book_author} | Loaned: {loan_date} Return: {return_date} | Status: {status}")
        
        
        
    def get_book_full_info(self, book_id):
        print("Book ID:", book_id)
        print("Book Name:", self._books[book_id].get_book_name())
        print("Book Author:", self._books[book_id].get_book_author())
        print("Book Publish Year:", self._books[book_id].get_book_publish_year())
        print("Book Type:", self._books[book_id].get_book_type(), "\n")
        return_date = self._loans[int(book_id)].get_loaned_return_date()
        if datetime.date.today() > return_date:
            print("Status: Loan Expired")
            return True
        if int(book_id) in self._loaned_books:
            print("Status: Loaned")
            return True
        else: print("Status: Not Loaned")
        
    def get_customer_by_name(self, name) -> list[Customer]:
        result = []
        for customer_id, customer in self._customers.items():
            if customer._customer_first_name == name:
                result.append(customer)
        return result
    
    def get_book_by_id(self, book_id):
        return self._books.get(book_id)
    
    def get_book_by_name(self, name):
        result = []
        for book_id, book in self._books.items():
            if book._book_name == name:
                result.append(book)
        return result
    
    def get_loan_by_id(self, loan_id):
        return self._loans.get(int(loan_id))
    
    def get_book_by_author(self, author_name) -> list[Book]:
        result = []
        for book_id, book in self._books.items():
            if book._book_author == author_name:
                result.append(book)
        return result
    
    def get_loans_for_customer(self):
        return self._loaned_for_customer
    
    def get_loaned_books(self):
        return self._loaned_books
    
    def get_loan_logs(self):
        loans:Loan = self._loans
        customer:Customer = self._customers
        for key in loans:
            loaned:Loan = loans[key]
            status = loaned.get_loaned_loan_status()
            
            customer_id = loaned.get_loaned_customer_id()
            customer = self.get_customer_by_id(int(customer_id))
            customer_name = customer.get_customer_full_name()

            book_id = loaned.get_loaned_book_id()
            book = self.get_book_by_id(int(book_id))
            book_name = book.get_book_name()
            book_author = book.get_book_author()
            
            loan_date_for_change = loaned.get_loaned_loan_date()
            loan_date = datetime.date.strftime(loan_date_for_change, "%d.%m.%Y")
            return_date_for_change = loaned.get_loaned_return_date()
            return_date = datetime.date.strftime(return_date_for_change, "%d.%m.%Y")
            
            if datetime.date.today() > return_date_for_change:
                status = "Expired"
            print(f"| Customer: [{customer_id}] {customer_name}. | Book: [{book_id}] `{book_name}` By Author: {book_author}. | Loan Date: {loan_date}, Return Date: {return_date} | Status: {status}")
    
    def get_late_loan_logs(self):
        loans:Loan = self._loans
        customer:Customer = self._customers
        for key in loans:
            loaned:Loan = loans[key]
            status = loaned.get_loaned_loan_status()
            
            customer_id = loaned.get_loaned_customer_id()
            customer = self.get_customer_by_id(int(customer_id))
            customer_name = customer.get_customer_full_name()

            book_id = loaned.get_loaned_book_id()
            book = self.get_book_by_id(int(book_id))
            book_name = book.get_book_name()
            book_author = book.get_book_author()
            
            loan_date_for_change = loaned.get_loaned_loan_date()
            loan_date = datetime.date.strftime(loan_date_for_change, "%d.%m.%Y")
            return_date_for_change = loaned.get_loaned_return_date()
            return_date = datetime.date.strftime(return_date_for_change, "%d.%m.%Y")
            
            if datetime.date.today() > return_date_for_change:
                status = "Expired"
            if status == "Expired":
                print(f"| Customer: [{customer_id}] {customer_name}. | Book: [{book_id}] `{book_name}` By Author: {book_author}. | Loan Date: {loan_date}, Return Date: {return_date} | Status: {status}")
    
    # Update func`s
    
    def update_library_name(self, new_name):
        self._library_name = new_name
        return True
    
    def update_library_address(self, address:Address):
        self._library_address = address
        return True
    
    # Delete func`s
    
    def delete_customer(self, customer_id):
        if customer_id in self._customers:
            self._customers.pop(customer_id)
            return True
        else:
            return False
    
    def delete_book(self, book_id):
        if book_id in self._books:
            self._books.pop(book_id)
            return True
        else:
            return False
        
    def delete_loan(self, return_book_id):
        
        loan = self._loans[return_book_id]
        customer_id = loan.get_loaned_customer_id()
        loan_book:list = self._loaned_books
        self._loaned_for_customer[int(customer_id)].pop(int(return_book_id))
        loan_book.remove(int(return_book_id))
        self._loans.pop(int(return_book_id))
    
    # __str__ and __repr__
    
    def __str__(self):
        return f"Library name: {self.get_library_name()}, Address: {self.get_library_address()}"
    
    def __repr__(self):
        return self.__str__()
    
# Main and Database system

def main():
    
    try:
        print(visual_database_menu)
        print(database_menu, "\n")
        database_menu_choose = input(enter_choose)
    
        if not database_menu_choose.isdigit():
            raise NoNumbersEntered()
            
        if database_menu_choose not in ["1", "2", "3", "4"]:
            raise NoUsedNumbersEntered()
    
    except NoNumbersEntered as error_message:
        print(visual_space)
        print("You can use only digits.")
        main()
        
    except NoUsedNumbersEntered as error_message:
        print(visual_space)
        print("You can use only displayed digits.")
        main()
        
    except Exception as error_message:
        print(visual_space)
        print(error_text)
        main()
    
    finally:
            library:Library.save_to_picke()
        
    if database_menu_choose == "1":
        
        try:
            if not os.path.isfile(DB_URL):
                raise DatabaseLoadError()
            
            else:
                library = Library.load_from_pickle()
                print(visual_space)
                print("\nLoading database...")
                time.sleep(1)
                print(visual_space)
                print(f"Database `{library.get_library_name()}` is loaded.")
                time.sleep(1)
                print(visual_space)
                goto_library_menu()
                
        except DatabaseLoadError as error_message:
            print(visual_space)
            print("Your database file not exist, Please create new one.")
            main()       
                
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            main()
        
        finally:
            library:Library.save_to_picke()
    
    if database_menu_choose == "2":
        
        try:
            if os.path.isfile(DB_URL):
                raise DatabaseCreateError()
            
            print(visual_creating_database)
            library_name = input("| Please enter a Library Name: ")
            print(visual_creating_database)
            print("| Choosed Library name:", library_name, "\n")
            library_creation_address = Address.create_address_for_library()
            print(visual_creating_database)
            print(f"| Choosed Library name: {library_name}")
            print(f"| Choosed Library Address: {library_creation_address}")
            print("\nCreating database...")
            library = Library(library_name, library_creation_address)
            time.sleep(1)
            print(visual_space)
            library_created = library.save_library_to_dict(library)
            library.save_to_picke(library)
            if library_created == True:
                print("Database file is created and saved successfully")
                main()
                
        except DatabaseCreateError as error_message:
            print(visual_space)
            print("You already have a Database, You can load him or delete and create new one.")
            main()       
                
        except NegativeNumber as error_message:
            print(visual_space)
            print("You can`t use negative numbers.")
            main()            
        
        except CantBeDigit as error_message:
            print(visual_space)
            print("Address cannot be created from numbers only.")
            main()
        
        except ValueError as error_message:
            print(visual_space)
            print("You can't use letters in 'Building Number' row.")
            main()           
        
        except Exception as error_message:
            print(visual_space)
            print(error_message)
            main()
        
        finally:
            library:Library.save_to_picke()    
            
    if database_menu_choose == "3":
        
        try:
        
            if os.path.isfile(DB_URL):
                os.unlink(DB_URL)
                print(visual_space)
                print("The Library Database file is been deleted")
                main()
            
            else:
                print(visual_space)
                print("File not found.")
                main()
            
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            main()

        finally:
            library:Library.save_to_picke()
            
    if database_menu_choose == "4":
        
        try:
            if os.path.isfile(DB_URL):
                print(visual_space)
                print("Saving library database...")
                library:Library.save_to_picke()
                time.sleep(2)
                print(visual_space)
                print("The data is been saved. Bye!\n")
            else: 
                print("Bye!")
            exit()
            
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            main()
            
        finally:
            library:Library.save_to_picke()
        
        
# Library Menu
def goto_library_menu():
    try:
        print(visual_library_menu)
        print(library_menu, '\n')
        library_menu_choose = input(enter_choose)
    
        if not library_menu_choose.isdigit():
            raise NoNumbersEntered()
            
        if library_menu_choose not in ["1", "2", "3", "4", "5"]:
            raise NoUsedNumbersEntered()
            
    except NoNumbersEntered as error_message:
        print(visual_space)
        print("You can use only digits.")
        goto_library_menu()
        
    except NoUsedNumbersEntered as error_message:
        print(visual_space)
        print("You can use only displayed digits.")
        goto_library_menu()
        
    except Exception as error_message:
        print(visual_space)
        print(error_text)
        goto_library_menu()
        
    finally:
        library:Library.save_to_picke()
        
    if library_menu_choose == "1":
        print(visual_space)
        goto_customer_menu()
        
    if library_menu_choose == "2":
        print(visual_space)
        goto_book_menu()
        
    if library_menu_choose == "3":
        print(visual_space)
        goto_loan_menu()
        
    if library_menu_choose == "4":
        
        try:
            library = Library.load_from_pickle()
            print(visual_space)
            print(visual_library_settings)
            print(library_settings, '\n')
            settings_menu_choose = input(enter_choose)
            
            if not settings_menu_choose.isdigit():
                raise NoNumbersEntered()
                
            if settings_menu_choose not in ["1", "2", "3", "4"]:
                raise NoUsedNumbersEntered()
                
            if settings_menu_choose == "1":
                while True:
                    print(visual_space)
                    print(visual_library_settings)
                    library.get_library_full_information()
                    return_menu = input("\n| Enter [1] to return to the customer menu: ")
                
                    if not return_menu.isdigit():
                        continue
                
                    if return_menu != "1":
                        continue
                
                    if return_menu == "1":
                        print(visual_space)
                        goto_library_menu()       
                        
            
        except NoNumbersEntered as error_message:
            print(visual_space)
            print("You can use only digits.")
            goto_library_menu()
        
        except NoUsedNumbersEntered as error_message:
            print(visual_space)
            print("You can use only displayed digits.")
            goto_library_menu()
            
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            goto_library_menu()
            
        finally:
            library:Library.save_to_picke()
            
        if settings_menu_choose == "2":
            
            try:
                library = Library.load_from_pickle()
                print(visual_space)
                print(visual_library_settings)
                new_name = input("| Enter a new name for Library or Press [ENTER] for return: ")
                if new_name == "" or new_name == " ":
                    print(visual_space)
                    goto_library_menu()
                changed_name = library.get_library().update_library_name(new_name)

                if changed_name == True:
                    library.save_to_picke(library)
                    print(visual_space)
                    print(f"Library name changed Successful to: {new_name}")
                    goto_library_menu()
                
                if changed_name == False:
                    raise Exception()
                    
            except Exception as error_message:
                print(visual_space)
                print(error_text)
                goto_library_menu()
                
            finally:
                library:Library.save_to_picke()
                
        if settings_menu_choose == "3":
            
            try:
                library = Library.load_from_pickle()
                print(visual_space)
                print(visual_library_settings)
                new_address = Address.create_address_for_library()
                if new_address == "" or new_address == " ":
                    print(visual_space)
                    goto_library_menu()
                change = library.get_library().update_library_address(new_address)

                if change == True:
                    library.save_to_picke(library)
                    print(visual_space)
                    print(f"Library address changed Successful to: \n{new_address}")
                    goto_library_menu()
                    
            except ValueError as error_message:
                print(visual_space)
                print("You can't use letters in 'Building Number' row.")
                goto_library_menu()           
                
            except CantBeDigit as error_message:
                print(visual_space)
                print("Address cannot be created from numbers only.")    
                goto_library_menu()

            except Exception as error_message:
                print(visual_space)
                print(error_text)
                goto_library_menu()
            
            finally:
                library:Library.save_to_picke()


        if settings_menu_choose == "4":
            print(visual_space) 
            goto_library_menu()
        
    if library_menu_choose == "5":
        
        try:
            if os.path.isfile(DB_URL):
                print(visual_space)
                print("Saving library database...")
                library:Library.save_to_picke()
                time.sleep(2)
                print(visual_space)
                print("The data is been saved to your database. Bye!\n")
            
            else:
                print(visual_space)
                library:Library.save_to_picke()
                print("Your database is not exist, your data not saved!\n")
            exit()
            
        except Exception as error_message:
            print(error_message)
            main()
            
        finally:
            library:Library.save_to_picke()
    
    
    # Customer Menu
def goto_customer_menu():
    
    try:
        print(visual_customer_menu)
        print(customer_menu, '\n')
        customer_menu_choose = input(enter_choose)
        
        if not customer_menu_choose.isdigit():
            raise NoNumbersEntered()
            
        if customer_menu_choose not in ["1", "2", "3", "4", "5", "6"]:
            raise NoUsedNumbersEntered()
        
    except NoNumbersEntered as error_message:
        print(visual_space)
        print("You can use only digits.")
        goto_customer_menu()
        
    except NoUsedNumbersEntered as error_message:
        print(visual_space)
        print("You can use only displayed digits.")
        goto_customer_menu()
        
    except Exception as error_message:
        print(visual_space)
        print(error_text)
        goto_customer_menu()
        
    finally:
        library:Library.save_to_picke()
        
    if customer_menu_choose == "1":
        
        try:
            library = Library.load_from_pickle()
            customers_list = library.get_customers_dict()
            print(visual_creating_customer)
            try:
                id_of_customer = int(input("| Please enter ID of Customer: "))
                
            except ValueError as error_message:
                print(visual_space)
                print("Please use only digits when you create ID.")
                goto_customer_menu()    
                
            if id_of_customer < 0:
                raise NegativeNumber()
            
            customers_list = library.get_customers_dict()
            if id_of_customer in customers_list:
                raise UsedID()
            
            first_name_of_customer = input("| Please enter First Name of Customer: ")
            last_name_of_customer = input("| Please enter Last Name of Customer: ")
            if first_name_of_customer.isdigit() or last_name_of_customer.isdigit():
                raise Exception("Name cannot be a digit.")
            
            email_of_customer = input("| Please enter Email for Customer: ")
            print(visual_creating_customer)
            print(f"| Customer ID: {id_of_customer}")
            print(f"| Customer Full Name: {first_name_of_customer} {last_name_of_customer}")
            print(f"| Customer E-mail: {email_of_customer}\n")
            
            try:
                birthdate_of_customer = input("\n| In next format: dd.mm.yyyy.\n| Please enter Birthdate of Customer: ")
                birthdate_of_customer_datetime = datetime.datetime.strptime(birthdate_of_customer, "%d.%m.%Y")
                visualdate = datetime.date.strftime(birthdate_of_customer_datetime, "%d.%m.%Y")
                
            except ValueError as error_message:
                print(visual_space)
                print("Please enter your date in right format.")
                goto_customer_menu()    
            
            print(visual_creating_customer)
            print(f"| Customer ID: {id_of_customer}")
            print(f"| Customer Full Name: {first_name_of_customer} {last_name_of_customer}")
            print(f"| Customer E-mail: {email_of_customer}")
            print(f"| Customer Birthdate: {visualdate}\n")
            
            print("\n| Make a Address of Customer: ")
            address_of_customer = Address.create_address_for_customer()
            
            print(visual_creating_customer)
            print(f"| Customer ID: {id_of_customer}")
            print(f"| Customer Full Name: {first_name_of_customer} {last_name_of_customer}")
            print(f"| Customer E-mail: {email_of_customer}")
            print(f"| Customer Birthdate: {visualdate}")
            print(f"| Customer Address: {address_of_customer}\n\n")
            print("Creating Customer Account...")
            time.sleep(1)            
            Created = library.add_customer(id_of_customer, first_name_of_customer, last_name_of_customer, address_of_customer, email_of_customer, birthdate_of_customer)
            if Created == True:
                loan_list_for_customer = library.get_loans_for_customer()
                loan_list_for_customer[int(id_of_customer)] = []
                print(visual_space)
                print("A new Customer account is been created successfuly and saved in the DB.")
                library:Library.save_to_picke()
                goto_customer_menu()
            
        except UsedID as error_message:
            print(visual_space)
            print("This ID is already occupied by another Customer.")
            goto_customer_menu()
            
        except NegativeNumber as error_message:
            print(visual_space)
            print("ID cannot be a negative digit!")
            goto_customer_menu()

        except CantBeDigit as error_message:
            print(visual_space)
            print("Address cannot be created from numbers only.")
            goto_customer_menu()
        
        except ValueError as error_message:
            print(visual_space)
            print("You can't use letters in 'Building Number' row.")
            goto_customer_menu()    
            
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            goto_customer_menu()

    if customer_menu_choose == "2":
        
        try:
            library = Library.load_from_pickle()
            customers_list = library.get_customers_dict()
            if len(customers_list) == 0:
                print(visual_space)
                print("There are no created Customers in the database.")
                goto_customer_menu()
            print(visual_space)
            print(visual_customers_delete)
            customer:Customer = library.get_customers_dict()
            for key in customer:
                print(customer[key])
            customer_id = int(input("\n| Enter ID to delete account: "))
            loans_check = library.get_loans_for_customer()
            if len(loans_check[customer_id]) >= 1:
                raise CustomerHaveBooks()
            
            customer_deleted = library.delete_customer(customer_id)
            if customer_deleted == True:
                print(visual_space)
                print(F"Account with (ID: {customer_id}) is deleted successfully.")
                library.save_to_picke(library)
                goto_customer_menu()
            else:
                raise CustomerNotExist()
                
        except CustomerHaveBooks as error_message:
            print(visual_space)
            print("You cannot delete Customer with loaned books.")
            goto_customer_menu()
            
        except CustomerNotExist as error_message:
            print(visual_space)
            print("Customer not exist.")
            goto_customer_menu()
        
        except ValueError as error_message:
            print(visual_space)
            print("You cannot use letters.")
            goto_customer_menu()
        
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            goto_customer_menu()
            
        finally:
            library:Library.save_to_picke()
            
    if customer_menu_choose == "3":
        
        try:
            library = Library.load_from_pickle()
            customers_list = library.get_customers_dict()
            if len(customers_list) == 0:
                print(visual_space)
                print("Your Customer database is empty now.")
                goto_customer_menu()
            print(visual_space)
            print(visual_customers_full)
            customer_id = int(input("| Enter ID to get information about Customer: "))
            if customer_id not in customers_list:
                raise CustomerNotExist()
            
            print(visual_space)
            print(visual_customers_full)
            library.get_customer_full_info(customer_id)
            return_menu = input("\n| Enter [1] to return to the customer menu: ")
            if not return_menu.isdigit():
                print(visual_space)
                print("Error")
                goto_customer_menu()
            if return_menu == "1":
                print(visual_space)
                goto_customer_menu()
        
        except CustomerNotExist as error_message:
            print(visual_space)
            print("Customer not exist.")
            goto_customer_menu()        
                
        except ValueError as error_message:
            print(visual_space)
            print("You cannot use letters.")
            goto_customer_menu()
                          
        except Exception as error_message:
            print(error_message)
            goto_customer_menu()
            
        finally:
            library:Library.save_to_picke()
            
    if customer_menu_choose == "4":
        
        try:
            library = Library.load_from_pickle()
            while True:
                customers_list = library.get_customers_dict()
                if len(customers_list) == 0:
                    print(visual_space)
                    print("There are no created Customers in the database.")
                    goto_customer_menu()
                print(visual_space)
                print(visual_customers_name)
                customer_name = input("| Enter name to search customers with choosed name: ").title()
                result = library.get_customer_by_name(customer_name)
                print(visual_space)
                print(visual_customers_name)
                for i in result:
                    print(i)
                return_menu = input("\n| Enter [1] to return to the customer menu: ")
                if not return_menu.isdigit():
                    continue
                if return_menu != "1":
                    continue
                if return_menu == "1":
                    print(visual_space)
                    goto_customer_menu()       
                        
            
        except NoNumbersEntered as error_message:
            print(visual_space)
            print("You can use only digits.")
            main()
        
        except NoUsedNumbersEntered as error_message:
            print(visual_space)
            print("You can use only displayed digits.")
            main()
            
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            main()
    
        finally:
            library:Library.save_to_picke()
            
    if customer_menu_choose == "5":
        
        try:
            library = Library.load_from_pickle()
            customers_list = library.get_customers_dict()
            if len(customers_list) == 0:
                print(visual_space)
                print("There are no created Customers in the database.")
                goto_customer_menu()    
            print(visual_space)
            print(visual_customers_list)
            customer:Customer = library.get_customers_dict()
            for key in customer:
                print(customer[key])
            print("\n")
            print(customer_list, "\n")
            customer_list_choose = input(enter_choose)
            if not customer_list_choose.isdigit():
                raise NoNumbersEntered()
            
            if customer_list_choose not in ["1", "2"]:
                raise NoUsedNumbersEntered()
                
            if customer_list_choose == "1":
                print(visual_space)
                print(visual_customers_full)
                customer_id = int(input("| Enter ID to get information about Customer: "))
                if customer_id not in customers_list:
                    raise CustomerNotExist()
                
                print(visual_space)
                print(visual_customers_full)
                library.get_customer_full_info(customer_id)
                return_menu = input("\n| Enter [1] to return to the customer menu: ")
                if not return_menu.isdigit():
                    raise NoNumbersEntered()
                
                if return_menu == "1":
                    print(visual_space)
                    goto_customer_menu()
                
            if customer_list_choose == "2":
                print(visual_space)
                goto_customer_menu()
        
        except CustomerNotExist as error_message:
            print(visual_space)
            print("Customer not exist.")
            goto_customer_menu()        
                
        except NoNumbersEntered as error_message:
            print(visual_space)
            print("You can use only digits.")
            main()
        
        except NoUsedNumbersEntered as error_message:
            print(visual_space)
            print("You can use only displayed digits.")
            main()
            
        except Exception as error_message:
            print(visual_space)
            print(error_text)
            main()
    
        finally:
            library:Library.save_to_picke()

    if customer_menu_choose == "6":
        print(visual_space)
        goto_library_menu()
   
def goto_book_menu():
    print(visual_book_menu)
    print(books_menu)
    print('\n')
    books_menu_choose = input(enter_choose)     
   
    try:
        if not books_menu_choose.isdigit():
            print(visual_space)
            print("You cant use digits, Only numbers!")
            goto_book_menu()
            
        if books_menu_choose not in ["1", "2", "3", "4", "5"]:
            print(visual_space)
            print("You can use only displayed options")
            goto_book_menu()
            
    except Exception as error_message:
        print(error_message)
        goto_book_menu()    
            
    if books_menu_choose == "1":
        try:
            
            library = Library.load_from_pickle()
            book_list = library.get_book_dict()
            print(visual_creating_book)
            id_of_book = input("| Please enter ID of Book: ")
            if not id_of_book.isdigit():
                print(visual_space)
                print("Error")
                goto_book_menu()
            id_of_book = int(id_of_book)
            book_list = library.get_book_dict()
            if id_of_book in book_list:
                print(visual_space)
                print("Error, This ID is used.")
                goto_book_menu()
            print(visual_creating_book)
            print(f"| Book ID: {id_of_book}")
            name_of_book = input("| Please enter Name of Book: ")
            author_name_of_book = input("| Please enter Author name of Book: ")
            publish_year_of_book = input("| Please enter the publish year of the book: ")
            print(visual_creating_book)
            print(f"| Book ID: {id_of_book}")
            print(f"| Book Name: {name_of_book}")
            print(f"| Book Autor: {author_name_of_book}")
            print(f"| Book Publish Year: {publish_year_of_book}\n")
            
            book_type_of_book = input("\n| Book Types:\n| The book type defines the maximum loan time for the book:\
                              \n| Type 1 – up to 10 days.\n| Type 2 – up to 5 days.\n| Type 3 – up to 2 day.\n\n| Enter book type for the book: ")
            print(visual_creating_book)
            print(f"| Book ID: {id_of_book}")
            print(f"| Book Name: {name_of_book}")
            print(f"| Book Autor: {author_name_of_book}")
            print(f"| Book Publish Year: {publish_year_of_book}")
            print(f"| Book Type: {book_type_of_book}\n")

            print("Creating new book...")
            time.sleep(3)            
            library.add_book(id_of_book, name_of_book, author_name_of_book, publish_year_of_book, book_type_of_book)
            print(visual_space)
            print("Successful, New book is been created!")
            library.save_to_picke(library)
            goto_book_menu()    
            
        except Exception as error_message:
            print(error_message)
            goto_book_menu()
    
    if books_menu_choose == "2":
        try:
             
            library = Library.load_from_pickle()
            loaned_books = library.get_loaned_books()
            book_list = library.get_book_dict()
            if len(book_list) == 0:
                print(visual_space)
                print("No books to delete!")
                goto_book_menu()
            print(visual_space)
            print(visual_books_delete)
            book:Book = library.get_book_dict()
            for key in book:
                print(book[key])
            book_id = input("\n| Enter book ID to delete: ")
            if not book_id.isdigit():
                print(visual_space)
                print("Error")
                goto_book_menu()
            book_id = int(book_id)
            if book_id in loaned_books:
                print(visual_space)
                print("You cant delete a book when him loaned!")
                goto_book_menu()
            book_deleted = library.delete_book(book_id)
            if book_deleted == True:
                print(visual_space)
                print("Book Deleted!")
                library.save_to_picke(library)
                goto_book_menu()
            else:
                print(visual_space)
                print("Book not exist!")
                goto_book_menu()
        
        except Exception as error_message:
            print(error_message)
            goto_book_menu()    
        
    if books_menu_choose == "3":
        try:
            
            print(visual_space)
            print(visual_find_book)
            print(books_find)
            print("\n")
            book_find_choose = input(enter_choose)
        
            if not book_find_choose.isdigit():
                print(visual_space)
                print("You cant use digits, Only numbers!")
                goto_book_menu()
            
            if book_find_choose not in ["1", "2", "3", "4"]:
                print(visual_space)
                print("You can use only displayed options")
                goto_book_menu()
        
            if book_find_choose == "1":
        
                library = Library.load_from_pickle()
                books_list = library.get_book_dict()
                if len(books_list) == 0:
                    print(visual_space)
                    print("No Books for display!")
                    goto_book_menu()
                print(visual_space)
                print(visual_books_full)
                book_id = input("| Enter ID to get information about the book: ")
                if not book_id.isdigit():
                    print(visual_space)
                    print("Error")
                    goto_book_menu()
                book_id = int(book_id)
                if book_id not in books_list:
                    print(visual_space)
                    print("Error, ID not exist.")
                    goto_book_menu()
                print(visual_space)
                print(visual_books_full)
                library.get_book_full_info(book_id)
                return_menu = input("\n| Enter [1] to return to the book menu: ")
                if not return_menu.isdigit():
                    print(visual_space)
                    print("Error")
                    goto_book_menu()
                if return_menu == "1":
                    print(visual_space)
                    goto_book_menu()
                    
            if book_find_choose == "2":
                
                    print(visual_space)
                    print(visual_find_book)
                    print("\n")
                    book_name_choose = input(enter_choose)
                    
                    library = Library.load_from_pickle()
                    books_list = library.get_book_dict()
                    if len(books_list) == 0:
                        print(visual_space)
                        print("No Books for display!")
                        goto_book_menu()
                    print(visual_space)
                    print(visual_find_book)
                    result = library.get_book_by_name(book_name_choose)
                    for i in result:
                        print(i)
                    return_menu = input("\n| Enter [1] to return to the book menu: ")
                    if not return_menu.isdigit():
                        print(visual_space)
                        print("Error")
                        goto_book_menu()
                    if return_menu == "1":
                        print(visual_space)
                        goto_book_menu()

                
            if book_find_choose == "3":
                print(visual_space)
                print(visual_find_book)
                print("\n")
                book_author_choose = input(enter_choose)
                    
                library = Library.load_from_pickle()
                books_list = library.get_book_dict()
                if len(books_list) == 0:
                    print(visual_space)
                    print("No Books for display!")
                    goto_book_menu()
                print(visual_space)
                print(visual_find_book)
                result = library.get_book_by_author(book_author_choose)
                for i in result:
                    print(i)
                return_menu = input("\n| Enter [1] to return to the book menu: ")
                if not return_menu.isdigit():
                    print(visual_space)
                    print("Error")
                    goto_book_menu()
                if return_menu == "1":
                    print(visual_space)
                    goto_book_menu()
                
                
            if book_find_choose == "4":
                print(visual_space)
                goto_book_menu()
                
        except Exception as error_message:
            print(error_message)
            goto_book_menu()
        
    if books_menu_choose == "4":
        try:
        
            library = Library.load_from_pickle()
            book_list = library.get_book_dict()
            if len(book_list) == 0:
                print(visual_space)
                print("No Books for display!")
                goto_book_menu()
            print(visual_space)
            print(visual_books_list)
            book:Book = library.get_book_dict()
            for key in book:
                print(book[key])
            print("\n")
            print(books_list_menu, "\n")
            books_list_choose = input(enter_choose)
            if not books_list_choose.isdigit():
                print(visual_space)
                print("You cant use digits, Only numbers!")
                goto_book_menu()
            
            if books_list_choose not in ["1", "2"]:
                print(visual_space)
                print("You can use only displayed options")
                goto_book_menu()
                
            if books_list_choose == "1":
                print(visual_space)
                print(visual_books_full)
                book_id = input("| Enter ID to get information about the Book: ")
                if not book_id.isdigit():
                    print(visual_space)
                    print("Error")
                    goto_book_menu()
                book_id = int(book_id)
                if book_id not in book_list:
                    print(visual_space)
                    print("Error, ID not exist.")
                    goto_book_menu()
                print(visual_space)
                print(visual_books_full)
                library.get_book_full_info(book_id)
                return_menu = input("\n| Enter [1] to return to the books menu: ")
                if not return_menu.isdigit():
                    print(visual_space)
                    print("Error")
                    goto_book_menu()
                if return_menu == "1":
                    print(visual_space)
                    goto_book_menu()
                    
            if books_list_choose == "2":
                print(visual_space)
                goto_book_menu()           
        
        except Exception as error_message:
            print(error_message)
            goto_book_menu()
            
    if books_menu_choose == "5":
        print(visual_space)
        goto_library_menu()
        
def goto_loan_menu():
    try:
        print(visual_loan_menu)
        print(loan_menu)
        print('\n')
        loan_menu_choose = input(enter_choose)
    
        if not loan_menu_choose.isdigit():
            print(visual_space)
            print("You cant use digits, Only numbers!")
            goto_loan_menu()
            
        if loan_menu_choose not in ["1", "2", "3", "4"]:
            print(visual_space)
            print("You can use only displayed options")
            goto_loan_menu()
            
    except Exception as error_message:
        print(error_message)
        goto_loan_menu()    
            
    if loan_menu_choose == "1":
        try:
            
            library = Library.load_from_pickle()
            loan_book:list = library.get_loaned_books()
            print(visual_space)
            print(visual_creating_loan)
            
            customer_id = input("| Please enter Customer ID: ")
            customer = library.get_customer_by_id(int(customer_id))
            loaned_customers = library.get_loans_for_customer()
            if len(loaned_customers[int(customer_id)]) >= 3:
                print(visual_space)
                print("You cant take more books!")
                goto_loan_menu()
            print(visual_space)
            print(visual_creating_loan)
            print(f"| Choosed Customer:", customer.get_customer_half_info(),"\n")
            book_id = input("| Please enter Book ID: ")
            book = library.get_book_by_id(int(book_id))
            if int(book_id) in loan_book:
                print(visual_space)
                print("This book loaned now!")
                goto_loan_menu()
            print(visual_space)
            print(visual_creating_loan)
            print(f"| Choosed Customer:", customer.get_customer_half_info())
            print(f"| Choosed Book:", book.get_book_info())
            loan_date = datetime.date.today()
            print(f"| Loan Date:", datetime.date.strftime(loan_date, "%d.%m.%Y"))
            return_date = None
            if book.get_book_type() == "1":
                return_date = loan_date + datetime.timedelta(days=10)
            if book.get_book_type() == "2":
                return_date = loan_date + datetime.timedelta(days=5)
            if book.get_book_type() == "3":
                return_date = loan_date + datetime.timedelta(days=2)
            print(f"| Return Date:", datetime.date.strftime(return_date, "%d.%m.%Y"))
            loan_status = "Waiting for confirm"
            print(f"| Loan Status: {loan_status}")
            make_loan_choose = input(f"\n| Confirm new loan? [Y/N]: ")
            if make_loan_choose == "N" or make_loan_choose == "n":
                print(visual_space)
                print("Loan is been canceled!")
                goto_loan_menu()
            if make_loan_choose == "Y" or make_loan_choose == "y":
                print(visual_space)
                print(visual_creating_loan)
                loan_status = "Confirmed"
                print(f"| Choosed Customer:", customer.get_customer_half_info())
                print(f"| Choosed Book:", book.get_book_info())
                print(f"| Loan Date:", datetime.date.strftime(loan_date, "%d.%m.%Y"))
                print(f"| Return Date:", datetime.date.strftime(return_date, "%d.%m.%Y"))
                print(f"| Loan Status: {loan_status}\n")
                print("| The loan is confirmed, Returning to Loan Menu....")
                time.sleep(3)
                loan_status = "Loaned"
                library.create_loan_book(customer_id, book_id, return_date, loan_date, loan_status)
                loan_customer = library.get_loans_for_customer()
                loan_customer[int(customer_id)].append(int(book_id))
                loan_book.append(int(book_id))
                library.save_to_picke(library)
                print(visual_space)
                print("Loan is been confirmed!")
                goto_loan_menu()
                
        except Exception as error_message:
            print(error_message)
            goto_loan_menu()
        
    if loan_menu_choose == "2":
        try:
            
            print(visual_space)
            print(visual_return_loans)
            library = Library.load_from_pickle()
            loan_book:list = library.get_loaned_books()
            loan_customer:dict = library.get_loans_for_customer()
            return_book_id = input("| Please enter Book ID to return: ")
            if not return_book_id.isdigit():
                print(visual_space)
                print("Enter only numbers!")
                goto_loan_menu()
            else:
                return_book_id = int(return_book_id)
                if return_book_id not in loan_book:
                    print(visual_space)
                    print("This book not loaned!")
                    goto_loan_menu()
                else:
                    library.delete_loan(int(return_book_id))
                    print(visual_space)
                    print("The book is returned.")
                    library.save_to_picke(library)
                    goto_loan_menu()

    
        except Exception as error_message:
            print(error_message)
            goto_loan_menu()
            
    if loan_menu_choose == "3":
        try:
            
            print(visual_space)
            print(visual_display_loans)
            library = Library.load_from_pickle()
            library.get_loan_logs()
            print("\n")
            print(display_loan_menu, "\n")
            display_loans_choose = input(enter_choose)
            
            if display_loans_choose == "1":
                print(visual_space)
                print(visual_display_loans)
                library.get_late_loan_logs()
                print("\n")
                return_menu = input("\n| Enter [1] to return to the customer menu: ")
                if not return_menu.isdigit():
                    print(visual_space)
                    print("Error")
                    goto_loan_menu()
                if return_menu == "1":
                    print(visual_space)
                    goto_loan_menu()
            
            if display_loans_choose == "2":
                print(visual_space)
                goto_loan_menu()
                
        except Exception as error_message:
            print(error_message)
            goto_loan_menu()
                
    if loan_menu_choose == "4":
        print(visual_space)
        goto_library_menu()
            
if __name__ == "__main__":
    print(visual_space) 
    main()