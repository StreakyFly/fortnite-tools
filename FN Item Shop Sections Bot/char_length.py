
# import wx
#
# list = [' ', "•", "'", ".", "!", ",", "-", "?", "(", ")", "&", "%", "$", "#", '"', "=", "*", "_", ":", ";", ">", "<", "+",
#         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
#         'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
#         's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
#
# test_line = "Today is a nice day"
#
# wx_app = wx.App()
# font = wx.Font(pointSize=11, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, faceName='Chirp')
# dc = wx.ScreenDC()
# dc.SetFont(font)
#
# length_dict = dict()
# length_sort = []
# for line in list:
#     length = dc.GetTextExtent(line)[0]
#     length_sort.append((line, length))
#     length_dict[line] = length
#     print((line, length))
#
# length_sort.sort(key=lambda length: length[1])
#
# length_sorted = []
# for ls in length_sort:
#     length_sorted.append(ls[0])
#
# # print(length_sorted)
# print(length_dict)
#
# length = 0
# for x in test_line:
#     length += length_dict[x]
#
# print(length)




def sort_by_text_lenght_char_method(list):
    char_length = {' ': 4, '•': 6, "'": 4, '.': 4, '!': 4, ',': 4, '-': 6, '?': 7, '(': 5, ')': 5, '&': 10, '%': 12,
                   '$': 9, '#': 10, '"': 6, '=': 9, '*': 5, '_': 6, ':': 4, ';': 5, '>': 9, '<': 9, '+': 9, 'A': 10,
                   'B': 10, 'C': 10, 'D': 11, 'E': 9, 'F': 8, 'G': 11, 'H': 11, 'I': 4, 'J': 6, 'K': 10, 'L': 8,
                   'M': 13, 'N': 11, 'O': 11, 'P': 9, 'Q': 11, 'R': 10, 'S': 9, 'T': 9, 'U': 11, 'V': 9, 'W': 14,
                   'X': 10, 'Y': 9, 'Z': 9, 'a': 8, 'b': 9, 'c': 8, 'd': 9, 'e': 8, 'f': 5, 'g': 8, 'h': 8, 'i': 4,
                   'j': 4, 'k': 8, 'l': 4, 'm': 12, 'n': 8, 'o': 8, 'p': 9, 'q': 9, 'r': 5, 's': 7, 't': 5, 'u': 8,
                   'v': 7, 'w': 11, 'x': 7, 'y': 7, 'z': 7, '0': 9, '1': 6, '2': 8, '3': 8, '4': 9, '5': 8, '6': 8,
                   '7': 7, '8': 9, '9': 8}

    length_sort = []
    for sect in list:
        length = 0
        for char in sect:
            try:
                length += char_length[char]
            except:
                length += 6
                print(f"A new unmeasured character has been detected: {char}")
                with open("unmeasured_characters.txt", "a") as file:
                    file.write(f"\n{char}")

        length_sort.append((sect, length))

    length_sort.sort(key=lambda length: length[1])

    length_sorted = []
    for ls in length_sort:
        length_sorted.append(ls[0])

    return length_sorted


sections = ["Daily", "Featured", "Something", "Beans", "_:;<>+--"]

print(sort_by_text_lenght_char_method(sections))




# def sort_by_text_length(list):
#     wx_app = wx.App()
#     font = wx.Font(pointSize=11, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, faceName='Chirp')
#     dc = wx.ScreenDC()
#     dc.SetFont(font)
#
#     length_sort = []
#     for line in list:
#         length = dc.GetTextExtent(line)[0]
#         length_sort.append((line, length))
#         # print(f"{line} | Lenght: {length}")
#
#     length_sort.sort(key=lambda length: length[1])
#
#     length_sorted = []
#     for ls in length_sort:
#         length_sorted.append(ls[0])
#
#     return length_sorted
#
# print(sort_by_text_length(sections))
