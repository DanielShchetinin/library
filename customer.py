import datetime
from address import Address


class Customer:
    
    def __init__(self, customer_id: int, customer_first_name: str, customer_last_name: str, address: Address, email: str, birth_date: datetime):
        
        self._customer_id = customer_id
        self._customer_first_name = customer_first_name
        self._customer_last_name = customer_last_name
        self._address: Address = address
        self._email = email
        self._birth_date = birth_date
        
    def get_customer_id(self):
        return self._customer_id
    
    def get_customer_full_name(self):
        return f"{self._customer_first_name} {self._customer_last_name}"
    
    def get_customer_half_info(self):
        return f"[{self._customer_id}] {self._customer_first_name} {self._customer_last_name}"
    
    def get_customer_address(self):
        return self._address
    
    def get_customer_email(self):
        return self._email
 
    def get_customer_age(self):
        today = datetime.datetime.today()
        customer = self._birth_date
        formating = datetime.datetime.strptime(customer, "%d.%m.%Y")
        age = today.year - formating.year - ((today.month, today.day) < (formating.month, formating.day))
        return age

    def __str__(self):
        return f"[{self._customer_id}] {self.get_customer_full_name()}, {self.get_customer_age()}, {self.get_customer_address().get_city()}."
    
    def __repr__(self):
        return self.__str__()
    
if __name__ == "__main__":
    pass