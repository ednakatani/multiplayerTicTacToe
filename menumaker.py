from os import system, name
  
def cls():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


class Menu:
    
    def __init__(self, title: str, clear: bool, items: list):
        '''
        Title → string\n
        Clear → True for clearing screen before every menu print\n
        Items → list [ ["Item", function_name], ... ]
        
        '''
        self.clear = clear
        self.title = title
        self.items = items


    def add(self, item):
        self.items.append(item)

    
    def add(self, name, function):
        item = [name,function]
        self.items.append(item)


    def print(self):
        size = len(self.title)
        star = "*" * size * 3
        n_items = len(self.items)
        
        print(star)
        print("*".ljust(int(len(star) / 3)) + self.title + "".ljust(int(len(star) / 3) - 1) + "*")
        print(star)
        print()
        for item in range(n_items):
            print('[' + str(item) + '] - ' + self.items[item][0])
        print("[" + str(n_items) + "] - Sair")


    def get_op(self):
        self.print()
        op = input("> ")
        op = int(op)

        return op


    def menu(self):
        show = True
        while show:
            
            if self.clear:
                cls()

            op = self.get_op()
            if op == len(self.items):
                break
            if self.clear:
                cls()

            self.items[op][1]()
            input("ENTER for return")
