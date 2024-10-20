import socket
import argparse

TWITCH_IRC_SERVER = 'irc.chat.twitch.tv'
TWITCH_IRC_PORT = 6667

def parse_arguments():
    parser = argparse.ArgumentParser(description="Connect to a Twitch channel and track user joins/leaves.")
    parser.add_argument('channel', type=str, help='The name of the Twitch channel to connect to')
    return parser.parse_args()

def connect_to_twitch(channel):
    irc_socket = socket.socket()
    irc_socket.connect((TWITCH_IRC_SERVER, TWITCH_IRC_PORT))
    nickname = f'justinfan11123'
    irc_socket.send(f"CAP REQ :twitch.tv/membership\r\n".encode('utf-8'))
    irc_socket.send(f"PASS oauth:anonymous\r\n".encode('utf-8'))
    irc_socket.send(f"NICK {nickname}\r\n".encode('utf-8'))
    irc_socket.send(f"JOIN #{channel}\r\n".encode('utf-8'))
    return irc_socket

def listen_for_events(irc_socket):
    response = irc_socket.recv(2048).decode('utf-8')
    responses = response.split("\r\n")
    for response in responses:
        if not response:
            continue
        if "PRIVMSG" in response:
            continue
        if "PING" in response:
            irc_socket.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        if "JOIN" in response:
            splitted_response = response.split('!')
            user = splitted_response[0][1:] if len(splitted_response) == 2 else None
            if not user:
                continue
            print(f'{user} has joined the Twitch chat!')
        if "PART" in response:
            splitted_response = response.split('!')
            user = splitted_response[0][1:] if len(splitted_response) == 2 else None
            if not user:
                continue
            print(f'{user} has left the Twitch chat!')

if __name__ == "__main__":
    args = parse_arguments()
    channel_name = args.channel
    irc_socket = connect_to_twitch(channel_name)
    while True:
        try:
            listen_for_events(irc_socket)
        except Exception as e:
            print(f"Error: {e}")
