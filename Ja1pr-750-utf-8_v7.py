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
    time1 = time.time() #Time measuring
    datalen = len(data)
    # < >Vigenere< >
    a,b,c = 0, 0, 0 # Three variables for keys
    vysledekl = []   #Final output from vigenere

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

    textl = []
    for i in data:                       #Translates back to characters from extended ascii
        textl.append(labeceda[i])       #This way is it ensured that messages can use any characters from utf-8 (including emoji´s and special characters)
    text = "".join(textl)               #Using .append and .join, as it is faster than +


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

        vysledekl.append(lista[pozice])                                  #Gets ciphered character

        a = (a + 1) % len(key1)     #\
        b = (b + 1) % len(key2)     # |> Moving to the next character
        c = (c + 1) % len(key3)     #/
    vysledek = "".join(vysledekl) #Using .append and .join, as it is faster than +
    # </>Vigenere< >

    # < >Base16< >
    base162 = []   #Variable for data in normal state
    sifr = abeceda #Creates map for base16

    # Translate to binary
    base161 = [format(sifr.index(i),"08b") for i in vysledekl] # Translates number to binary
    base161 = "".join(base161)
    # Translating back to characters
    for b in range(0, len(base161), 4): # Goes through every character of binary data
        g = int(base161[b:b+4], 2)   # Decodes binary to number (4 bits to one number between 0-16)
        base162.append(supress[g])         #Adds character from supress with index of the decoded binary to result
    base162 = "".join(base162)
    # </>Base16<>
    print("Ciphered data:")
    print("Completed! Time", time.time()-time1, "s, average time for character :", (time.time()-time1)/datalen, "s")
    return base162  # Returns result


def odsifrovat(data, key1, key2, key3, abeceda, supress="abcdefghijklmnop"):
    time1 = time.time() # Time measuring
    datalen = len(data)

    # < >Base16< >
    base161, base162  = [], [""]
    sifr = abeceda # Gets map

    for i in data:
        a = supress.index(i)        # Gets number for coding
        base161.append(format(a,"04b"))  # Codes number into half bytes
    base161 = "".join(base161) # Again uses .append because it is faster etc.

    for b in range(0, len(base161), 8): # Goes through every eight character of base161
        g =  int(base161[b:b+8],2)      #  Translates binary into decimal
        base162.append(sifr[g])
    base162 = "".join(base162)  # Once more
    # </>Base16<>

    # < >Vigenere < >
    a, b ,c = 0, 0, 0
    key1elenght = min(len(key1) * len(key2) * len(key3), 100)

    vysledekl = []
    lista = list(abeceda) #Dynamic alphabet
    lista2 = list(abeceda) # Alphabet backup
    for i in range(len(base162)): #For every character

        posun1 = int((lista.index(key1[a])) % len(abeceda))                     # Gets first number for deciphering from key1
        lista = rotate(lista, key1[a])                                          # Rotates dynamic list
        posun2 = (lista.index(key2[b]) ^ lista.index(key3[c])) % len(abeceda)   # Gets second number for deciphering from key2 xor key3
        lista[posun1], lista[posun2] = lista[posun2], lista[posun1]             # Swaps two characters in dynamic list posun1 and posun2
        lista = rotate(lista, abeceda[posun2])                                  # Rotates dynamic list once more
        # lista = rotate(lista, key2[b])
        # lista = rotate_back(lista, key3[c])

        pozice = lista.index(base162[i]) #  Position of character after mixing
        vysledekl.append(lista2[pozice]) #  Gets of character from backup list
        lista2 = list(lista)        # Saving alphabet state for next character (to decode avalanche effect)

        a = (a + 1) % len(key1)     #\
        b = (b + 1) % len(key2)     # |> Moving to the next character
        c = (c + 1) % len(key3)     #/

    data = [abeceda.index(i) for i in vysledekl] #Translating into numbers for de-avalanche

    # De-avalanching
    for i in range(len(data) - 1, 0, -1):
        data[i] = data[i] ^ data[i - 1]

    # Using try because of possible errors in transmitting
    try:
        vysledek = bytes(data).decode("utf-8") # Decodes in utf
    except: # Means utf-8 coding was unsuccesfull
        print(" ")                                                # Informing user
        print("Critic error, data were damaged or manipulated!")
        print("Returning without utf-8 coding!")
        print("!Warning! Data aren´t valid!")
        etext = [abeceda[i] for i in data]  # Emergency translating data into ASCII extended
        vysledek="".join(etext)
    vysledek = vysledek[key1elenght:]
    print("Completed! Time", time.time() - time1, "s, average time for character :",
          (time.time() - time1) / datalen, "s") # Calculate used time
    print("Deciphered data:")
    return vysledek # Retrurns deciphered data
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

    si = (sifrovat(sifr, key1, key2, key3, abeceda))
    print(si)
    azn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in si:
        azn[supress.index(i)] = azn[supress.index(i)] + 1
    for a in azn:
        print(a * 100 / len(si))


