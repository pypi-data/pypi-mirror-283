__author_ = 'MPMMS'
def func(x):
    c = len(x)
    b = c*['']
    for i in range(c):
        b[i] = x[i]
    return b

def encrypt(text):
    s = func(text)
    x = ''
    for i in range(len(s)):
        if s[i]=='ا' or s[i]=='آ':
            x += 'ی'
        elif s[i]=='ب':
            x += 'ه'
        elif s[i]=='پ':
            x += 'و'
        elif s[i]=='ت':
            x += 'ن'
        elif s[i]=='ث':
            x += 'م'
        elif s[i]=='ج':
            x += 'ل'
        elif s[i]=='چ':
            x += 'گ'
        elif s[i]=='ح':
            x += 'ک'
        elif s[i]=='خ':
            x += 'ق'
        elif s[i]=='د':
            x += 'ف'
        elif s[i]=='ذ':
            x += 'غ'
        elif s[i]=='ر':
            x += 'ع'
        elif s[i]=='ز':
            x += 'ظ'
        elif s[i]=='ژ':
            x += 'ط'
        elif s[i]=='س':
            x += 'ض'
        elif s[i]=='ش':
            x += 'ص'
        elif s[i]=='ص':
            x += 'ش'
        elif s[i]=='ض':
            x += 'س'
        elif s[i]=='ط':
            x += 'ژ'
        elif s[i]=='ظ':
            x += 'ز'
        elif s[i]=='ع':
            x += 'ر'
        elif s[i]=='غ':
            x += 'ذ'
        elif s[i]=='ف':
            x += 'د'
        elif s[i]=='ق':
            x += 'خ'
        elif s[i]=='ک':
            x += 'ح'
        elif s[i]=='گ':
            x += 'چ'
        elif s[i]=='ل':
            x += 'ج'
        elif s[i]=='م':
            x += 'ث'
        elif s[i]=='ن':
            x += 'ت'
        elif s[i]=='و':
            x += 'پ'
        elif s[i]=='ه':
            x += 'ب'
        elif s[i]=='ی':
            x += 'ا'
        elif s[i]=='1':
            x += '0'
        elif s[i]=='2':
            x += '9'
        elif s[i]=='3':
            x += '8'
        elif s[i]=='4':
            x += '7'
        elif s[i]=='5':
            x += '6'
        elif s[i]=='6':
            x += '5'
        elif s[i]=='7':
            x += '4'
        elif s[i]=='8':
            x += '3'
        elif s[i]=='9':
            x += '2'
        elif s[i]=='0':
            x += '1'
        elif s[i]=='a':
            x += 'z'
        elif s[i]=='b':
            x += 'y'
        elif s[i]=='c':
            x += 'x'
        elif s[i]=='d':
            x += 'w'
        elif s[i]=='e':
            x += 'v'
        elif s[i]=='f':
            x += 'u'
        elif s[i]=='g':
            x += 't'
        elif s[i]=='h':
            x += 's'
        elif s[i]=='i':
            x += 'r'
        elif s[i]=='j':
            x += 'q'
        elif s[i]=='k':
            x += 'p'
        elif s[i]=='l':
            x += 'o'
        elif s[i]=='m':
            x += 'n'
        elif s[i]=='n':
            x += 'm'
        elif s[i]=='o':
            x += 'l'
        elif s[i]=='p':
            x += 'k'
        elif s[i]=='q':
            x += 'j'
        elif s[i]=='r':
            x += 'i'
        elif s[i]=='s':
            x += 'h'
        elif s[i]=='t':
            x += 'g'
        elif s[i]=='u':
            x += 'f'
        elif s[i]=='v':
            x += 'e'
        elif s[i]=='w':
            x += 'd'
        elif s[i]=='x':
            x += 'c'
        elif s[i]=='y':
            x += 'b'
        elif s[i]=='z':
            x += 'a'
        elif s[i]=='A':
            x += 'Z'
        elif s[i]=='B':
            x += 'Y'
        elif s[i]=='C':
            x += 'X'
        elif s[i]=='D':
            x += 'W'
        elif s[i]=='E':
            x += 'V'
        elif s[i]=='F':
            x += 'U'
        elif s[i]=='G':
            x += 'T'
        elif s[i]=='H':
            x += 'S'
        elif s[i]=='I':
            x += 'R'
        elif s[i]=='J':
            x += 'Q'
        elif s[i]=='K':
            x += 'P'
        elif s[i]=='L':
            x += 'O'
        elif s[i]=='M':
            x += 'N'
        elif s[i]=='N':
            x += 'M'
        elif s[i]=='O':
            x += 'L'
        elif s[i]=='P':
            x += 'K'
        elif s[i]=='Q':
            x += 'J'
        elif s[i]=='R':
            x += 'I'
        elif s[i]=='S':
            x += 'H'
        elif s[i]=='T':
            x += 'G'
        elif s[i]=='U':
            x += 'F'
        elif s[i]=='V':
            x += 'E'
        elif s[i]=='W':
            x += 'D'
        elif s[i]=='X':
            x += 'C'
        elif s[i]=='Y':
            x += 'B'
        elif s[i]=='Z':
            x += 'A'
        else:
            x += s[i]
    return x
