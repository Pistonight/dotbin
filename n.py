#!usr/bin/env python
"""Prints information about the number n"""
import sys
import struct
def group(s, n):
    x  = len(s) % n
    if x:
        s = "0" * (n-x) + s
    return " ".join(s[i:i+n] for i in range(0, len(s), n))
def p(s, n):
    print(f"{s:<16}: {n}")
def info_n(n):
    u64 = n & 0xFFFFFFFFFFFFFFFF
    u32 = u64 & 0xFFFFFFFF
    i64 = struct.unpack('<q', struct.pack('<Q', u64))[0]
    i32 = struct.unpack('<i', struct.pack('<I', u32))[0]
    f32 = struct.unpack('<f', struct.pack('<I', u32))[0]
    f64 = struct.unpack('<d', struct.pack('<Q', u64))[0]
    info(u32, u64, i32, i64, f32, f64)
def info_f(n):
    u32 = struct.unpack('<I', struct.pack('<f', n))[0]
    u64 = struct.unpack('<Q', struct.pack('<d', n))[0]
    i32 = struct.unpack('<i', struct.pack('<f', n))[0]
    i64 = struct.unpack('<q', struct.pack('<d', n))[0]
    info(u32, u64, i32, i64, n, n)
def info(u32, u64, i32, i64, f32, f64):
    if u32 == i32:
        p("Decimal-32", u32)
    else:
        p("Signed-32", i32)
        p("Unsigned-32", u32)
    if u64 == i64:
        p("Decimal-64", u64)
    else:
        p("Signed-64", i64)
        p("Unsigned-64", u64)
    if u32 == u64:
        p("Hex", hex(u32))
        p("Binary", group(bin(u32)[2:], 4))
    else:
        p("Hex-32", hex(u32))
        p("Hex-64", hex(u64))
        p("Binary-32", group(bin(u32)[2:], 4))
        p("Binary-64", group(bin(u64)[2:], 4))
    if f32 == f64:
        p("IEEE-754", f32)
    else:
        p("Float-32", f32)
        p("Float-64", f64)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python n.py <number>")
        sys.exit(1)
    n = sys.argv[1]
    if "." in n:
        info_f(float(n))
    else:
        if n.startswith("0x"):
            n = int(n, 16)
        elif n.startswith("0b"):
            n = int(n, 2)
        else:
            n = int(n)
        info_n(n)