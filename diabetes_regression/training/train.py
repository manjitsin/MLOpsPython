"""
Copyright (C) Microsoft Corporation. All rights reserved.​
 ​
Microsoft Corporation (“Microsoft”) grants you a nonexclusive, perpetual,
royalty-free right to use, copy, and modify the software code provided by us
("Software Code"). You may not sublicense the Software Code or any use of it
(except to your affiliates and to vendors to perform work on your behalf)
through distribution, network access, service agreement, lease, rental, or
otherwise. This license does not purport to express any claim of ownership over
data you may have shared with Microsoft in the creation of the Software Code.
Unless applicable law gives you more rights, Microsoft reserves all other
rights not expressly granted herein, whether by implication, estoppel or
otherwise. ​
 ​
THE SOFTWARE CODE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
MICROSOFT OR ITS LICENSORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE CODE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import os
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import lightgbm


# Split the dataframe into test and train data
def split_data(data_df):
    features = data_df.drop(['target', 'id'], axis = 1)
    labels = np.array(data_df['target'])
    features_train, features_valid, labels_train, labels_valid = train_test_split(features, labels, test_size=0.2, random_state=0)

    train_data = lightgbm.Dataset(features_train, label=labels_train)
    valid_data = lightgbm.Dataset(features_valid, label=labels_valid, free_raw_data=False)
    
    return (train_data, valid_data)


# Train the model, return the model
def train_model(data, parameters):
    """Train a model with the given datasets and parameters"""
    # The object returned by split_data is a tuple.
    # Access train_data with data[0] and valid_data with data[1]
    
    train_data= data[0]
    valid_data= data[1]
    
    model = lightgbm.train(parameters,
                            train_data,
                            valid_sets=valid_data,
                            num_boost_round=500,
                            early_stopping_rounds=20)
    
    return model


# Evaluate the metrics for the model
def get_model_metrics(model, data):
    """Construct a dictionary of metrics for the model"""
    
    ## TODO
  
    predictions = model.predict(data[1].data)
    fpr, tpr, thresholds = metrics.roc_curve(data[1].label, predictions)
    model_metrics = {"auc": (metrics.auc(fpr, tpr))}
    print(model_metrics)

    return model_metrics


def main():
    """This method invokes the training functions for development purposes"""
    
    # Read data from a file
    data_df = pd.read_csv('porto_seguro_safe_driver_prediction_input.csv')

    # Hard code the parameters for training the model
    parameters = {
        'learning_rate': 0.05,
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'auc',
        'sub_feature': 0.7,
        'num_leaves': 60,
        'min_data': 100,
        'min_hessian': 1,
        'verbose': 2
    }

    data = split_data(data_df)

    # Call the functions defined in this file
    model = train_model(data, parameters)
    
    # Print the resulting metrics for the model
    metrics = get_model_metrics(model, data)


if __name__ == '__main__':
    main()
