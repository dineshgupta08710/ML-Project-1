import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.exception import CustomException
from src.logger import logging
from src.utils import save_objects

@dataclass
class DataTransformationConfig: #  it will give me any path/inputs that I will probably be requiring for data tranformation
    preprocessor_ob_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
            This function is resposible for data transformation.
        '''
        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            # Numerical pipeline
            num_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="median")), # median :- replace missing values using the median along each column
                    # An imputer is a tool or technique used in data preprocessing to fill in missing values in a dataset.

                    ("scaler", StandardScaler()) # It will do standard scaling
                ]
            )

            # Categorical pipeline
            cat_pipeline = Pipeline(
                steps = [
                    ("imputer", SimpleImputer(strategy="most_frequent")), # most_frequent :- replace missing values using the mode along each column
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info("Numerical column standard scaling completed")
            logging.info("Categorical column encoding completed")

            # Combine Numerical & categorical pipeline by ColumnTransformer
            preprocessor = ColumnTransformer(
                 transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ( "cat_pipeline",cat_pipeline, categorical_columns)
                 ]
             )
            
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math_score"
            numerical_column = ["writing_score", "reading_score"]
            
            # Train data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1) # Input features :- all features excluding target feature(math_score)
            target_feature_train_df = train_df[target_column_name]
            # Test data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training and testing dataframe"
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[ # np.c_ :-> concatenate along columns
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            # Saving pkl file
            save_objects(
                file_path = self.data_tranformation_config.preprocessor_ob_file_path, #pkl file path
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_ob_file_path #pkl file path
            )
        
        except Exception as e:
            raise CustomException(e, sys)