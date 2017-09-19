import http.client
import sys
import urllib.request, urllib.parse, urllib.error
#import urllib.parse
#from urllib import urllib.parse
import sys
import array
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
########Globals
#port parameter on which client can connect
port = None
#file w/ setup of your board
board = None
oboard = None

#number of hits each ship has recieved
chit = 0
bhit = 0
rhit = 0
shit = 0
dhit = 0
FAILURE = "\033[1;31;40m"
DEF_C = "\033[0;37;40m"
class Server(BaseHTTPRequestHandler):

    #when fire: send message to other server, get response back, update own board based on that info


    def do_GET(self):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(board, "utf8"))

    def do_POST(self):
        coor = urllib.parse.parse_qs(self.path)
        xCoord = int(coor['x'][0])
        yCoord = int(coor['y'][0])
        returnMessage = checkInput(xCoord, yCoord)
        self.send_response(returnMessage[0])
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(returnMessage[1].encode())







def checkInput(x, y):
    if x < 0 | x > 9 | y < 0 | y > 9:
        return [404, "HTTP Not Found"]
    elif ((oboard[x][y] == 'X') | (oboard[x][y] == '.')):
        return [410, "HTTP Gone"]
    else:
        return checkBoard(x, y)


def checkBoard(x, y):
    cell = oboard[x][y]
    if cell == 'C':
        chit = chit +1
        oboard[x][y] = 'X'
        if chit == 5:
            message = "hit=1&sink=C"
            code = 200
            #carrier sunk
        else:
            message = "hit=1"
            code = 200
            #carrier hit
    elif cell == 'B':
        bhit = bhit +1
        oboard[x][y] = 'X'
        if bhit == 4:
            message = "hit=1&sink=B"
            code = 200
            #battleship sunk
        else:
            message = "hit=1"
            code = 200
            #battleship hit
    elif cell == 'R':
        rhit = rhit +1
        oboard[x][y] = 'X'
        if rhit == 3:
            message = "hit=1&sink=R"
            code = 200
            #cruiser sunk
        else:
            message = "hit=1"
            code = 200
            #cruiser hit
    elif cell == 'S':
        shit = shit +1
        oboard[x][y] = 'X'
        if shit == 3:
            message = "hit=1&sink=S"
            code = 200
            #sub sunk
        else:
            message = "hit=1"
            code = 200
            #sub hit
    elif cell == 'D':
        dhit = dhit +1
        oboard[x][y] = 'X'
        if dhit == 2:
            message = "hit=1&sink=D"
            code = 200
            #destroyer sunk
        else:
            message = "hit=1"
            code = 200
            #destroyer hit
    else:
        oboard[x][y] = '.'
        message = "hit=0"
        code = 200
    return [code, message]
        #missed

def show_board(which_board):
    g = open(which_board, 'r')
    b = g.read()
    message = b
    return message

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print((FAILURE + 'incorrect number of arguments!' + DEF_C))
        sys.exit(1)
    port = sys.argv[1]
    board = sys.argv[2]
    oboard = []
    f = open(board, 'r')
    for line in f:
        oboard.append(list(line))
    server = HTTPServer(('', int(port)), Server)
    server.serve_forever()
