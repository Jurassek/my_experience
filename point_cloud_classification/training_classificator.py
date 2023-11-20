import pickle
import itertools
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import time
debug = True

#%% Funkcje
# funkcja czytająca dane uczące, walidacyjne i testowe
def read_dane(filepath):
    X, Y = [], []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            tokens = line.strip().split(' ')
            if 'nan' not in tokens:
                class_value = int(float(tokens[class_index]))
                X.append([float(t) for t_index, t in enumerate(tokens) if t_index != class_index])
                Y.append(class_value)
    return np.asarray(X, dtype=np.float64), np.asarray(Y, dtype=np.float64)

# funkcja trenowania modelu Random Forest
def train_model(X_train, Y_train, n_estimators, max_depth, random_state, max_samples, n_jobs):
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        oob_score=True,
        n_jobs=n_jobs,
        class_weight='balanced',
        random_state=random_state,
        max_samples=max_samples
    )
    model.fit(X_train[:, wyb_cech], Y_train)
    return model


# funkcja zapisywania przewidzianej klasyfikacji danych walidacyjnych
def write_klasyfikacja(X, Y, filename):
    with open('{}.txt'.format(filename), 'w') as out:
        X = X.tolist()
        Y = Y.tolist()
        for index, x in enumerate(X):
            x_as_str = " ".join([str(i) for i in x])
            out.write('{} {}\n'.format(x_as_str, str(Y[index])))
            
# funkcja zapisywania modelu do pliku (.pkl)
def save_model(model, filename):
    with open(filename, 'wb') as out:

        pickle.dump(model, out, pickle.HIGHEST_PROTOCOL)

# funkcja czytająca wytrenowany model
def read_model(filepath):
    return pickle.load(open(filepath, 'rb'))

#%%
#Wczytywanie danch
uczace_filepath = 'D:\\MAGIST\\final\\u.txt'
walidacyjne_filepath = 'D:\\MAGIST\\final\\w1.txt'
testowe_filepath= 'D:\\MAGIST\\final\\t.txt'

# Cechy i klasy klumny
#6-26 cechyCC + deltaHigh + normalne
#6-33 cechyCC + deltaHigh + normalne + python
wyb_cech = list(range(6,33))
class_index = 9
wyb_cech.remove(7)
wyb_cech.remove(9)
wyb_cech.remove(10)


# Rdzenie
n_jobs = -1

#%%
print("Ładowanie danych...")

X_train, Y_train = read_dane(uczace_filepath)
X_test, Y_test = read_dane(walidacyjne_filepath)

X_train_other = X_train[Y_train != 1]
Y_train_other = Y_train[Y_train != 1]

X_testowe, Y_testowe = read_dane(testowe_filepath)


print('\tPróbki uczące: {}\n\tPunkty walidacyjne: {}\n\tUżyte cechy o indeksach: {}'.format(len(Y_train_other), len(Y_test), wyb_cech))
print('---> Ilosć punktów w danych klasach (do treningu)')
unique_classes, class_counts = np.unique(Y_train_other, return_counts=True)
for cls, count in zip(unique_classes, class_counts):
    print("Klasa {}: Liczba punktów: {}".format(cls, count)) 

# Trenowanie modelu
# Parametery
n_estimators = [100]
max_depths = [1000]
random_state = [None]
max_samples = [10000]
# Najlepsza konfiguracja parametrów
best_conf = {'ne' : 0, 'md' : 0, 'ms' : 0, 'rs' : 0, 'ms' : 0} 
best_f1 = 0

print('\nTrenowanie modelu...')  
                                  
for ne, md, rs, ms in list(itertools.product(n_estimators, max_depths, random_state, max_samples)):
    start_time = time.time()

    model = train_model(X_train_other, Y_train_other, ne, md, rs, ms, n_jobs)

    Y_test_pred = model.predict(X_test[:, wyb_cech])

    acc = accuracy_score(Y_test, Y_test_pred)
    f1 = f1_score(Y_test, Y_test_pred, average='weighted')
    if f1 > best_f1:
        best_conf['ne'] = ne
        best_conf['md'] = md
        best_conf['rs'] = rs
        best_conf['ms'] = ms
        best_f1 = f1


    end_time = time.time()
    duration = end_time - start_time

    if debug:
        print('\tne: {}, md: {}, rs: {}, ms: {} - acc: {} f1: {} oob_score: {} czas: {:.2f}s'.format(ne, md, rs, ms, acc, f1, model.oob_score_, duration))




print('---> Najlepsze parametry: ne: {}, md: {}, rs: {}, ms: {}'.format(best_conf['ne'], best_conf['md'], best_conf['rs'], best_conf['ms']))
print('---> Istotnosc cech:\n{}'.format(model.feature_importances_))
print('---> Macierz pomyłek klasyfikacji:\n{}'.format(confusion_matrix(Y_test, Y_test_pred)))

model_params = model.get_params()
param_value_list = sorted(model_params.items())
print(param_value_list)


# Wykres istotnosci cech
df = pd.DataFrame(columns=['Cecha', 'Istotnosć'])
for i in range(len(model.feature_importances_)):
    df = df.append({'Cecha':wyb_cech[i], 'Istotnosć':model.feature_importances_[i]}, ignore_index=True)
df = df.sort_values('Istotnosć', ascending = False)
df.plot(x='Cecha', y='Istotnosć', kind='bar', figsize=(12,6))
plt.show()

#%%
# Nazwa pliku walidacyjnego i testowego predict
wal_pred_name = 'wal_pred'
test_pred_name =  'test_pre'

# Zapisywanie modelu klasyfiaktora oraz zapisywanie klasyfikacji
model = train_model(X_train, Y_train, best_conf['ne'], best_conf['md'], best_conf['rs'], best_conf['ms'], n_jobs)

start_time = time.time()
Y_test_pred = model.predict(X_test[:, wyb_cech])
end_time = time.time()
duration = end_time - start_time
print('Czas klasyfikacji zbioru walidacyjnego: {:.2f}s'.format(duration))
print('---> Macierz pomyłek klasyfikacji danych wali:\n{}'.format(confusion_matrix(Y_test, Y_test_pred)))
print('---> Dokładnosc klasyfiakcji danych wali:\n{}'.format(accuracy_score(Y_test, Y_test_pred)))
#%%
# save_model(model, 'ne{}_md{}.pkl'.format(best_conf['ne'], best_conf['md'],))
# W przypadku gdy chcesz zastosować zapisany wczesniej model:
#model = 'E:\magisterka_algorytm\kod_python\ne100_mdNone_rs40.pkl'
#model = read_model(model)

print ('Klasyfikowanie chmury punktów ...')
start_time = time.time()
Y_testowe_pred = model.predict(X_testowe[:, wyb_cech])
end_time = time.time()
duration = end_time - start_time
print('Czas klasyfikacji zbioru testowego: {:.2f}s'.format(duration))

print('---> Macierz pomyłek klasyfikacji danych testowych:\n{}'.format(confusion_matrix(Y_testowe, Y_testowe_pred)))
print('---> Dokładnosc klasyfiakcji danych testowych:\n{}'.format(accuracy_score(Y_testowe, Y_testowe_pred)))
#%%
print ('Zapisywanie klasyfiakcji testowej ...')
write_klasyfikacja(X_testowe, Y_testowe_pred, test_pred_name)
print ('Zapisywanie klasyfiakcji walidacyjnej ...')
write_klasyfikacja(X_test, Y_test_pred, wal_pred_name)