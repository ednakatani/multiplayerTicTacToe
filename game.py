#!/usr/bin/python
from os import system, name
import platform
import menumaker
import socket
from colors import bcolors

player = 1
turn = 1 # 1 - Player 1 | 2 - Player 2
clean = ('clear','cls')[platform.system() == 'Windows']
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
    
    print("  %s │ %s │ %s " % (table[0],table[1],table[2]))
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


def host():
    return 0

def client():

    while True:
        cls()
        view()

        print ("Player %s: " % turn)
        movement = int(input())
        move(movement)

        win = winner()
        if not win: continue
        if win == p_char:
            print ("Player 1 Wins!")
            input()
            exit()
        if win == c_char:
            print ("Player 2 Wins!")
            input()
            exit()

menu = menumaker.Menu("TIC-TAC-TOE", True,[["Host",host],["Client",client]])

menu.menu()