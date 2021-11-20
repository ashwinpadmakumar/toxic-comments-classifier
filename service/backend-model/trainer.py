import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

train = pd.read_csv('./datasets/traindata.csv')

X_train = train['comment_text']
Y_train = train[train.columns[4:]]


tfv = TfidfVectorizer(min_df=3, max_df=0.9, max_features=None,
                      strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                      ngram_range=(1, 2), use_idf=1, smooth_idf=1,
                      sublinear_tf=1, stop_words='english')

tfv.fit(X_train)

#saving fit model
filename = "fit_model.sav"                      
pickle.dump(tfv,open(filename,'wb'))
loaded_fit = pickle.load(open('fit_model.sav','rb'))

X_train = loaded_fit.transform(X_train)

#saving seven model
for i in range(Y_train.shape[1]):
    feature = Y_train.columns[i]
    clf = LogisticRegression(C=4.0, solver='sag')
    clf.fit(X_train, Y_train.iloc[:, i])
    filename = 'model_{}.sav'.format(feature)
    pickle.dump(clf,open(filename,'wb'))


