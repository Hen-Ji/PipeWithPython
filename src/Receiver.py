import win32file
import win32pipe


class PipeReceiver:
    def __init__(self):
        self.pipeHandle = 0
        self.pipeName = ""
        self.pipePath = ""
        self.pipeSize = 0

    def open(self, name, size=4096):
        self.pipeName = name
        self.pipePath = f"\\\\.\\pipe\\{name}"
        self.pipeSize = size

        win32pipe.WaitNamedPipe(
            self.pipePath,
            win32pipe.NMPWAIT_USE_DEFAULT_WAIT)

        self.pipeHandle = win32file.CreateFile(
            self.pipePath,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            win32file.FILE_SHARE_WRITE | win32file.FILE_SHARE_READ,
            None,
            win32file.OPEN_EXISTING,
            0,
            None)
        return self.pipeHandle

    def write(self, msg):
        win32file.WriteFile(self.pipeHandle, str.encode(msg), None)

    def read(self):
        try:
            data = win32file.ReadFile(self.pipeHandle, self.pipeSize)
        except Exception:
            return ""
        return bytes(data[1]).decode("utf-8")

    def close(self):
        win32file.CloseHandle(self.pipeHandle)


# 打开管道
receiver = PipeReceiver()
receiver.open("test")

# 读取服务端发来的数据
read = receiver.read()
print(read)

# 向服务端发送数据
s = input()
receiver.write(s)

# 关闭管道
receiver.close()

input("good")
