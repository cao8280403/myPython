# coding=UTF-8
filename = 'test_text.txt'

a = ['weq','rrrrr','wwwvvv']
print(len(a))
with open(filename, 'a',encoding='utf8') as file_object:
    # file_object.write("lalala\n")
    # file_object.write("hahaha\n")
    for x in a:
        file_object.write(x+"\n")

    file_object.close()