from ctypes import cdll, c_int, c_char_p
lib = cdll.LoadLibrary("target/release/libalignment_rust.so")

lib.alignment.argtypes = (c_char_p, c_char_p)
lib.alignment.restype = c_int
sequence_test1 = "AAAAA----AA".encode('utf-8')
sequence_test2 = "ABCDEFG".encode('utf-8')
result = lib.alignment(sequence_test1, sequence_test2)
print(result)