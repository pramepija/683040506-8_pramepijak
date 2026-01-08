
from datetime import datetime

class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self._id = item_id
        self._checked_out = False
    
    def get_status(self):
        return "Checked out" if self._checked_out else "Available"
    
    def check_out(self):
        
        if not self._checked_out:
            self._checked_out = True
            return True
        
        return False
    
    def return_item(self):
        if not self._checked_out:
            self._checked_out = True
            return True
        return False

    def display_info(self):
        
        print(f"Title : {self.title}")
        print(f"ID : {self._id}")
        print(f"Status : {self.get_status()}")
        


class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0
    
    def set_pages_count(self, pages):
        self.pages_count = pages

    def display_info(self):
        if self.check_out():
            status = "Checked Out"
        else:
            status = "Avaliable"
        
        print(f"Title : {self.title}")
        print(f"Author : {self.author}")
        print(f"Page count : {self.pages_count}")
        print(f"Status : {status}")


class TextBook(Book):
    def __init__(self, title, item_id, author, subject ,grade):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade

    def display_info(self):
        print(f"Item : {self.title}")
        print(f"ID : {self._id}")
        print(f"Author : {self.author}")
        print(f"Pages : {self.pages_count}")
        print(f"Subject : {self.subject}")
        print(f"Grade Level : {self.grade_level}")
        print(f"Status : {self.get_status()}")

class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue_number):
        super().__init__(title, item_id)
        self.issue_number = issue_number
    

        now = datetime.now()
        self.month = now.month
        self.year = now.year

    def display_info(self):
        print(f"Item : {self.title}")
        print(f"ID : {self._id}")
        print(f"Issue : {self.issue_number}")
        print(f"Month : {self.month}")
        print(f"year : {self.year}")
        print(f"Status : {self.get_status()}")



book = Book("Harry Potter", "B001", "J.K. Rowling")
book.set_pages_count(350)

textbook = TextBook("Physics", "T101", "Serway", "Science", 12)
textbook.set_pages_count(500)

mag = Magazine("Time", "M202", 45)
mag.check_out()
mag.return_item()
book.check_out()
textbook.check_out()

book.display_info()
print()
textbook.display_info()
print()
mag.display_info()