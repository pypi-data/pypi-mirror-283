import optuna
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    RandomForestClassifier,
    GradientBoostingClassifier,
    DecisionTreeClassifier,
    DecisionTreeRegressor,
)
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.svm import SVR, SVC
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np


class TuningHyperparameters:
    """
    This class is responsable for tuning the hyperparameters of a model using Optuna.

    """


    def __init__(self, problem_type, model_name, metric):
        self.problem_type = problem_type
        self.model_name = model_name
        self.metric = metric

    def objective(self, trial, x, y):
        """
        This function is responsable for defining the objective function for the optimization.

        :param trial: optuna trial
        :type: object
        :param x: features
        :type: np.array
        :param y: target
        :type: np.array
        :return: metric
        :rtype: float
        
        """
        
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, random_state=42
        )
        model = TuningHyperparameters.model_selection(
            self.problem_type, self.model_name
        )
        model.fit(x_train, y_train)

        if self.problem_type == "classification":
            result = model.predict(x_test, y)
        elif self.problem_type == "regression":
            result = model.predict(x_test, y)

        performance = TuningHyperparameters.evaluation(y_test, result)

        return performance

    def evaluation(self, y_test, y_pred):
        """
        This function is responsable for evaluating the model based on the metric and problem type.

        :param y_test: target test
        :type: np.array
        :param y_pred: predicted target
        :type: np.array
        :return: performance
        :rtype: float
    
        
        """
        if self.problem_type == "classification":
            if self.metric == "accuracy":
                return accuracy_score(y_test, y_pred)
            elif self.metric == "precision":
                return precision_score(y_test, y_pred)
            elif self.metric == "recall":
                return recall_score(y_test, y_pred)
            elif self.metric == "f1":
                return f1_score(y_test, y_pred)
            else:
                print(
                    "Metric not found. Please choose between: accuracy, precision, recall, f1"
                )

        elif self.problem_type == "regression":
            if self.metric == "mse":
                return mean_squared_error(y_test, y_pred)
            elif self.metric == "mae":
                return mean_absolute_error(y_test, y_pred)
            elif self.metric == "rmse":
                return mean_squared_error(y_test, y_pred, squared=False)
            elif self.metric == "r2":
                return r2_score(y_test, y_pred)
            else:
                print("Metric not found. Please choose between: mse, mae, rmse, r2")

        return self.metric(y_test, y_pred)

    def model_selection(problem_type, model_name):
        """
        This function is responsable for selecting the model based on the problem type and model name.

        :param problem_type: classification or regression
        :type: str
        :param model_name: name of the model
        :type: str
        :return: model
        :rtype: object
        
        """
        if problem_type == "classification":
            if model_name == "random_forest":
                return RandomForestClassifier()
            elif model_name == "tree":
                return DecisionTreeClassifier()
            elif model_name == "gradient_boosting":
                return GradientBoostingClassifier()
            elif model_name == "mlp":
                return MLPClassifier()
            elif model_name == "svm":
                return SVC()
            elif model_name == "xgboost":
                return XGBClassifier()
            else:
                print(
                    "Model not found. Please choose between: random_forest, tree, gradient_boosting, mlp, svm, xgboost"
                )
        elif problem_type == "regression":
            if model_name == "random_forest":
                return RandomForestRegressor()
        elif model_name == "tree":
            return DecisionTreeRegressor()
        elif model_name == "gradient_boosting":
            return GradientBoostingRegressor()
        elif model_name == "mlp":
            return MLPRegressor()
        elif model_name == "svm":
            return SVR()
        elif model_name == "xgboost":
            return XGBRegressor()
        else:
            print(
                "Model not found. Please choose between: random_forest, tree, gradient_boosting, mlp, svm, xgboost"
            )

    def tuning_hyperparameters(X, y, objective, direction, n_trials=100):
        """
        This function is responsable for tuning the hyperparameters of a model using Optuna.
        
        :param X: pandas DataFrame with the features
        :type: pd.DataFrame
        :param y: pandas Series with the target
        :type: pd.Series
        :param objective: function that will be optimized
        :type: function
        :param direction: maximize or minimize the objective function
        :type: str
        :param n_trials: number of trials for the optimization
        :type: int
        :return: best hyperparameters
        rtpe: dict
        
        """

        study = optuna.create_study(direction=direction)
        study.optimize(objective, n_trials=n_trials)
        return study.best_params
