import win32file
import win32pipe


class PipeSender:
    def __init__(self):
        self.pipeHandle = 0
        self.pipeName = ""
        self.pipePath = ""
        self.pipeSize = 0

    def create(self, name, size=4096, timeout=0):
        self.pipeName = name
        self.pipePath = f"\\\\.\\pipe\\{name}"
        self.pipeSize = size

        self.pipeHandle = win32pipe.CreateNamedPipe(
            self.pipePath,
            win32pipe.PIPE_ACCESS_DUPLEX,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT | win32pipe.PIPE_READMODE_MESSAGE,
            win32pipe.PIPE_UNLIMITED_INSTANCES,
            size,
            size,
            timeout,
            None)
        return self.pipeHandle

    def connect(self):
        win32pipe.ConnectNamedPipe(self.pipeHandle, None)

    def write(self, msg):
        win32file.WriteFile(self.pipeHandle, str.encode(msg), None)

    def read(self):
        try:
            data = win32file.ReadFile(self.pipeHandle, self.pipeSize)
        except Exception:
            return ""
        return bytes(data[1]).decode("utf-8")

    def disconnect(self):
        win32pipe.DisconnectNamedPipe(self.pipeHandle)

    def close(self):
        win32pipe.DisconnectNamedPipe(self.pipeHandle)
        win32file.CloseHandle(self.pipeHandle)


# 创建命名管道
sender = PipeSender()
sender.create("test")

# 等待客户端的连接
sender.connect()

# 向客户端发送数据
s = input()
sender.write(s)

# 读取客户端数据
read = sender.read()
print(read)

# 关闭管道
sender.close()

input("good")
