import secrets
import time

def remove2(vec):
    return vec.replace("2", "")


def randomsalt(szn, lenght):
    a = ""
    for i in range(lenght):
        a = a + secrets.choice(szn)
    return a


def mix_szn(szn):
    pocet = len(szn)
    for i in range(pocet):
        a = secrets.choice(szn)
        szn.remove(a)
        szn.insert(secrets.randbelow(len(szn)), a)
    print(len(szn))
    return szn


def rotate(list, n):
    while not list[0] == n:
        a = list.pop()
        list.insert(0, a)
    return list


def rotate_back(list, n):
    while not list[0] == n:
        a = list.pop(0)
        list.append(a)
    return list


def sifrovat(data, key1, key2, key3, abeceda, supress="abcdefghijklmnop"):
    time1 = time.time()
    datalen = len(data)
    # < >Vigenere< >
    a,b,c = 0, 0, 0 # Three variables for keys
    vysledek = ""   #Final output from vigenere

    #Adding salt
    key1elenght = min(len(key1) * len(key2) * len(key3), 100)  #Ensuring the salt will be one repeating sequence of keys, if too long it jumps to 100
    labeceda = list(abeceda)                                   #Makes lists of characters that salt can contain
    data = randomsalt(labeceda, key1elenght) + data            #Calls randomsalt function which creates the salt using secrets library and then adds salt to data


    #Utf-8 coding
    utf = data.encode("utf-8")     #Code into numbers from 0 to 256

    #Amplifing the avalanche effect
    data = list(utf)
    for i in range(1, len(data)):
        data[i] = data[i] ^ data[i - 1]


    text = ""
    for i in data:                       #Translates back to characters from extended ascii
        text = text + labeceda[i]       #This way is it ensured that messages can use any characters from utf-8 (including emoji´s and special characters)


    lista = list(abeceda)       #Creates list for mixing
    for i in range(len(text)):  #Goes through every character of text

        #Rotating and mixing
        pozice = lista.index(text[i])                                               # Position of character before mixing
        posun1 = int((lista.index(key1[a])) % len(abeceda))                         # Gets first number for mixing from key1
        lista = rotate(lista, key1[a])                                              # Rotates mixing list
        posun2 = int((lista.index(key2[b]) ^ lista.index(key3[c])) % len(abeceda))  # Gets second number for mixing from key2 xor key3
        lista[posun1], lista[posun2] = lista[posun2], lista[posun1]                 # Swaps two characters in mixing list posun1 and posun2
        lista = rotate(lista, abeceda[posun2])                                      # Rotates mixing list once more
        #lista = rotate(lista, key2[b])                                             #\
        #lista = rotate_back(lista,key3[c])                                         #/ Some more unnesseary rotations



        vysledek = vysledek + lista[pozice]                                         #Gets ciphered character


        a = (a + 1) % len(key1)     #\
        b = (b + 1) % len(key2)     # |> Moving to the next character
        c = (c + 1) % len(key3)     #/


    # </>Vigenere< >

    # < >Base16< >
    base161 = ""   #Variable for data in binary state
    base162 = ""   #Variable for data in normal state
    sifr = abeceda #Creates map for base16

    # Translate to binary
    for i in vysledek:
        a = sifr.index(i)                 # Gets number from map (sifr)
        base161=base161 + format(a,"08b") # Tranalstes number to binary

    # Translating back to characters
    for b in range(0, len(base161), 4): # Goes through every character of binary data
        g = int(base161[b: b + 4], 2)   # Decodes binary to number (4 bits to one number between 0-16)
        base162 += supress[g]           #Adds character from supress with index of the decoded binary to result
    # </>Base16<>
    print("Ciphered data:")
    print("Completed! Time", time.time()-time1, "s, average time for character :", (time.time()-time1)/datalen, "s")
    return base162  # Returns result


