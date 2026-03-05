import secrets


def remove2(vec):
    return vec.replace("2", "")

def mix_szn(szn):
    pocet = len(szn)
    for i in range(pocet):
        a = secrets.choice(szn)
        szn.remove(a)
        szn.insert(secrets.randbelow(len(szn)),a)
    print(len(szn))
    return szn

def rotate(list,n):
    while not list[0]==n:
        a=list.pop()
        list.insert(0,a)
    return list

def rotate_back(list,n):
    while not list[0]==n:
        a=list.pop(0)
        list.append(a)
    return list

def sifrovat(slovo,klic,klic2,klic3,abeceda , supress="abcdefghijklmnop"):
    #< >Vigenere< >
    a=0
    b=0
    c=0
    vysledek=""
    lista = list(abeceda)
    for i in range(len(slovo)):
        

        pozice=lista.index(slovo[i])
        posun1 = int((lista.index(klic[a])) % len(abeceda))
        #lista=rotate(lista,klic[a])
        
        posun2 = int((lista.index(klic2[b]) ^ lista.index(klic3[c])) % len(abeceda))
        
        lista[posun1], lista[posun2] = lista[posun2], lista[posun1]
        
        lista = rotate(lista, abeceda[posun2])
        
        #lista = rotate(lista, klic2[b])

        #lista = rotate_back(lista,klic3[c])

        vysledek=vysledek+lista[pozice]
        a=a+1
        b=b+1
        c=c+1
        if a>=len(klic):
            a=0
        if b >= len(klic2):
            b = 0
        if c >= len(klic3):
            c = 0
    #</>Vigenere< >


    #< >Base16< >
    kĂłd1 = ""
    kĂłd2 = ""
    sifr = abeceda

    # Dostat do binĂˇrnĂ­ soustavy
    for i in vysledek:
        a = sifr.index(i)  # pozice na mapÄ›
        add = ""

        # Do binĂˇrnĂ­ soustavy
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
        while len(add) < 8:
            add = "0" + add
        kĂłd1 = kĂłd1 + add

    # ZpÄ›t na pĂ­smena
    for b in range(0, len(kĂłd1), 4):
        d = ""
        g = 0
        for c in range(4):
            d = d + kĂłd1[b + c]
        d = remove2(d)
        for k in range(len(d)):
            l = 0
            if d[k] == "1":
                for p in range(len(d) - k):
                    l = 2 * l
                    if l == 0:
                        l = 1
            g = g + l
        kĂłd2 = kĂłd2 + supress[g]
    #</>Base16<>

    return kĂłd2

def odsifrovat(slovo,klic,klic2,klic3,abeceda ,supress="abcdefghijklmnop"):
    #< >Base16< >
    kĂłd1 = ""
    kĂłd2 = ""
    sifr = abeceda
    for i in slovo:
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
        kĂłd1 = kĂłd1 + add
    for b in range(0, len(kĂłd1), 8):
        d = ""
        g = 0
        for c in range(8):
            d = d + kĂłd1[b + c]
        d = remove2(d)
        for k in range(len(d)):
            l = 0
            for p in range(len(d) - k):
                l = 2 * l
                if l == 0:
                    l = 1
            if d[k] == "1":
                g = g + l
        kĂłd2 = kĂłd2 + sifr[g]
    #</>Base16<>

    #< >Vigenere < >
    a = 0
    b=0
    c=0
    vysledek = ""
    lista = list(abeceda)
    lista2 = list(abeceda)
    for i in range(len(kĂłd2)):
        
        posun1 = int((lista.index(klic[a])) % len(abeceda))
        #lista = rotate(lista, klic[a])
        
        posun2 = (lista.index(klic2[b]) ^ lista.index(klic3[c])) % len(abeceda)
        
        lista[posun1], lista[posun2] = lista[posun2], lista[posun1]
        
        lista = rotate(lista, abeceda[posun2])

        #lista = rotate(lista, klic2[b])

        #lista = rotate_back(lista, klic3[c])

        pozice = lista.index(kĂłd2[i])

        

        vysledek = vysledek + lista2[pozice]

        lista2=list(lista)



        a = a + 1
        if a >= len(klic):
            a = 0
        b = b + 1
        if b >= len(klic2):
            b = 0
        c=c+1
        if c >= len(klic3):
            c = 0
    # </>Vigenere < >

    return vysledek



abeceda=""
for i in range(256):
    abeceda= abeceda + chr(i) #also you can mess with this, map#2 - full ascii in random order
supress = "abcdefghijklmnop"  #key4, it could be different 16 characters

#print("____GENEROVĂNĂŤ MAP_____")
#abeceda = (mix_szn(list(abeceda)))


#print("____MAPY GENEROVĂNY_____")
#print(abeceda)

sifr=input("Slovo pro ĹˇifrovĂˇnĂ­ nebo odĹˇifrovĂˇnĂ­:")
klic=input("KlĂ­ÄŤ:")
klic2 = input("KlĂ­ÄŤ2:")
klic3= input("KlĂ­ÄŤ3:")
co=int(input("Zadej 1 pro odĹˇifrovĂˇnĂ­, 2 pro zaĹˇifrovĂˇnĂ­:"))

if co==1:
     print(odsifrovat(sifr,klic,klic2,klic3,abeceda))
else:
     print(sifrovat(sifr,klic,klic2,klic3,abeceda))













