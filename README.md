# PipeWithPython
PipeWithPython: 基于Python的双向命名管道，可实现进程间通信

例:
客户端:
```
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
```
服务端:
```
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
```
先运行服务端，再运行客户端即可

注: 使用方法与 PipeWithCpp 相同
