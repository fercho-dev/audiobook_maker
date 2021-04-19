import pandas as pd
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier


knn = KNeighborsClassifier(n_neighbors=7)
svc_rbf = SVC(probability=True)
svc_poly = SVC(kernel='poly', probability=True)
rf = RandomForestClassifier(n_estimators=100)
gbc = GradientBoostingClassifier(n_estimators=150, random_state=0)
voting_clf_soft = VotingClassifier(estimators=[('svc_rbf', svc_rbf), ('svc_poly', svc_poly),
                                               ('knn', knn), ('rf', rf), ('gbc', gbc)],
                                   voting='soft')
# fitting the data
train = pd.read_csv('./training_data_1.csv')
train = df.drop('split', axis=1)
features = ['id', 'chars', 'chars_height', 'para_height', 'para_width',
            'para_area', 'para_pos1_x', 'para_pos1_y', 'para_pos2_x', 'para_pos2_y']
X = df[features]
y = df['label']
voting_clf_soft.fit(X, y)
