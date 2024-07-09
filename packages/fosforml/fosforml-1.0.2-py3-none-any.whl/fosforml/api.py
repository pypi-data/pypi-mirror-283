# -*- coding: utf-8 -*-
import base64
import json
import os
import shutil
import tempfile
import uuid
import pandas as pd
import platform
import requests
import snowflake
from .validators import *
from fosforml.widgets.registered_output import ModelDescribe
import logging as log
from .model_manager import ModelRegistry

def register_model(
    model_obj,
    session,
    scoring_func,
    name,
    description,
    flavour,
    y_true=None,
    y_pred=None,
    prob=None,
    model_type=None,
    conda_dependencies=[],
    x_train=None,
    y_train=None,
    x_test=None,
    y_test=None,
    pretty_output=False,
    metadata=None,
    **kwargs
):
    """
    Register model to the mosaic ai server

    Args:
        model_obj (object): model to be registered
        scoring_func (function): function to be used for scoring
        name (string): name of the model
        description (string): description of the model
        flavour (string): flavour of the model eg: keras, pytorch, tensorflow etc
        tags (array of strings): user tags associated with the model
        schema (Dict): input and output schema structure for scoring function
        y_true: array, shape = [n_samples]
        y_pred : array, shape = [n_samples]
        prob : array-like of shape (n_samples,)
        features : dummy feature names
        labels: predicted labels
        feature_names : all features
        model_type(string): type of the model eg: classification, regression etc
        datasource_name(string):
        metadata_info: metadata information about the version
        x_train (numpy array) : training data of model with feature column
        x_test (numpy array) :  test data of model with feature column
        y_train (numpy array) : training data of model with target column
        y_test (numpy array) : test data of model with target column
        kyd (bool)  :
            If True will generate Know your data Data Drift for the model.

            Once model registered import global variable for viewing InNotebook result.
            from fosforml.api import kyd_executor
            kyd_executor.kyd_client.fallback_display()
        kyd_score (bool) :
            if True will generate drift score for the model.
        pretty_output (bool):
            if True returns widget after registeration else dictionary
    Optional:
        explicit_x_train:
            :pd.DataFrame or np.ndarray
            Explicit x_train clean raw data.
            if Provided the following algorithm will automatically pickup for its executions:
                - Know Your Data : explicit_x_train is used for extraction of knowledge. x_train is still used internally.
        explicit_x_test:
            :pd.DataFrame or np.ndarray
            Explicit x_test clean raw data.
            if Provided the following algorithm will automatically pickup for its executions:
                - Know Your Data : explicit_x_test is used for extraction of knowledge. x_test is still used internally.
        explicit_feature_names:
            :list
            Feature Names for The Explicit Provided Data.
        source:
            :string
            Value will be automl if model registered from automl else None
        model_display
            :bool
            If true display model on model list

    Returns:

    """

    
    valid_datasets,message_ = validate_datasets_for_sf(x_train, y_train, x_test, y_test, y_pred,prob)
    if valid_datasets is False:
        return message_

    source = kwargs.get("source") if kwargs.get("source") else None
    model_display = kwargs.get("model_display")
    if model_display is None:
        model_display = True
    
    if not session or not isinstance(session,snowflake.snowpark.session.Session):
        return False,"Invalid session object."

    # register model
    model_registry = ModelRegistry(session=session)
    model_status,response = model_registry.register_model(
        model=model_obj,
        score=None,
        model_name=name,
        conda_dependencies=conda_dependencies,
        description=description,
        model_flavour=flavour,
        model_type=model_type,
        x_train=x_train,
        y_train=y_train,
        x_test=x_test,
        y_test=y_test,
        y_pred=y_pred,
        prob=prob,
        python_version=platform.python_version(),
        source=None,
        metadata=metadata
    )

    return response


def validate_datasets_for_sf(x_train, y_train, x_test, y_test, y_pred, prob):
    if x_train is not None and not isinstance(x_train, (pd.DataFrame, pd.Series,snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("x_train must be a DataFrame")
    if y_train is not None and not isinstance(y_train, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("y_train must be a Series")
    if x_test is not None and not isinstance(x_test, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("x_test must be a DataFrame")
    if y_test is not None and not isinstance(y_test, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("y_test must be a Series")
    if y_pred is not None and not isinstance(y_pred, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("y_pred must be a Series")
    if prob is not None and not isinstance(prob, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("prob must be a Series")
    
    return True, "All datasets are valid"

def validate_dataset(dataset):
    if dataset is not None and not isinstance(dataset, (pd.DataFrame, pd.Series, snowflake.snowpark.dataframe.DataFrame)):
        raise ValueError("Dataset must be a DataFrame or Series")