def odsifrovat(data, key1, key2, key3, abeceda, supress="abcdefghijklmnop"):
    time1 = time.time()
    datalen = len(data)
    # < >Base16< >
    base161 = ""
    base162 = ""
    sifr = abeceda
    for i in data:
        a = supress.index(i)
        add = ""
        while True:
            if a % 2 == 1:
                add = add + "1"
                a = a - 1
            else:
                add = add + "0"
            a = a // 2
            if a == 0:
                break
        add = add[::-1]
        while len(add) < 4:
            add = "0" + add
        base161 = base161 + add
    for b in range(0, len(base161), 8):
        d = ""
        g = 0
        for c in range(8):
            d = d + base161[b + c]
        d = remove2(d)
        for k in range(len(d)):
            l = 0
            for p in range(len(d) - k):
                l = 2 * l
                if l == 0:
                    l = 1
            if d[k] == "1":
                g = g + l
        base162 = base162 + sifr[g]
    # </>Base16<>

    # < >Vigenere < >
    a = 0
    b = 0
    c = 0
    key1elenght = min(len(key1) * len(key2) * len(key3), 100)

    vysledek = ""
    lista = list(abeceda) #Dynamic aplhabet
    lista2 = list(abeceda) #Aplhabet backup
    for i in range(len(base162)): #For every character

        posun1 = int((lista.index(key1[a])) % len(abeceda))

        lista = rotate(lista, key1[a])

        posun2 = (lista.index(key2[b]) ^ lista.index(key3[c])) % len(abeceda)

        lista[posun1], lista[posun2] = lista[posun2], lista[posun1]

        lista = rotate(lista, abeceda[posun2])

        # lista = rotate(lista, key2[b])

        # lista = rotate_back(lista, key3[c])

        pozice = lista.index(base162[i])

        vysledek = vysledek + lista2[pozice]

        lista2 = list(lista)

        a = (a + 1) % len(key1)
        b = (b + 1) % len(key2)
        c = (c + 1) % len(key3)

    labeceda = list(abeceda)
    text = []
    for i in vysledek:
        text.append(labeceda.index(i))

    data = list(text)
    for i in range(len(data) - 1, 0, -1):
        data[i] = data[i] ^ data[i - 1]
    try:
        vysledek = bytes(data).decode("utf-8")
    except:
        print(" ")
        print("Critic error, data were damaged or manipulated!")
        print("Returning without utf-8 coding!")
        print("!Warning! Data aren´t valid!")
        etext = ""
        ebeceda = abeceda
        for i in data:  # Translates back to characters from extended ascii
            etext = etext + ebeceda[i]
        print(" ")
        vysledek=etext
    vysledek = vysledek[key1elenght:]
    print("Completed! Time", time.time() - time1, "s, average time for character :",
          (time.time() - time1) / datalen, "s")
    print("Deciphered data:")
    return vysledek
    # </>Vigenere < >


abeceda = ""
for i in range(256):
    abeceda = abeceda + chr(i)  # also you can mess with this, map#2 - full ascii in random order
supress = "abcdefghijklmnop"  # key4, it could be different 16 characters

# print("____GENEROVĂNĂŤ MAP_____")
# abeceda = (mix_szn(list(abeceda)))

print(r"""
       █████           ████                                 ██████████ ██████████    █████             Patch notes:     
      ░░███           ░░███                                ░███░░░░███░███░░░░░░█  ███░░░███                       V.1 - Linear version
       ░███   ██████   ░███  ████████  ████████            ░░░    ███ ░███     ░  ███   ░░███                      V.2 - XOR version, Avalanche version
       ░███  ░░░░░███  ░███ ░░███░░███░░███░░███ ██████████      ███  ░█████████ ░███    ░███                      V.3 - Swapping version
       ░███   ███████  ░███  ░███ ░███ ░███ ░░░ ░░░░░░░░░░      ███   ░░░░░░░░███░███    ░███                      V.4 - Swapping & rotating version
 ███   ░███  ███░░███  ░███  ░███ ░███ ░███                    ███     ███   ░███░░███   ███                       V.5 - Utf-8 version
░░████████  ░░████████ █████ ░███████  █████                  ███     ░░████████  ░░░█████░                        V.6 - Salt version
  ░░░░░░░░    ░░░░░░░░ ░░░░░  ░███░░░  ░░░░░                  ░░░       ░░░░░░░░     ░░░░░░                        V.7 - Extra avalanche version
                              ░███                                                                                 
                              █████                             V.7 - Extra avalanche version                                        
                              ░░░░░                             Created by Ja1pr       
▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓
""")

# print("____MAPY GENEROVĂNY_____")
# print(abeceda)
print("Please entry data")
sifr = input("> ")
key1 = input("Entry key one   > ")
key2 = input("Entry key two   > ")
key3 = input("Entry key three > ")
co = int(input("Write 1 for deciphering, or 2 for ciphering > "))

print("▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓▒▓▒▒▒░▒░░░▒░▒▒▒▓▒▓▓▓")
print("")
if co == 1:

    print(odsifrovat(sifr, key1, key2, key3, abeceda))
else:

    print(sifrovat(sifr, key1, key2, key3, abeceda))


