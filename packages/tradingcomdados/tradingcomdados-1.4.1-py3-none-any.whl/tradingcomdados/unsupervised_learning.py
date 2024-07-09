import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.cluster import PCA
from sklearn.manifold import TSNE


def transform_missings_data(
    df: pd.DataFrame, fill_numerical: float, fill_categorical: str
):
    """
    This function is responsable for fill missings in dataFrame for numerical and categorical features with the substitution value passed by the user.
    
    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :param fill_numerical: The value that will be used to fill the NaNs for numerical features
    :type: float
    :param fill_categorical: The value that will be used to fill the NaNs for categorical features
    :type: str
    :return: The final DataFrame with no missings
    :rtype: DataFrame
    """

    if fill_numerical is not None:
        numerical_data = get_numerical_data(df)

    if fill_categorical is not None:
        categorical_data = get_categorical_data(df)

    numerical_data = numerical_data.fillna(fill_numerical)
    categorical_data = categorical_data.fillna(fill_categorical)

    df = _merge_num_cat(numerical_data, categorical_data)

    return df



def _merge_num_cat(numerical_data, categorical_data):

    df = pd.merge(numerical_data, categorical_data, left_index=True, right_index=True)

    return df



def get_categorical_data(df: pd.DataFrame):
    """
    This function is responsable for the identification of categorical and date features.
    
    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :return: DataFrame with only categorical and date data types
    :rtype: DataFrame
    """
    categorical_data = df.select_dtypes(
        include=["object", "category", "datetimetz", "datetime", "timedelta"]
    )

    return categorical_data



def get_numerical_data(df: pd.DataFrame):
    """
    This function is responsable for the identification of numerical features.
    
    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :return: DataFrame with only numerical data types
    :rtype: DataFrame
    """
    numerical_data = df.select_dtypes(include=["number", "float64", "int64"])

    return numerical_data



def transform_numerical_data(df: pd.DataFrame):
    """
    The objective here is to transform numerical features for clustering techniques.

    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :return: DataFrame that contains all the features transformed
    :rtype: DataFrame
    """
    scale = StandardScaler(with_mean=True)
    df_scale = scale.fit_transform(df)
    df_result = pd.DataFrame(df_scale, columns=df.columns)

    return df_result



def transform_categorical_data(df: pd.DataFrame):
    """
    The objective here is to transform categorical features for specific clustering techniques, such as: Kmodes, KPrototypes but not limited to it.

    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :return: DataFrame that contains all the features transformed
    :rtype: DataFrame
    """

    categorical_data = get_categorical_data(df)
    le = LabelEncoder()
    df_result = categorical_data.apply(le.fit_transform)

    return df_result



def _process_data_clustering(df: pd.DataFrame, algorithm: object, id: str):
    df.index = df[id]
    df = df.drop(columns=id)

    numerical_data = get_numerical_data(df)

    if algorithm == KMeans or AgglomerativeClustering or DBSCAN:
        df_model = transform_numerical_data(numerical_data)

    return df, df_model



def clustering_pipeline(algorithm: object, df: pd.DataFrame, id: str):
    """
    Clustering pipeline is developed for the end-to-end clustering cycle. It can process the features, fit and predict the cluster for each row and finally score the results in a new column to the dataFrame.

    :param algorithm: The clustering object
    :type: object
    :param df: Pandas DataFrame that is given as the features to be clustered
    :type: pd.DataFrame
    :param id: Id is the key identification of the dataFrame
    :type: str
    :return: DataFrame that contains the results for the chosen clustering technique
    :rtype: DataFrame
    """

    df, df_model = _process_data_clustering(df, algorithm, id)

    df[algorithm] = algorithm.fit_predict(df_model)

    return df


def check_sillouette(algorithm: object, test_range: list, df: pd.DataFrame, id: str):
    """
    Sihouette score test that can be performed for the range given as test_range attribute, the result is a informative print of number of cluster and the score itself for all iteration.

    :param algorithm: The clustering object
    :type: object
    :param test_range: The list of range numbers used to each test
    :type: list
    :param df: Pandas DataFrame that is given as the features to be clustered
    :type: pd.DataFrame
    :param id: Id is the key identification of the dataFrame
    :type: str
    """

    df, df_model = _process_data_clustering(df, algorithm, id)

    for num_cluster in test_range:
        algo = algorithm(n_clusters=num_cluster)
        prediction = algo.fit_predict(df_model)

        score = silhouette_score(df_model, prediction)
        print(
            f"The silhouette_score value is {score}, for the number of clusters equals to {num_cluster}"
        )


def pca_transform(df: pd.DataFrame, n_components: int):
    """
    The PCA transformation is used to reduce the number of features in the dataset.

    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :param n_components: The number of components that will be used in the PCA transformation
    :type: int
    :return: DataFrame that contains all the features transformed
    :rtype: DataFrame
    """

    pca = PCA(n_components=n_components)
    df_pca = pca.fit_transform(df)

    return df_pca

def tsne_transform(df: pd.DataFrame, n_components: int):
    """
    The t-SNE transformation is used to reduce the number of features in the dataset.

    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :param n_components: The number of components that will be used in the t-SNE transformation
    :type: int
    :return: DataFrame that contains all the features transformed
    :rtype: DataFrame
    """

    tsne = TSNE(n_components=n_components)
    df_tsne = tsne.fit_transform(df)

    return df_tsne


def isolation_forest(df: pd.DataFrame, contamination: float):
    """
    The isolation forest is used to detect outliers in the dataset.

    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :param contamination: The percentage of contamination that will be used in the isolation forest
    :type: float
    :return: DataFrame that contains the results for the chosen clustering technique
    :rtype: DataFrame
    """

    from sklearn.ensemble import IsolationForest

    iso = IsolationForest(contamination=contamination)
    df["outliers"] = iso.fit_predict(df)

    return df

def dbscan_clustering(df: pd.DataFrame, id: str, eps: float, min_samples: int):
    """
    DBSCAN clustering is used to cluster the dataset.

    :param df: Pandas DataFrame
    :type: pd.DataFrame
    :param id: Id is the key identification of the dataFrame
    :type: str
    :param eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other
    :type: float
    :param min_samples: The number of samples in a neighborhood for a point to be considered as a core point
    :type: int
    :return: DataFrame that contains the results for the chosen clustering technique
    :rtype: DataFrame
    """

    df.index = df[id]
    df = df.drop(columns=id)

    numerical_data = get_numerical_data(df)

    df_model = transform_numerical_data(numerical_data)

    df["dbscan"] = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(df_model)

    return df