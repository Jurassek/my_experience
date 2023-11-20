import numpy as np

#%%
# Wczytaj chmurę punktów sklasyfikowanych poprawnie
poprawnie_sklasyfikowane = np.loadtxt('D:\\MAGIST\\final\\t.txt')

# Wczytaj chmurę punktów sklasyfikowanych przez model
sklasyfikowane_przez_model = np.loadtxt('D:\\MAGIST\\final\\test_pre.txt')
#%%
# Porównaj indeksy klas w obu chmurach punktów
indeksy_klas_poprawne = poprawnie_sklasyfikowane[:, 9]  # Indeksy klas w 9. kolumnie w chmurze poprawnie sklasyfikowanych punktów
indeksy_klas_model = sklasyfikowane_przez_model[:, -1]  # Indeksy klas w ostatniej kolumnie w chmurze punktów sklasyfikowanych przez model

# Znajdź indeksy punktów źle sklasyfikowanych
indeksy_zle_sklasyfikowane = np.where(indeksy_klas_poprawne != indeksy_klas_model)[0]

# Tworzenie dodatkowej kolumny, która oznacza poprawne i źle sklasyfikowane punkty
chmura_punktow = np.concatenate((sklasyfikowane_przez_model, np.zeros((sklasyfikowane_przez_model.shape[0], 1))), axis=1)  # Dodanie pustej kolumny

# Ustawienie wartości 1 dla punktów źle sklasyfikowanych
chmura_punktow[indeksy_zle_sklasyfikowane, -1] = 1

np.savetxt('D:\\MAGIST\\final\\chmura_punktow_test.txt', chmura_punktow, fmt='%.5f')
