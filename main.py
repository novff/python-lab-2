from datetime import datetime
from tabulate import tabulate

class item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_name(self):
        return self.name
    def set_name(self, new_name):
        self.name = new_name

    def get_price(self):
        return self.price
    def set_price(self, new_price):
        self.price = new_price

    def get_quantity(self):
        return self.quantity
    def set_quantity(self, new_quantity):
        self.quantity = new_quantity
    def add_quantity(self, quantity):
        self.quantity += quantity

class user:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.action_history = []
    def get_name(self):
        return self.name
    def change_password(self, old_password, new_password):
        self.action_history.append({"change_password": datetime.now()})
        if self.password == old_password:
            self.password = new_password
        else:
            print("неправильный старый пароль.")
    def list_items(self):
        self.action_history.append({"list_items": datetime.now()})
        table = [["наименование","количество","цена"]]
        for i in items:
            table.append([i.get_name(), i.get_quantity(), i.get_price()])
        print(tabulate(table))
    def take_item(self, n):
        self.action_history.append({"take_item " + n: datetime.now()})
        for i in items:
            if i.get_name() == n:
                i.add_quantity(-1)
                return

            
    def list_analytics(self):
        self.action_history.append({"list_analytics": datetime.now()})
        print(tabulate(self.action_history))
    
            
class admin:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.action_history = []
    def get_name(self):
        return self.name
    def change_password(self, old_password, new_password):
        self.action_history.append({"change_password": datetime.now()})
        if self.password == old_password:
            self.password = new_password
        else:
            print("неправильный старый пароль.")
    def add_item(self, n, p, q):
        self.action_history.append({"add_item": datetime.now()})
        #if item exists combine quantities else append
        for i in items:
            if i.get_name() == n:
                i.add_quantity(q)
                return
        items.append(item(n,p,q))        
    def remove_item(self, n):
        self.action_history.append({"remove_item": datetime.now()})
        #find item with name n and remove item from list
        for i in items:
            if i.get_name() == n:
                items.pop(items.index(i))
                return    
    def edit_item(self, n, new_name, new_quantity, new_price):
        self.action_history.append({"edit_item": datetime.now()})
        for i in items:
            if i.get_name() == n:
                i.set_name(new_name)
                i.set_quantity(new_quantity)
                i.set_price(new_price)
                return        
    def list_items(self):
        self.action_history.append({"list_items": datetime.now()})
        header = ["наименование","количество","цена"]
        table = []
        for i in items:
            table.append([i.get_name(), i.get_quantity(), i.get_price()])
        print(tabulate(table, headers=header))
        
        
    def list_analytics(self, user):
        self.action_history.append({"list_analytics": datetime.now()})
        print(tabulate(user.action_history))


        
items = [
    item("шапка деда мороза", 350, 3),
    item("гирлянды", 1300, 12),
    item("шарики", 2400, 1),
]
users = [
    admin("adm", "passwd"),
    user("usr", "passwd")
]

def adminPanel(u):
    print("добро пожаловать в админскую панель" )
    T = True
    while T:
        inp = int(input("выберите действие:\n1)добавить предмет на склад\n2)удалить предмет со склада\n3) редактировать предмет со склада\n4)смотреть историю пользователя\n5)список предметов\n6)создать новую учетку\n0)выйти из аккаунта\n"))
        match inp:
            case 0:
                T = not T
            case 1:
                a = input("введите название нового предмета: ")
                b = int(input("введите количество нового предмета: "))
                c = int(input("введите стоимость нового предмета: "))
                u.add_item(a, b, c)
            case 2:
                a = input("введите название удаляемого предмета: ")
                u.remove_item(a)
            case 3:
                a = input("введите название редактируемого предмета: ")
                for i in items:
                    if i.get_name() == a:
                        b = input("введите новое название предмета или оставьте поле пустым: ").strip() or i.get_name()
                        c = int(input("введите новое количество предмета или оставьте поле пустым: ").strip() or i.get_quantity())
                        d = int(input("введите новую стоимость предмета или оставьте поле пустым: ").strip() or i.get_price())
                        u.edit_item(a, b, c, d)
                    else:
                        print("ошибка, предмета с данным названием не существует")     
            case 4:
                a = input("введите имя пользователя: ")
                for e in users:
                    if e.get_name() == a:
                        print(tabulate([u.action_history]))
                        break
            case 5:
                u.list_items()
            case 6:
                a = int(input("выберите тип учетной записи:\n1)пользователь\n2)админ"))
                if a == 1 or a == 2:
                    login = input("введите логин: ")
                    login_exists = False
                    for e in users:
                        if e.get_name() == login:
                            login_exists = True
                    if login_exists:
                        print("ошибка пользователь существует.")
                    else:
                        passwd = input("введите пароль: ")
                        if a == 1:
                            users.append(user(login, passwd))
                        else:
                            users.append(admin(login, passwd))
                else:
                    print("выбранного типа не существует")
            case _:
                print("действия не существует.")

def userPanel(u):
    print("добро пожаловать в пользовательскую панель" )
    T = True
    while T:
        inp = int(input("выберите действие:\n1)сменить пароль\n2)список товаров\n4)забрать товар\n0)выйти из аккаунта\n"))
        match inp:
            case 0:
                T = not T
            case 1:
                a = input("введите старый пароль:")
                b = input("введите новый пароль:")
                u.change_password(a, b)
            case 2:
                u.list_items()
            case 3:
                u.list_analytics()
            case 4:
                a = input("введите название товара: ")

                u.take_item(a)


            case _:
                print("действия не существует.")


def main():
    while True:
        login = input("введите логин: ")
        passwd = input("введите пароль: ")
        for u in users:
            if u.name == login and u.password == passwd:
                if u.__class__.__name__ == "admin":
                    adminPanel(u)  
                else:
                    userPanel(u)

main()