from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


dataset = pd.read_excel("TGF05.xls")


def select_lx(dataset, age):
    generation = str(2023 - age)
    return dataset[generation]


def lx(x, table):
    return table[x]


def Cx(x, rate, table):
    return (lx(x, table) - lx(x + 1, table)) / ((1 + rate) ** (x + 1))


def Mx(x, rate, table):
    sum = 0
    for i in range(len(table) - x - 1):
        sum += Cx(i + x, rate, table)
    return sum


def Dx(x, rate, table):
    return ((1 / (1 + rate)) ** x) * lx(x, table)


def Nx(x, rate, table):
    sum = 0
    for i in range(len(table) - x - 1):
        sum += Dx(i + x, rate, table)
    return sum


def annuityFactor(x, m, n, rate, table):
    return (Mx(x + m, rate, table) - Mx(x + m + n, rate, table)) / Dx(x, rate, table)


def create_dataset(N):
    age_array = np.zeros(N)
    for i in range(len(age_array)):
        age_array[i] = random.randint(18, 75)
    term_array = np.zeros(N)
    for i in range(N):
        term_array[i] = random.randint(1, 120 - age_array[i])
    differed_array = np.zeros(N)
    for i in range(N):
        differed_array[i] = random.randint(1, 120 - age_array[i])
    nb_payement = np.zeros(N)
    for i in range(N):
        nb_payement[i] = random.randint(1, term_array[i])
    amount = np.zeros(N)
    for i in range(N):
        amount[i] = random.randint(100, 1000)
    interest_rate = np.zeros(N)
    for i in range(N):
        interest_rate[i] = random.randint(1, 100) / 1000
    Price = np.zeros(N)
    for i in range(N):
        Price[i] = amount[i] * ((Nx(int(age_array[i]) + int(differed_array[i]) + 1, float(interest_rate[i]),
                                    select_lx(dataset, int(age_array[i]))) -
                                 Nx(int(age_array[i]) + int(differed_array[i]) + int(nb_payement[i]) + 1,
                                    float(interest_rate[i]), select_lx(dataset, int(age_array[i])))) /
                                Dx(int(age_array[i]), float(interest_rate[i]), select_lx(dataset, int(age_array[i]))))
    df = {'age': age_array, 'term': term_array, 'nb_paiement': nb_payement, 'differed': differed_array,
          'amount': amount, 'interest_rate': interest_rate, 'Price': Price}
    df = pd.DataFrame(data=df)
    return df


def prediction_knn(taille, age, term, nb_paiment, amount, rate, differed):
    df = create_dataset(taille)
    X = df[['age', 'term', 'nb_paiement', 'differed', 'amount', 'interest_rate']]
    y = df['Price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    # training
    knn = KNeighborsRegressor(n_neighbors=3)
    knn.fit(X_train, y_train)
    data = [age, term, nb_paiment, differed, amount, rate]
    X_to_predict = pd.DataFrame([data], columns=['age', 'term', 'nb_paiement', 'differed', 'amount', 'interest_rate'])
    pricer = amount * ((Nx(age + differed + 1, rate, select_lx(dataset, age)) -
                        Nx(age + differed + nb_paiment + 1, rate, select_lx(dataset, age))) / Dx(age, rate,
                                                                                                 select_lx(dataset,
                                                                                                           age)))

    result = knn.predict(X_to_predict)
    return pricer, result[0]


app = Flask(__name__)

CORS(app)


# http://127.0.0.1:5000/predict/1500/50/10/5/550/0.02/3
# prediction_knn(1500, 50, 10, 5, 1000, 0.02)
@app.get("/predict/<int:taille>/<int:age>/<int:term>/<int:nb_paiment>/<int:amount>/<float:rate>/<int:differed>")
def calcul(taille, age, term, nb_paiment, amount, rate, differed):
    u, p = prediction_knn(taille, age, term, nb_paiment, amount, rate, differed)
    price = float("{:.2f}".format(u))
    pred = float("{:.2f}".format(p))
    return jsonify(pred, price)


if __name__ == "__main__":
    app.run(debug=True)
