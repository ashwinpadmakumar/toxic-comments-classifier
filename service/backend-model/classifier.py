import pandas as pd
import pickle
import sys
import os

BASE_PATH = '/home/ashwin/Downloads/project/Functionality'
train = pd.read_csv('{}/datasets/traindata.csv'.format(BASE_PATH))

comment = sys.argv[1]
X_test = [comment]

Y_train = train[train.columns[4:]]

loaded_fit = pickle.load(open('{}/fit_model.sav'.format(BASE_PATH), 'rb'))
X_test = loaded_fit.transform(X_test)

for i in range(Y_train.shape[1]):
    feature = Y_train.columns[i]
    loaded_model = pickle.load(open('{}/model_{}.sav'.format(BASE_PATH,feature), 'rb'))
    exec('pred_{} = pd.Series(loaded_model.predict_proba(X_test).flatten()[1::2])'.format(feature))

submission = pd.DataFrame({
    'comment': comment,
    'toxic': pred_toxic,
    'severe_toxic': pred_severe_toxic,
    'obscene': pred_obscene,
    'threat': pred_threat,
    'insult': pred_insult,
    'identity_hate': pred_identity_hate,
    'none': pred_none
})


submission.to_csv('/{}/result.csv'.format(BASE_PATH), index=False)
print(submission.idxmax(axis=1).get(0))
