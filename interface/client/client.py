import socket


def main():
    waiting_port = 8000
    # 获取服务器地址，需要提供一个端口号
    # server_ip = get_server_ip(waiting_port)

    server_port = 8080
    command = "get all"
    # 向服务器发送一个指令，获取结果
    recvData = send_message("127.0.0.1", server_port, command)

    print('接收到的数据为: ', recvData)


def get_server_ip(PORT):
    """
    UDP协议用于获取服务器地址
    :param PORT: 获取的端口号
    :return: 返回服务器地址
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 开启一个udp协议
    address = ("0.0.0.0", PORT)
    server_socket.bind(address)  # 绑定0.0.0.0地址，端口号8000
    receive_data, client = server_socket.recvfrom(1024)  # 接收到服务器发送的hello数据
    server_ip = client[0]  # 解析出服务器地址
    server_socket.close()  # 关闭连接
    return server_ip


def send_message(server_ip, server_port, send_data):
    """
    TCP协议发送指令，接收返回数据
    :param server_ip: 服务器地址
    :param server_port: 服务器端口
    :param send_data: 发送指令
    :return: 数据返回，如果服务器发生错误，则返回error
    """
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 绑定tcp协议
    tcp_client_socket.connect((server_ip, server_port))  # 绑定服务器地址和端口
    tcp_client_socket.send(send_data.encode("gbk"))  # 发送数据
    recvData = tcp_client_socket.recv(1024).decode('gbk')  # 接收服务器反馈结果
    tcp_client_socket.close()  # 关闭连接
    return recvData


if __name__ == "__main__":
    main()
