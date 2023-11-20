import funkcje as f

if __name__ == '__main__':
    print('Witamy w grze kółko i krzyżyk! ')
    i = 1
    
    # Wybór swojego znaczka
    gracze = f.wybor_gracza()
    
    # Wyczyszczenie planszy
    pole = ['#']*10
    f.plansza_wzor()
    while True:
        
        # Ustawienie gry
        gra = f.plansza_pelna(pole)
        while not gra:
            
            # Gracz decyduje gdzie umiescic znaczek
            pozycja = f.spr_pole_gracz(pole)
            
            #Sprawdzanie kto w danym momencie gra
            if i % 2 == 0:
                znak = gracze[1]
            else:
                znak = gracze[0]
            
            # Zaczecie gry
            f.znaczek_mark(pole, znak, int(pozycja))
            
            #Sprawdzenie i wyswietlenie planszy
            f.plansza(pole)
            i += 1
            
            #Sprawdzenie wygranej
            if f.spr_wyg(pole, znak):
                print('Wygrałes !!!')
                break
            gra = f.plansza_pelna(pole)
            
            # Powtórzenie rozgrywki
        if not f.powtorz():
            break
        else:
            i=1
            
            #Wybór swojego znaczka
            gracze = f.wybor_gracza()
            
            # Wyczyszczenie planszy
            pole = ['#'] * 10
            