
# Add New Model To Framework

## Table of Contents

- [1. Understand the machine learning algorithm](#1-understand-the-model)

- [2. Construct A Model (Algorithm Workflow) Class](#2-add-model)
  - [2.1 Add The Model Class](#21-add-the-model-class)
    - [2.1.1 Find Add File](#211-find-add-file)
    - [2.1.2 Define class properties and constructors, etc.](#212-define-class-properties-and-constructors-etc)
    - [2.1.3 Define manual\_hyper\_parameters](#213-define-manual_hyper_parameters)
    - [2.1.4 Define special\_components](#214-define-special_components)

  - [2.2 Add AutoML](#22-add-automl)
    - [2.2.1 Add AutoML code to class](#221-add-automl-code-to-class)

  - [2.3 Get the hyperparameter value through interactive methods](#23-get-the-hyperparameter-value-through-interactive-methods)
    - [2.3.1 Find file](#231-find-file)
    - [2.3.2 Create the .py file and add content](#232-create-the-py-file-and-add-content)
    - [2.3.3 Import in the file that defines the model class](#233-import-in-the-file-that-defines-the-model-class)

  - [2.4 Call Model](#24-call-model)
    - [2.4.1 Find file](#241-find-file)
    - [2.4.2 Import module](#242-import-module)
    - [2.4.3 Call model](#243-call-model)

  - [2.5 Add the algorithm list and set NON\_AUTOML\_MODELS](#25-add-the-algorithm-list-and-set-non_automl_models)
    - [2.5.1 Find file](#251-find-file)

  -  [2.6 Add Functionality](#26-add-functionality)

      - [2.6.1 Model Research](#261-model-research)

     - [2.6.2 Add Common_component](#262-add-common_component)

      - [2.6.3 Add Special_component](#263-add-special_component)

- [3. Test model](#3-test-model)

- [4. Completed Pull Request](#4-completed-pull-request)

- [5. Precautions](#5-precautions)


## 1. Understand Machine Learning Algorithm
You need to understand the general meaning of the machine learning algorithm. Then you encapsultate it as an algorithm workflow in our framework and put it under the directory `geochemistrypi/data_mining/model`. Then you need to determine which **mode** this algorithm belongs to and the role of each parameter. For example, linear regression algorithm belongs to regression mode in our framework.
+ **Notice**: in our framework, a model class refers to an algorithm workflow class and a mode includes multiple models class.
+ When learning the ML algorithm, you can refer to the relevant knowledge on the [scikit-learn official website](https://scikit-learn.org/stable/index.html).


## 2. Construct Model (Algorithm Workflow) Class

**Noted**: You can reference any existing model classes in our framework to implement your own model class. 

### 2.1 Add Basic Elements

#### 2.1.1 Find File
First, you need to construct the algorithm workflow class in the corresponding model file. The corresponding model file locates under the path `geochemistrypi/data_mining/model`.

![image1](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/3c7d4e53-1a99-4e7e-87b6-fdcb94a9e510)

**E.g.,** If you want to add a model for the regression mode, you need to add it in the `regression.py` file.


#### 2.1.2 Define Class Attributes and Constructor
(1) Define the algorithm workflow class and its Base class
```
class ModelClassName(BaseModelClassName):
```
+ You can refer to the ModelName of other models, the format (Upper case and with the suffix 'Corresponding Mode') needs to be consistent. E.g., `XGBoostRegression`.
+ Base class needs to be inherited according to the mode the model belongs to.

```
"""The automation workflow of using "ModelClassName" algorithm to make insightful products."""
```
+ Class docstring, you can refer to other classes. The template is shown above.

(2) Define the class attributes `name` and `special_function`

```
name = "algorithm terminology"
```
+ The class attributes `name` is different from ModelClassName. E.g., `XGBoost`
+ This name needs to be added to the corresponding constant variable in `geochemistrypi/data_mining/constants.py` file and the corresponding mode processing file under the `geochemistrypi/data_mining/process` folder. Note that those name value should be identical.
+ For example, the name value `XGBoost` should be included in the constant varible `REGRESSION_MODELS` in `geochemistrypi/data_mining/constants.py` file and it will be use in `geochemistrypi/data_mining/process/regress.py`.
```
special_function = []
```
+ the values of special_function are the description of the owned functionalities of that specific model. Those special functions cannot be reused by other models. You can refer to the existed models. E.g., `special_function = ["Feature Importance Diagram"]` in the model class `XGBoostRegression`. 
+ Noted that in base class, there is a class attribute `common_function`. E.g, `common_function = ["Model Score", "Cross Validation", "Model Prediction", "Model Persistence", "Predicted vs. Actual Diagram", "Residuals Diagram", "Permutation Importance Diagram"]` in the base class `RegressionWorkflowBase`. It means the children class (all regession models) can share the same common functionalies as well.

(3) Define the signature of the constructor
```
def __init__(
       self,
       parameter: type = Default parameter value,
    ) -> None:
```
+ The parameters in the constructor is from the algorithm library you depend on. For example, you use **Lasso** algorithm from Sckit-learn library. You can reference its introduction ([Lasso](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html)) in Scikit-learn website.
+ Default parameter value needs to be set according to scikit-learn official documents also.

![image2](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/0f02b7bb-bef1-4b56-9c84-6162e86e2093)


```
"""
Parameters
----------
parameter: type，default = Dedault

References
----------
Scikit-learn API: sklearn.model.name
https://scikit-learn.org/......
```
+ Parameters docstring are in the source code of the corresponding algorithm on the official website of sklearn.

![image3](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/0926a7e5-7243-4f4b-a3bb-bc4393b9633d)


(4) The constructor of Base class is called
```
super().__init__()
```

(5) Initializes the instance's state by assigning the parameter values passed to the constructor to the instance's attributes.
```
self.parameter=parameter
```

(6) Instantiate the algorithm class you depend on and assign. For example, `Lasso` from the library `sklearn.linear_model`.
```
self.model = modelname(
  parameter=self.parameter
)
```
**Note:** Don't forget to import the class from scikit-learn library

![image4](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/38e64144-fa19-4ef2-83d1-709504ba8001)

(7) Define the instance attribute `naming`
```
self.naming = Class.name
```
This one will be use to print the name of the class and to activate the AutoML functionality. E.g, `self.naming = LassoRegression.name`. Further explaination is in section 2.2.

(8) Define the instance attribute  `customized` and `customized_name`
```
self.customized = True
self.customized_name = "Algorithm Name"
```
These will be use to leverage the customization of AutlML functionality. E.g,`self.customized_name = "Lasso"`. Further explaination is in section 2.3.

(9) Define other instance attributes
```
self.attributes=...
```


### 2.2 Add Manual Hyperparameter Tuning Functionality

Our framework provides the user to set the algorithm hyperparameter manually or automiacally. In this part, we implement the manual functionality.

Sometimes the users want to input the hyperparameter values for model training manually, so you need to establish an interaction way to get the user's input.

#### 2.2.1 Define manual_hyper_parameters Method

The manual operation is control by the **manual_hyper_parameters** method. Inside this method, we encapsulate a lower level service function called algorithm_manual_hyper_parameters().

```
@classmethod
def manual_hyper_parameters(cls) -> Dict:
    """Manual hyper-parameters specification."""
    print(f"-*-*- {cls.name} - Hyper-parameters Specification -*-*-")
    hyper_parameters = algorithm_manual_hyper_parameters()
    clear_output()
    return hyper_parameters
```

+ The **manual_hyper_parameters** method is called in the corresponding mode operation file under the `geochemistrypi/data_mining/process` folder.

+ This lower level service function locates in the `geochemistrypi/data_mining/model/func/specific_mode` folder  which limits the hyperparameters the user can set manually. E.g., If the model class `LassoRegression` belongs to the regression mode, you need to add the `_lasso_regression.py` file under the folder `geochemistrypi/data_mining/model/func/algo_regression`. Here, `_lasso_regression.py` contains all encapsulated service functions specific to lasso algorithm.
![image5](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/9d7b44d0-fd85-4a6a-a2a8-3f531475f3f6)

#### 2.2.2 Create .py File and Add Service Function

(1) Create a _algorithm.py file
**Note:** Keep name format consistent.

(2) Import module
```
from typing import Dict
from rich import print
from ....constants import SECTION
```
+ In general, these modules need to be imported
```
from ....data.data_readiness import bool_input, float_input, num_input
```
+ You needs to choose the appropriate common utility functions according to the input type of hyperparameter.

(3) Define the service function
```
def algorithm_manual_hyper_parameters() -> Dict:
```

(4) Interactive format
```
print("Hyperparameters: Explaination")
print("A good starting value ...")
Hyperparameters = type_input(Default Value, SECTION[2], "@Hyperparameters: ")
```
**Note:** You can query ChatGPT for the recommended good starting value. The default value can come from that one in the imported library. For example, check the default value of the specific parameter for `Lasso` algorithm in [Scikit-learn Website](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html).

(5) Integrate all hyperparameters into a dictionary type and return.
```
hyper_parameters = {
        "Hyperparameters1": Hyperparameters1,
        "Hyperparameters": Hyperparameters2,
}
retuen hyper_parameters
```

#### 2.2.3 Import in The Model Class File
```
from .func.algo_mode._algorithm.py import algorithm_manual_hyper_parameters
```
![image6](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/27e74d2c-8539-41e6-bca9-f0dd50d4ed74)


### 2.3 Add Automated Hyperparameter Tuning (AutoML) Functionality

#### 2.3.1 Add AutoML Code to Model Class

Currently, only supervised learning modes (regression and classification) support AutoML. Hence, only the algorithm belonging to these two modes need to implment AutoML functionality.

Our framework leverages FLAML + Ray to build the AutoML functionality. For some algorithms, FLAML has encapsulated them. Hence, it is easy to operate with those built-in algorithm. However, some algorithms without encapsulation needs our customization on our own.

There are three cases in total:
+ C1: Encapsulated -> FLAML (Good example: `XGBoostRegression` in `regression.py`)
+ C2: Unencapsulated -> FLAML (Good example: `SVMRegression` in `regression.py`)
+ C3: Unencapsulated -> FLAML + RAY (Good example: `MLPRegression` in `regression.py`)

Here, we only talk about 2 cases, C1 and C2. C3 is a special case and it is only implemented in MLP algorithm.

Noted:

+ The calling method **fit** is defined in the base class, hence, no need to define it again in the specific model class. You can refrence the **fit** method of `RegressionWorkflowBase` in `regression.py`


The following two steps is needed to implement AutoML functionality in the model class. But for C1 it only requires the first step while C2 needs two step both.

(1)  Create `settings` method
```
    @property
    def settings(self) -> Dict:
        """The configuration of your model to implement AutoML by FLAML framework."""
        configuration = {
            "time_budget": '...'
            "metric": '...',
            "estimator_list": '...'
            "task": '...'
        }
        return configuration
```
+ "time_budget" represents total running time in seconds
+ "metric" represents Running metric
+ "estimator_list" represents list of ML learners
+ "task" represents task type

For C1, the value of "estimator_list" should come from the specified name in [FLAML library](https://microsoft.github.io/FLAML/docs/Use-Cases/Task-Oriented-AutoML). For example, the specified name `xgboost` in the model class `XGBoostRegression`. Also we need to put this specified value inside a list.

<img width="1274" alt="image" src="https://github.com/ZJUEarthData/geochemistrypi/assets/47497750/3287fefa-3986-4b98-9746-fb2f348fa7e7">

For C2, the value of "estimator_list" should be the instance attribute `self.customized_name`. For example, `self.customized_name = "SVR"` in the model class `SVMRegression`. Also we need to put this specified value inside a list.

**Note:** You can keep the other key-value pair consistent with other exited model classes.

(2) Create `customization` method
You can add the parameter tuning code according to the following code:
```
    @property
    def customization(self) -> object:
        """The customized 'Your model' of FLAML framework."""
        from flaml import tune
        from flaml.data import 'TPYE'
        from flaml.model import SKLearnEstimator
        from 'sklearn' import 'model_name'

        class 'Model_Name'(SKLearnEstimator):
            def __init__(self, task=type, n_jobs=None, **config):
                super().__init__(task, **config)
                if task in 'TYPE':
                    self.estimator_class = 'model_name'

            @classmethod
            def search_space(cls, data_size, task):
                space = {
                    "'parameters1'": {"domain": tune.uniform(lower='...', upper='...'), "init_value": '...'},
                    "'parameters2'": {"domain": tune.choice([True, False])},
                    "'parameters3'": {"domain": tune.randint(lower='...', upper='...'), "init_value": '...'},
                }
                return space

        return "Model_Name"
```
**Note1:** The content in ' ' needs to be modified according to your specific code. You can reference that one in the model class `SVMRegression`.
**Note2:**
```
                space = {
                    "'parameters1'": {"domain": tune.uniform(lower='...', upper='...'), "init_value": '...'},
                    "'parameters2'": {"domain": tune.choice([True, False])},
                    "'parameters3'": {"domain": tune.randint(lower='...', upper='...'), "init_value": '...'},
                }
```

+ tune.uniform represents float
+ tune.choice represents bool
+ tune.randint represents int
+ lower represents the minimum value of the range, upper represents the maximum value of the range, and init_value represents the initial value
**Note:** You need to select parameters based on the actual situation of the model


### 2.4 Add Application Function to Model Class

We treat the insightful outputs (index, scores) or diagrams to help to analyze and understand the algorithm as useful application. For example, XGBoost algorithm can produce feature importance score, hence, drawing feature importance diagram is an application function we can add to the model class `XGBoostRegression`. 

Conduct research on the corresponding model and confirm the functions that need to be added.

+ You can confirm the functions that need to be added on the official website of the model (such as scikit learn), search engines (such as Google), chatGPT, etc.

(1) Common_component is a public function in a class, and all functions in each class can be used, so they need to be added in the parent class，Each of the parent classes can call Common_component.

(2) Special_component is unique to the model, so they need to be added in a specific model，Only they can use it.

![Image1](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/3f983a7a-3b0d-4c7b-b7b7-31b317f4d9d0)


#### 2.4.1 Add Special Application Functions

Each algorithms has their own characteristics. Hence, they have different special fucntionalities as well. For example, for KMeans algorithm, we can get the inertia scores from it. Hence, inside the model class `KMeansClustering`, we have a **private** instance method `_get_inertia_scores`.

#### Define `special_components` method

Inside this method, you need to invoke all special application functions for this algorithms. For example, inside the `special_components` method of the model class `KMeansClustering`, the application function `_get_inertia_scores` will be called.

```
def _get_inertia_scores(self, algorithm_name: str, store_path: str) -> None:
    ...

def special_components(self, **kwargs: Union[Dict, np.ndarray, int]) -> None:
    self._get_inertia_scores(...)
    ...
```

Howerever, there are two different scenarios when defining `special_component` method. Is is needed because we need to differentiate AutoML and manuanl ML. It leverages the thought of method overloading which is not supported by Python natively but we can achieve it through a library **multipledispatch**.




a.The multi-dispatch function is different
Scikit-learn framework：@dispatch()
FLAML framework：@dispatch(bool)

b.Added 'is_automl: bool' to the def
**eg:**
```
Scikit-learn framework：
def special_components(self, **kwargs) -> None:

FLAML framework：
def special_components(self, is_automl: bool, **kwargs) -> None:
```
c.self.model has a different name
**eg:**
```
Scikit-learn framework：
coefficient=self.model.coefficient

FLAML framework：
coefficient=self.auto_model.coefficient
```

**Note:** The content of this part needs to be selected according to the actual situation of your own model.Can refer to similar classes.

```
GEOPI_OUTPUT_ARTIFACTS_IMAGE_MODEL_OUTPUT_PATH = os.getenv("GEOPI_OUTPUT_ARTIFACTS_IMAGE_MODEL_OUTPUT_PATH")
```
+ This line of code gets the image model output path from the environment variable.
```
GEOPI_OUTPUT_ARTIFACTS_PATH = os.getenv("GEOPI_OUTPUT_ARTIFACTS_PATH")
```
+ This line of code takes the general output artifact path from the environment variable.
**Note:** You need to choose to add the corresponding path according to the usage in the following functions.

+ Also, if only part of the models share a functionality, for example, feature importance in tree-based algorithm including XGBoost, Decision Tree, etc, you can create a Mixin class and let the model class inherit it.

**Note:** You can refer to other similar codes to complete your code.


### 2.4 Call Model

#### 2.4.1 Find file
Call the model in the corresponding file in the `process` folder. The corresponding algorithm file is in the `process` folder in the` model` folder in the `data_mining` folder in the `geochemistrypi` folder.

![image7](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/36e8f6ee-ae21-4f86-b000-0a373ea63cca)

**eg:** If your model belongs to the regression,you need to call it in the regress.py file.

#### 2.4.2 Import module
You need to add your model in the from ..model.regression import().
```
from ..model.regression import(
  ...
  NAME,
)
```
**Note:** NAME needs to be the same as the NAME when defining the class in step 2.1.2.
**eg:**

![image8](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/36fabb07-10b0-419a-b31d-31c036493b7b)

#### 2.4.3 Call model
There are two activate methods defined in the Regression and Classification algorithms, the first method uses the Scikit-learn framework, and the second method uses the FLAML and RAY frameworks. Decomposition and Clustering algorithms only use the Scikit-learn framework. Therefore, in the call, Regression and Classification need to add related codes to implement the call in both methods, and only one time is needed in Clustering and Decomposition.

(1) Call model in the first activate method(Including Classification, Regression,Decomposition,Clustering)
```
elif self.model_name == "name":
            hyper_parameters = NAME.manual_hyper_parameters()
            self.dcp_workflow = NAME(
                Hyperparameters1=hyper_parameters["Hyperparameters2"],
                Hyperparameters1=hyper_parameters["Hyperparameters2"],
                ...
            )
```
+ The name needs to be the same as the name in 2.4
+ The hyperparameters in NAME() are the hyperparameters obtained interactively in 2.2
**eg:**
![image9](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/d4d3c208-e7a5-4e5c-a403-1fa6646bf7a7)

（2）Call model in the second activate method（Including Classification, Regression）
```
elif self.model_name == "name":
  self.reg_workflow = NAME()
```
+ The name needs to be the same as the name in 2.4
**eg:**
![image10](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/0eae64d1-8e50-4a02-bf08-c9fc543130d0)

### 2.5 Add the algorithm list and set NON_AUTOML_MODELS

#### 2.5.1 Find file
Find the constants file to add the model name,The constants file is in the `data_mining` folder in the `geochemistrypi` folder.

![image11](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/84544ad9-44aa-4fb4-b0f1-668f4c3da65f)

(1) Add the model name
Add model name to the algorithm list corresponding to the model in the constants file.
**eg:** Add the name of the Lasso regression algorithm.
![image12](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/ec647037-2467-4a86-b7bb-e009a48cb964)

（2）set NON_AUTOML_MODELS
Because this is a tutorial without automatic parameters, you need to add the model name in the NON_AUTOML_MODELS.
**eg:**
![image13](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/d6b03566-a833-4868-8738-be09d7356c9c)





### 2.6 Add Functionality

#### 2.6.1 Model Research

Conduct research on the corresponding model and confirm the functions that need to be added.

\+ You can confirm the functions that need to be added on the official website of the model (such as scikit learn), search engines (such as Google), chatGPT, etc.

(1) Common_component is a public function in a class, and all functions in each class can be used, so they need to be added in the parent class，Each of the parent classes can call Common_component.

(2) Special_component is unique to the model, so they need to be added in a specific model，Only they can use it.

![Image1](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/3f983a7a-3b0d-4c7b-b7b7-31b317f4d9d0)



#### 2.6.2 Add Common_component

Common_component refer to functions that can be used by all internal submodels, so it is necessary to consider the situation of each submodel when adding them.

***\*1. Add corresponding functionality to the parent class\****

Once you've identified the features you want to add, you can define the corresponding functions in the parent class.

The code format is:

(1) Define the function name and add the required parameters.

(2) Use annotations to describe function functionsUse annotations to describe function functions.

(3) Referencing specific functions to implement functionality.

(4) Change the format of data acquisition and save data or images.



***\*2. Define Common_component\****

(1) Define the common_components in the parent class, its role is to set where the output is saved.

(2) Set the parameter source for the added function.



***\*3. Implement function functions\****

Some functions may use large code due to their complexity. To ensure the style and readability of the code, you need to put the specific function implementation into the corresponding `_common` files and call it.

It includes:

(1) Explain the significance of each parameter.

(2) Implement functionality.

(3) Returns the required parameters.



***\*eg:\**** You want to add model evaluation to your clustering.

First, you need to find the parent class to clustering.

![Image2](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/b41a5af8-6cf3-4747-8c83-e613a3fee04b)

![Image3](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/e81f3c96-f90d-49c8-b2e9-e8675d41cf90)

***\*1. Add the clustering score function in class ClusteringWorkflowBase (WorkflowBase).\****


```python

@staticmethod
def _score(data: pd.DataFrame, labels: pd.DataFrame, algorithm_name: str, store_path: str) -> None:

    """Calculate the score of the model."""

    print("-----* Model Score *-----")

    scores = score(data, labels)

    scores_str = json.dumps(scores, indent=4)

    save_text(scores_str, f"Model Score - {algorithm_name}", store_path)

    mlflow.log_metrics(scores)

```


(1) Define the function name and add the required parameters.

(2) Use annotations to describe function functionsUse annotations to describe function functions.

(3) Referencing specific functions to implement functionality (Reference 3.2.3).

(4) Change the format of data acquisition and save data or images.

***\*Note:\**** Make sure that the code style of the added function is consistent.

***\*2. Define common_components below the added function to define the output position and parameter source for the added function.\****

```python

def common_components(self) -> None:

    """Invoke all common application functions for clustering algorithms."""

    GEOPI_OUTPUT_METRICS_PATH = os.getenv("GEOPI_OUTPUT_METRICS_PATH")

    GEOPI_OUTPUT_ARTIFACTS_IMAGE_MODEL_OUTPUT_PATH = os.getenv("GEOPI_OUTPUT_ARTIFACTS_IMAGE_MODEL_OUTPUT_PATH")

    self._score(

      data=self.X,

      labels=self.clustering_result["clustering result"],

      algorithm_name=self.naming,

      store_path=GEOPI_OUTPUT_METRICS_PATH,

    )

```

The positional relationship is shown in Figure 4.

![Image4](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/5e3eac82-19f8-4ef3-87a6-701ce6f9ac1b)

***\*3. You need to add the specific function implementation to the corresponding `_commom` file.\****

![Image5](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/ee6bb43e-f30e-47b6-8d78-13f017994a44)

```python

def score(data: pd.DataFrame, labels: pd.DataFrame) -> Dict:

    """Calculate the scores of the clustering model.

      Parameters

      ----------

      data : pd.DataFrame (n_samples, n_components)

        The true values.

      labels : pd.DataFrame (n_samples, n_components)

        Labels of each point.

      Returns

      -------

      scores : dict

        The scores of the clustering model.

    """

    silhouette = silhouette_score(data, labels)

    calinski_harabaz = calinski_harabasz_score(data, labels)

    print("silhouette_score: ", silhouette)

    print("calinski_harabasz_score:", calinski_harabaz)

    scores = {

        "silhouette_score": silhouette,

        "calinski_harabasz_score": calinski_harabaz,

    }

    return scores

```

(1) Explain the significance of each parameter.

(2) Implement functionality.

(3) Returns the required parameters.



#### 2.6.3 Add Special_component

Special_components is a feature that is unique to each specific model.

The process of adding a Special_components is similar to that of a Common_component.



The process is as follows:

(1) Find the location that needs to be added.

(2) Defined function.

(3) Define Special_components and add a parametric function to it.

(4) Add the corresponding specific function implementation function to the `corresponding manual parameter tuning` file.



***\*eg:\**** An example is to add a score evaluation function to k-means clustering.

***\*1. Find the location that needs to be added.\****

We add his own unique score to the k-means.

![Image2](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/b41a5af8-6cf3-4747-8c83-e613a3fee04b)

![Image6](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/34f1b0f8-9809-4ba6-86d5-aa28a565abc9)

***\*2. Defined function.\****

```python

def _get_inertia_scores(self, algorithm_name: str, store_path: str) -> None:

    """Get the scores of the clustering result."""

    print("-----* KMeans Inertia Scores *-----")

    print("Inertia Score: ", self.model.inertia_)

    inertia_scores = {"Inertia Score": self.model.inertia_}

    mlflow.log_metrics(inertia_scores)

    inertia_scores_str = json.dumps(inertia_scores, indent=4)

    save_text(inertia_scores_str, f"KMeans Inertia Scores - {algorithm_name}", store_path)

```

(1) Define the function name and add the required parameters.

(2) Use annotations to describe function functionsUse annotations to describe function functions.

(3) Referencing specific functions to implement functionality.

(4) Change the format of data acquisition and save data or images.

***\*3. Define Special_components and add a parametric function to it.\****


```python

def special_components(self, **kwargs: Union[Dict, np.ndarray, int]) -> None:

	  """Invoke all special application functions for this algorithms by Scikit-learn framework."""

	   GEOPI_OUTPUT_METRICS_PATH = os.getenv("GEOPI_OUTPUT_METRICS_PATH")

	   self._get_inertia_scores(

	   algorithm_name=self.naming,

	   store_path=GEOPI_OUTPUT_METRICS_PATH,

	 )

```

The positional relationship is shown in Figure 7.

![Image7](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/18dec84b-44ae-4883-a5b8-db2c6e0ef5c8)

***\*4. Add the corresponding specific function implementation function to the `corresponding manual parameter tuning` file.\****

If the defined function has complex functions, it is necessary to further improve its function content in the manual parameter file, and the code format should refer to Common_component.

![Image](https://github.com/ZJUEarthData/geochemistrypi/assets/113361635/a3ea82c2-9c20-49f4-bf3e-354b012aff7c)

## 3. Test model
After the model is added, it can be tested. If the test reports an error, it needs to be checked. If there is no error, it can be submitted.

## 4. Completed Pull Request
After the model test is correct, you can complete the pull request according to the puu document instructions in [Geochemistry π](https://geochemistrypi.readthedocs.io/en/latest/index.html)
![image](https://github.com/ZJUEarthData/geochemistrypi/assets/97781484/e95c2e44-21f7-44af-8e32-e857189a5204)

## 5. Precautions
**Note1:** This tutorial only discusses the general process of adding a model, and the specific addition needs to be combined with the actual situation of the model to accurately add relevant codes.
**Note2:** If there are unclear situations and problems during the adding process, communicate with other people in time to solve them.
