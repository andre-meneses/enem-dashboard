import data_handler as dh
import numpy as np
import os

def label_data(tipo_prova, csv_prova, redo=False):

    labels_folder = 'labels/'

    if not os.path.exists(labels_folder):
        os.makedirs(labels_folder)

    gabarito = 'TX_GABARITO_' + tipo_prova
    respostas = 'TX_RESPOSTAS_' + tipo_prova

    x_filename = os.path.join(labels_folder, 'x_' + tipo_prova + '.npy')
    y_filename = os.path.join(labels_folder, 'y_' + tipo_prova + '.npy')

    if os.path.exists(x_filename) and os.path.exists(y_filename) and not redo:
        x = np.load(x_filename)
        y = np.load(y_filename)
    else:
        x = np.array([])
        y = np.array([])

        def count_correct_answers(row):
            # print(row[gabarito], " ", row[respostas])
            return sum(a == b for a, b in zip(row[gabarito], row[respostas]))

        for prova in csv_prova:
            df = dh.read_enem(prova)

            df.dropna(subset=[gabarito, respostas, 'NU_NOTA_' + tipo_prova], inplace=True)

            df['correct_answers_' + prova] = df.apply(count_correct_answers, axis=1)

            correct_answ_vector = df['correct_answers_' + prova].values
            grade_vector = df['NU_NOTA_' + tipo_prova]

            x = np.append(x, correct_answ_vector)
            y = np.append(y, grade_vector)

        # Save the data to .npy files
        np.save(x_filename, x)
        np.save(y_filename, y)

    return x, y

if __name__ == '__main__':
    csv_prova = ['enem_data/enem_2016.csv','enem_data/enem_2017.csv','enem_data/enem_2018.csv', 'enem_data/enem_2019.csv', 'enem_data/enem_2020.csv']

    provas = ['CN', 'MT', 'CH', 'LC']

    for prova in provas:
        label_data(prova, csv_prova)
