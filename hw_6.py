from collections import UserDict

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_contact(self, record):
        self.data[record.name.value] = record

    def remove_contact(self, name):
        if name in self.data:
            del self.data[name]
    
    def change_contact_name(self, name):
        if name in self.data:
            record = self.data.pop(name)
            new_name = input("Enter new name for the contact: ")
            record.name.value = new_name
            self.data[new_name] = record

    def change_contact_phone(self, name):
        if name in self.data:
            record = self.data[name]
            old_phone_number = input("Enter the old phone number: ")
            new_phone_number = input("Enter the new phone number: ")
            record.edit_phone(old_phone_number, new_phone_number)
            print("Phone number changed.")

    def show_phone(self, name):
        if name in self.data:
            print(self.data[name])

    def get_contact(self, name):
        return self.data.get(name)

    def get_all_contacts(self):
        return self.data.values()
    
# Клас, що представляє базове поле (значення)
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас, який наслідується від базового поля для збереження імені
class Name(Field):
    pass

# Клас, який наслідується від базового поля для збереження номера телефону з валідацією
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)

# Клас, що представляє запис у книзі контактів
class Record:
    def __init__(self, name, phone_number):
        self.name = Name(name)  # Записуємо ім'я як об'єкт класу Name
        self.phones = [Phone(phone_number)]  # Список для збереження номерів телефонів

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))  # Додаємо новий номер телефону

    def remove_phone(self, phone_number):
        # Видаляємо номер телефону зі списку
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        # Редагуємо номер телефону у списку
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break

    def find_phone(self, phone_number):
        # Пошук номера телефону у записі
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        # Перевизначений метод для зручного виводу інформації про запис
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

    

def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    Обробляє винятки KeyError, ValueError, IndexError.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            print(f"Error: {e}")
            return None
    return wrapper    

@input_error
# Функція для додавання контакту
def add_contact(address_book):
    name = input("Enter contact name: ")
    phone_number = input("Enter contact phone number: ")
    record = Record(name, phone_number)
    address_book.add_contact(record)
    print("Contact added.")

@input_error
# Функція для видалення контакту
def remove_contact(address_book):
    name = input("Enter the name of the contact you want to remove: ")
    address_book.remove_contact(name)
    print("Contact removed.")

@input_error
# Функція для зміни імені контакту
def change_contact_name(address_book):
    name = input("Enter the name of the contact you want to change: ")
    address_book.change_contact_name(name)
    print("Contact name changed.")

@input_error
# Функція для зміни номеру телефону контакту
def change_contact_phone(address_book):
    name = input("Enter the name of the contact whose phone number you want to change: ")
    address_book.change_contact_phone(name)
    print("Phone number changed.")

@input_error
# Функція для відображення конкретного контакту
def show_phone(address_book):
    name = input("Enter the name of the contact you want to show: ")
    address_book.show_phone(name)

@input_error
# Функція для відображення всіх контактів
def show_all_contacts(address_book):
    print("All contacts:")
    for record in address_book.get_all_contacts():
        print(record)


def parse_input(command):
    """
    Функція для розбору введеної команди.
    """
    parts = command.split()
    if len(parts) < 1:
        return None, []
    return parts[0].lower(), parts[1:]


def main():
    print("Welcome to the assistant bot!")
    address_book = AddressBook()

    while True:
        command = input("Enter command: ")
        action, args = parse_input(command)
        if action == "exit" or command == "close":
            print("Good bye!")
            break
        elif action == "hello":
            print("How can I help you?")
        elif action == "add":
            add_contact(address_book)
        elif action == "remove":
            remove_contact(address_book)
        elif action == "change_name":
            change_contact_name(address_book)
        elif action == "change_phone":
            change_contact_phone(address_book)
        elif action == "show":
            show_phone(address_book)
        elif action == "all":
            show_all_contacts(address_book)
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
