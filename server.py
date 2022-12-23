import socket
import sqlite3
from struct import pack
from _thread import start_new_thread



def threaded(conn):
    while True:
        # receive data stream.
        data = conn.recv(4096).decode()
        if not data:
            # if data is not received break
            break

        data = data.split(';')
        if data[0] == "1":
            result = send_monsters(data[1], data[2], data[3])
            conn.send((';'.join(result)).encode())


    conn.close()  # close the connection

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    start_new_thread(threaded, (conn,))




def send_monsters(players, levels, complexity):
    con = sqlite3.connect('players.db')
    players = [int(i) for i in players.split(",")]
    levels = [int(i) for i in levels.split(",")]
    complexity = int(complexity)
    monsters_score = [25, 50, 100, 200, 450, 700, 1100, 1800, 2300, 2900,
                      3900, 5000, 5900, 7200, 8400, 10000, 11500, 13000, 15000, 18000,
                      20000, 22000, 25000, 33000, 41000, 50000, 62000, 75000, 90000, 105000,
                      120000, 135000, 155000]
    cur = con.cursor()
    all_count = 0
    result = []
    k = [1, 1.5, 2, 2, 2, 2, 2.5, 2.5, 2.5, 2.5, 2.5, 3, 3, 3, 3, 4]
    for i in range(len(levels)):
        sql_select = """SELECT * FROM players WHERE level = ?"""
        cur.execute(sql_select, (levels[i],))
        rec = cur.fetchall()

        all_count += rec[0][complexity] * players[i]
        print(rec[0][complexity])
    for i in range(len(monsters_score)-1, 0, -1):
        j = 0
        monster = monsters_score[i]
        if monsters_score[i] <= all_count:
            while monster*k[j] < all_count and j < 14:
                monster += monster
                j += 1
            result.append(f"{monsters_score[i]},{k[j]}")
    return result



if __name__ == "__main__":
    while True:
        server_program()

