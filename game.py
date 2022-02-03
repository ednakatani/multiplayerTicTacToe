from os import system, name
import menumaker
import random
import socket
from colors import bcolors


PLAYER = 1           
PORT = 6589
host = '127.0.0.1'

turn = 1 # 1 - Player 1 | 2 - Player 2
p_char = f"{bcolors.OKGREEN}X{bcolors.ENDC}"
c_char = f"{bcolors.FAIL}O{bcolors.ENDC}"
table = ['1','2','3',
         '4','5','6',
         '7','8','9']


def cls():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def winner():
    global table
    global p_char
    global c_char
    for i in [p_char,c_char]:
        # horizontal
        if table[0] == table[1] == table[2] == i: return i
        if table[3] == table[4] == table[5] == i: return i
        if table[6] == table[7] == table[8] == i: return i
        # vertical
        if table[0] == table[3] == table[6] == i: return i
        if table[1] == table[4] == table[7] == i: return i
        if table[2] == table[5] == table[8] == i: return i
        # diagonal
        if table[0] == table[4] == table[8] == i: return i
        if table[6] == table[4] == table[2] == i: return i
    return None

def view():
    global table

    
    
    print("\n  %s │ %s │ %s " % (table[0],table[1],table[2]))
    print("────┼───┼───")
    print("  %s │ %s │ %s " % (table[3],table[4],table[5]))
    print("────┼───┼───")
    print("  %s │ %s │ %s \n" % (table[6],table[7],table[8]))

def move(pos):
    global turn
    global table
    global p_char
    global c_char
    
    if not pos: return None
    if not 0 < pos < 10: return False
    if table[pos-1] in [p_char,c_char]: return False

    table[pos-1] = (c_char,p_char)[turn == 1]
    turn = (1,2)[turn == 1]

def send(conn: socket, data: str):
    conn.send(str(data).encode())

def recive(conn: socket):
    msg = conn.recv(1024)
    return msg.decode()

def rand():
    return random.randint(1,2)

def run_host():

    start = rand()

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    orig = (host, PORT)
    tcp.bind(orig)
    tcp.listen(1)

    print("IP:",socket.gethostbyname(socket.gethostname()))
    print("PORT:", PORT)
    print ("Waiting Client ...")
    
    con, cliente = tcp.accept()
    
    #print ('Concetado por', cliente)

    while not winner():
        
        cls()
        view()

        if  start == 2:
            send(con, "10")
            start = 0

        else:
            print ("Your turn")
            movement = int(input("> "))
            move(movement)
            send(con, movement)

        cls()
        view()

        print ("Waiting...")

        msg = recive(con)

        move(int(msg))
        
        #print (cliente, msg)

    #print ('Finalizando conexao do cliente', cliente)

    con.close()

    win = winner()
    if win == p_char:
        print ("Player 1 Wins!")

    if win == c_char:
        print ("Player 2 Wins!")

    
def run_client():

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (host, PORT)
    tcp.connect(dest)

    while not winner():
        
        cls()
        view()

        print ("Waiting...")

        msg = recive(tcp)

        move(int(msg))

        cls()
        view()

        print ("Your turn")
        movement = int(input("> "))
        move(movement)
        send(tcp, movement)

    #print ('Finalizando conexao do cliente', cliente)

    tcp.close()

    win = winner()
    if win == p_char:
        print ("Player 1 Wins!")

    if win == c_char:
        print ("Player 2 Wins!")




menu = menumaker.Menu("TIC-TAC-TOE", True,[["Host",run_host],["Client",run_client]])

menu.menu()