from google.cloud import automl_v1beta1 as automl
#import pandas as pd
#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.svm import SVC
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import GradientBoostingClassifier
#from sklearn.ensemble import VotingClassifier


def make_prediction_mlauto(df, model_display_name, gcs_output_uri, project_id):
    client = automl.TablesClient(project=project_id)

    # Query model
    response = client.batch_predict(
        pandas_dataframe=df,
        gcs_output_uri_prefix=gcs_output_uri,
        model_display_name=model_display_name
    )
    print("Making batch prediction... ")
    # `response` is a async operation descriptor,
    # you can register a callback for the operation to complete via `add_done_callback`:

    # def callback(operation_future):
    #    result = operation_future.result()
    # response.add_done_callback(callback)
    #
    # or block the thread polling for the operation's results:
    response.result()

    print("Batch prediction complete.\n{}".format(
        response.metadata))


def make_prediction_scikilearn(df):
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
    train = train.drop('split', axis=1)
    features = ['id', 'chars', 'chars_height', 'para_height', 'para_width',
                'para_area', 'para_pos1_x', 'para_pos1_y', 'para_pos2_x', 'para_pos2_y']
    X = train[features]
    y = train['label']
    voting_clf_soft.fit(X, y)
    df_pred = df[features]
    predictions = voting_clf_soft.predict(df_pred)
    df['label'] = predictions

    return df
