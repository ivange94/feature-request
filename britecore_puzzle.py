ascii_values = [104, 116, 116, 112, 115, 58, 47, 47, 101, 110, 103, 105, 110, 101, 101, 114, 105, 110, 103, 45, 97, 112, 112, 108, 105, 99, 97, 116, 105, 111, 110, 46, 98, 114, 105, 116, 101, 99, 111, 114, 101, 46, 99, 111, 109, 47, 113, 117, 105, 122, 47, 115, 100, 102, 103, 119, 114, 52, 52, 104, 114, 102, 104, 102, 104, 45, 119, 115 ]
chr_values = [chr(i) for i in ascii_values]

text = "".join(chr_values)
print(text)