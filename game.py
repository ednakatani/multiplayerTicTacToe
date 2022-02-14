from os import system, name
import menumaker
import random
import socket
from colors import bcolors


PLAYER = 1           
PORT = 6589
host = '127.0.0.1'

turn = 1 # 1 - Player 1 | 2 - Player 2
moves = 0
p_char = f"{bcolors.OKGREEN}X{bcolors.ENDC}"
c_char = f"{bcolors.FAIL}O{bcolors.ENDC}"
table = ['1','2','3',
         '4','5','6',
         '7','8','9']


def cls():
    """
    Clear the screen
    """
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def winner():
    """
    Check if anyone has won
    Returning char or bool
    """

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
    return False

def tie():
    """
    Check if the game is tied
    """
    global moves
    if moves >= 9:
        return True
    else:
        return False

def win_game():
    """
    Check if anyone has won
    Returning only bool
    """
    global p_char
    global c_char
    if winner() in [p_char,c_char]: 
        return True
    else:
        return False
    
def view():
    """
    Print the game board
    """
    global table
    global moves

    print("\n  %s │ %s │ %s " % (table[0],table[1],table[2]))
    print("────┼───┼───")
    print("  %s │ %s │ %s " % (table[3],table[4],table[5]))
    print("────┼───┼───")
    print("  %s │ %s │ %s \n" % (table[6],table[7],table[8]))

def move(pos):
    """
    Changes the value of the char in the game list
    """
    global turn
    global table
    global p_char
    global c_char
    global moves
    
    if not pos: return False
    if not 0 < pos < 10: return False
    if table[pos-1] in [p_char,c_char]: return False

    moves += 1
    table[pos-1] = (c_char,p_char)[turn == 1]
    turn = (1,2)[turn == 1]
    return True

def send(conn: socket, data: str):
    """
    Send data thru a socket 
    """
    conn.send(str(data).encode())

def recive(conn: socket):
    """
    Wait and recieves data of a socket
    """
    msg = conn.recv(1024)
    return msg.decode()

def rand():
    """
    Generate a random number (1 or 2)
    """
    return random.randint(1,2)

def reset():
    """
    Reset the table and moves variables
    """
    global table
    global moves
    moves = 0
    table = ['1','2','3',
         '4','5','6',
         '7','8','9']

def run_host():

    reset()

    start = rand()

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    orig = (socket.gethostbyname(socket.gethostname()), PORT)
    tcp.bind(orig)
    tcp.listen(1)

    print("IP:",socket.gethostbyname(socket.gethostname()))
    print("PORT:", PORT)
    print ("Waiting Client ...")
    
    con, cliente = tcp.accept()
    
    #print ('Concetado por', cliente)

    while not win_game() and not tie():
        
        cls()
        print("win >",win_game(), "tie >", tie())
        print("moves >",moves)
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
        

    con.close()

    win = winner()
    if win == p_char:
        print ("Player 1 Wins!")
    elif win == c_char:
        print ("Player 2 Wins!")
    else:
        print("It's a tie!")

    
def run_client():

    reset()

    print("HOST IP")
    host = input("> ")

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (host, PORT)
    tcp.connect(dest)

    while not win_game() and not tie():
        
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


    tcp.close()

    win = winner()
    if win == p_char:
        print ("Player 1 Wins!")
    elif win == c_char:
        print ("Player 2 Wins!")
    else:
        print("It's a tie!")




menu = menumaker.Menu("TIC-TAC-TOE", True,[["Host",run_host],["Client",run_client]])

menu.menu()