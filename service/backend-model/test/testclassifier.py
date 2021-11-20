import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import time

train, test = pd.read_csv('./datasets/traindata.csv'), pd.read_csv('./datasets/test_data.csv')
IDs = test['id']
comment = test['comment_text']

X_train, X_test = train['comment_text'], test['comment_text']
Y_train = train[train.columns[4:]]

tfv = TfidfVectorizer(min_df=3, max_df=0.9, max_features=None,
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                      ngram_range=(1, 2), use_idf=1, smooth_idf=1,
                      sublinear_tf=1, stop_words='english')

tfv.fit(X_train)
X_train = tfv.transform(X_train)
X_test.loc[X_test.isnull()] = " "
X_test = tfv.transform(X_test)

for i in range(Y_train.shape[1]):
    feature = Y_train.columns[i]
    clf = LogisticRegression(C=4.0, solver='sag')
    clf.fit(X_train, Y_train.iloc[:, i])
    exec('pred_{} = pd.Series(clf.predict_proba(X_test).flatten()[1::2])'.format(feature))

submission = pd.DataFrame({
    'toxic': pred_toxic,
    'severe_toxic': pred_severe_toxic,
    'comment': comment,
    'obscene': pred_obscene,
    'threat': pred_threat,
    'insult': pred_insult,
    'identity_hate': pred_identity_hate,
    'none': pred_none
})

submission.to_csv("test_result.csv", index=False)

results = pd.read_csv('test_result.csv')
data = results[results.columns[1:]]

results['max_value'] = data.idxmax(axis=1)


# converting to csv
# should add comment id to the csv file . 
results.to_csv('test_results.csv', index=False)