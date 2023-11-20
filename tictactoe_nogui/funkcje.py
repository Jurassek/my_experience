# Plansza wzorcowa
def plansza_wzor():
    plansza_wzor = """
___________________
|     |     |     |
|  7  |  8  |  9  |
|_____|_____|_____|
|     |     |     |
|  4  |  5  |  6  |
|_____|_____|_____|
|     |     |     |
|  1  |  2  |  3  |
|_____|_____|_____|
"""
print(plansza_wzor)

# Plansza
def plansza(pole):
    pusta_plansza = """
___________________
|     |     |     |
|  7  |  8  |  9  |
|_____|_____|_____|
|     |     |     |
|  4  |  5  |  6  |
|_____|_____|_____|
|     |     |     |
|  1  |  2  |  3  |
|_____|_____|_____|
"""
    for i in range(1, 10):
        if (pole[i] == 'O' or pole[i] == 'X'):
            pusta_plansza = pusta_plansza.replace(str(i), pole[i])
        else:
            pusta_plansza = pusta_plansza.replace(str(i), ' ')
    print(pusta_plansza)


# Wybór znaczka    
def wybor_gracza():
    gracz1 = input('Wybierz znaczek X/x lub O/o: ')
    while True:
        if gracz1.upper() == 'X':
            gracz2 = 'O'
            print('Wybrałes znaczek X, drugi gracz będzie znaczkiem O')
            return gracz1.upper(), gracz2
        
        elif gracz1.upper() == 'O':
            gracz2 = 'X'
            print('Wybrałes znaczek O, drugi gracz będzie znaczkiem X')
            return gracz1.upper(), gracz2
        else:
            gracz1 = input('Wybierz znaczek X/x lb O/o: ')
        
# Postawienie znaczka
def znaczek_mark(pole, znak, pozycja):
    pole[pozycja] = znak
    return pole

# Sprawdzanie miejsca
def spr_pole(pole, pozycja):
    return pole[pozycja] == '#'

# Sprawdzanie miejsca pod wybór gracza
def spr_pole_gracz(pole):
    wybor = input('Wybierz miejsce na wstawienie znaczka od 1 do 9.')
    while not spr_pole(pole, int(wybor)):
        wybor = input('To pole jest zajęte. Proszę wybierz mijesce od 1 do 9 jeszcze raz.')
    return wybor
        
# Sprawdanie czy plansza jest zapełniona
def plansza_pelna(pole):
    return len([x for x in pole if x == '#']) == 1

# Sprawdzanie wygranej
def spr_wyg(pole, znak):
    if pole[1] == pole[2] == pole[3] == znak:
        return True
    if pole[4] == pole[5] == pole[6] == znak:
        return True
    if pole[7] == pole[8] == pole[9] == znak:
        return True
    if pole[1] == pole[4] == pole[7] == znak:
        return True
    if pole[2] == pole[5] == pole[8] == znak:
        return True
    if pole[3] == pole[6] == pole[9] == znak:
        return True
    if pole[1] == pole[5] == pole[9] == znak:
        return True
    if pole[3] == pole[5] == pole[7] == znak:
        return True
    return False

# Pytanie o powtórke
def powtorz():
    powtorka = input('Czy chcecie zagrać jeszcze raz? [T - Tak/N - Nie]')
    if powtorka.upper == 'T':
        return True
    if powtorka.upper == 'N':
        return False

    
    
        
        
    