def decrypt(text):
    s = func(text)
    x = ''
    for i in range(len(s)):
        if s[i]=='ا' or s[i]=='آ':
            x += 'ی'
        elif s[i]=='ب':
            x += 'ه'
        elif s[i]=='پ':
            x += 'و'
        elif s[i]=='ت':
            x += 'ن'
        elif s[i]=='ث':
            x += 'م'
        elif s[i]=='ج':
            x += 'ل'
        elif s[i]=='چ':
            x += 'گ'
        elif s[i]=='ح':
            x += 'ک'
        elif s[i]=='خ':
            x += 'ق'
        elif s[i]=='د':
            x += 'ف'
        elif s[i]=='ذ':
            x += 'غ'
        elif s[i]=='ر':
            x += 'ع'
        elif s[i]=='ز':
            x += 'ظ'
        elif s[i]=='ژ':
            x += 'ط'
        elif s[i]=='س':
            x += 'ض'
        elif s[i]=='ش':
            x += 'ص'
        elif s[i]=='ص':
            x += 'ش'
        elif s[i]=='ض':
            x += 'س'
        elif s[i]=='ط':
            x += 'ژ'
        elif s[i]=='ظ':
            x += 'ز'
        elif s[i]=='ع':
            x += 'ر'
        elif s[i]=='غ':
            x += 'ذ'
        elif s[i]=='ف':
            x += 'د'
        elif s[i]=='ق':
            x += 'خ'
        elif s[i]=='ک':
            x += 'ح'
        elif s[i]=='گ':
            x += 'چ'
        elif s[i]=='ل':
            x += 'ج'
        elif s[i]=='م':
            x += 'ث'
        elif s[i]=='ن':
            x += 'ت'
        elif s[i]=='و':
            x += 'پ'
        elif s[i]=='ه':
            x += 'ب'
        elif s[i]=='ی':
            x += 'ا'
        elif s[i]=='1':
            x += '0'
        elif s[i]=='2':
            x += '9'
        elif s[i]=='3':
            x += '8'
        elif s[i]=='4':
            x += '7'
        elif s[i]=='5':
            x += '6'
        elif s[i]=='6':
            x += '5'
        elif s[i]=='7':
            x += '4'
        elif s[i]=='8':
            x += '3'
        elif s[i]=='9':
            x += '2'
        elif s[i]=='0':
            x += '1'
        elif s[i]=='a':
            x += 'z'
        elif s[i]=='b':
            x += 'y'
        elif s[i]=='c':
            x += 'x'
        elif s[i]=='d':
            x += 'w'
        elif s[i]=='e':
            x += 'v'
        elif s[i]=='f':
            x += 'u'
        elif s[i]=='g':
            x += 't'
        elif s[i]=='h':
            x += 's'
        elif s[i]=='i':
            x += 'r'
        elif s[i]=='j':
            x += 'q'
        elif s[i]=='k':
            x += 'p'
        elif s[i]=='l':
            x += 'o'
        elif s[i]=='m':
            x += 'n'
        elif s[i]=='n':
            x += 'm'
        elif s[i]=='o':
            x += 'l'
        elif s[i]=='p':
            x += 'k'
        elif s[i]=='q':
            x += 'j'
        elif s[i]=='r':
            x += 'i'
        elif s[i]=='s':
            x += 'h'
        elif s[i]=='t':
            x += 'g'
        elif s[i]=='u':
            x += 'f'
        elif s[i]=='v':
            x += 'e'
        elif s[i]=='w':
            x += 'd'
        elif s[i]=='x':
            x += 'c'
        elif s[i]=='y':
            x += 'b'
        elif s[i]=='z':
            x += 'a'
        elif s[i]=='A':
            x += 'Z'
        elif s[i]=='B':
            x += 'Y'
        elif s[i]=='C':
            x += 'X'
        elif s[i]=='D':
            x += 'W'
        elif s[i]=='E':
            x += 'V'
        elif s[i]=='F':
            x += 'U'
        elif s[i]=='G':
            x += 'T'
        elif s[i]=='H':
            x += 'S'
        elif s[i]=='I':
            x += 'R'
        elif s[i]=='J':
            x += 'Q'
        elif s[i]=='K':
            x += 'P'
        elif s[i]=='L':
            x += 'O'
        elif s[i]=='M':
            x += 'N'
        elif s[i]=='N':
            x += 'M'
        elif s[i]=='O':
            x += 'L'
        elif s[i]=='P':
            x += 'K'
        elif s[i]=='Q':
            x += 'J'
        elif s[i]=='R':
            x += 'I'
        elif s[i]=='S':
            x += 'H'
        elif s[i]=='T':
            x += 'G'
        elif s[i]=='U':
            x += 'F'
        elif s[i]=='V':
            x += 'E'
        elif s[i]=='W':
            x += 'D'
        elif s[i]=='X':
            x += 'C'
        elif s[i]=='Y':
            x += 'B'
        elif s[i]=='Z':
            x += 'A'
        else:
            x += s[i]
    return x