# Incremental Feature Analysis Tool - Mathematical definition

The IFA tool is used to find if a feature has incremental predictive power over an existing model. While literature discusses looking at forecast error (i.e. $y_i - s_i$) the nature of classification models makes it difficult to determine if a contesting feature who we believe should be part of the separation hyperplance will have incremental value.

The IFA Tool does not assume any relationship between the contesting feature and the performance. Rather, we segment the feature using an arbitrary segmentor and observe the model error in local "neighborhoods" defined by the segmentor and use visual judgement to determine what pre-processing, if any, the feature will require.

## 1. Usage

### 1.1 Installation

```
pip install ak-ifa
```
requirements are listed in the `requirements.txt` file

### 1.2 General usage

Given a dataframe with at least:
- 1 column of labels {0,1} or any values in the range (0,1), called 'y' in the example
- 1 column of predictions as probabilities in the range (0,1), called 'p' in the example
- 1 column of a candidate continuous feature, called 'x' in the example

```python
from ifa.api import *

result, _ = analyze_feature(df, x_col='x', p_col='p', y_col='y', plot=True)
```

Will plot a graphical test for the added information of the feature 'x' over the prediction 'p'.

### 1.3 Demo of feature with added information

To ease learning, we have provided a demo module with some helper functions

```python
import numpy as np
import pandas as pd

from ifa.api import *
from ifa.demo import model_samples, fit_logistic_regression
from ifa.math import sigmoid

# assume linear coefficients of a logistic regression model
beta = np.array([1, -1, 2, -2])

# create model samples based of coefficients (see math below)
X, y, _ = model_samples(10000, beta, seed=42)

# fit a model on part of the features
X_partial = X[:,:3]
beta_hat_partial = fit_logistic_regression(X_partial, y)
print(beta_hat_partial) # [ 0.78434972 -0.79164423  1.61375143], values might depend on RandomState's impl.

y_hat_partial = sigmoid(X_partial.dot(beta_hat_partial))

df_partial = pd.DataFrame({
    'x':X[:,3], # the 'missing' feature
    'y': y,
    'y_hat': y_hat_partial
    })

result, _ = analyze_feature(df_partial, x_col='x', p_col='y_hat', y_col='y', plot=True)
```

![alt text](/readme_images/example%20with%20information.png)


### 1.4 Demo of feature without added information

```python
import numpy as np
import pandas as pd

from ifa.api import *
from ifa.demo import model_samples, fit_logistic_regression
from ifa.math import sigmoid

# assume linear coefficients of a logistic regression model
beta = np.array([1, -1, 2, -2])

# create model samples based of coefficients (see math below)
n = 10000
X, y, _ = model_samples(n, beta, seed=42)

# fit a model on all features
beta_hat = fit_logistic_regression(X, y)

y_hat = sigmoid(X.dot(beta_hat))

df = pd.DataFrame({
    'x':np.random.uniform(-1,1,n), # the 'missing' feature, this time with no information
    'y': y,
    'y_hat': y_hat
    })

result, _ = analyze_feature(df, x_col='x', p_col='y_hat', y_col='y', plot=True)
```

![alt text](/readme_images/example%20without%20information.png)



## 2. Scope of this doc

When using the CT to find sloping features for a production model we should follow these steps:
1. Use the tool to determine if the feature can improve the model.
2. Decide, based on quantitative thresholds and qualitative considerations if the feature should be added to the model.
3. Pre-process the feature. repeat steps 1, 2 if necessary.
4. Add the processed feature to the model.

In this doc, we will cover steps 1, 4. we will also cover some mathematical properties of CT through simulation.

## 3. Definition

### 3.1 CT Constraints

- CT's Feature analysis can be used with any probability generating model. 
- CT can operate with any real or categorical feature.
- The suggested correction can also be used for any probability generating model, but would fit very nicely and linearly with Logistic Models.

### 3.2 Notation

Let:

$s\in(0,1)$ denote a score from a classification model<br>
$y\in\{0,1\}$ denote a label<br>
$w>0$ denote a weight<br>
$x\in\mathbb{R}$ denote a contesting real feature <br>

#### The segmentor

Let $g: \mathbb{R}\rightarrow G$ denote some segmentor that maps $\mathbb{R}$ to a set $G=\{g_\text{NULL}, g_1, g_2 ,..., g_{|G|}\}$. Where each $g_i$ is some interval $[x_a, x_b]$ with $x_a<x_b$.<br>
The set $G$ will include $g_\text{NULL}$ which is the set of all indices where $x$ is Null.<br>

For each $i < j$ the associated groups $g_i,\ g_j$ should be defined over intervals $[x_{a,i}, x_{b,i}]$ and $[x_{a,j}, x_{b,j}]$ where $x_{a,i} < x_{a,j} \leq x_{b,i}$. In words, the intervals can be mutually exclusive or overlapping but their mid-points should be increasing with the index. A simple example for g could be `numpy.qcut`<br>


Over a dataset that is defined by the below tuple:<br>

$$\mathcal{D}=\{(x_k, s_k, w_k, y_k, g(x_k))\}_{k=1}^n$$

Define $m_i$ the local weighted mean of all $x_k$ in $g_i$:<br>

$$m_i:=\frac{\sum_{k\in g_i}x_k w_k}{\sum_{k\in g_i}w_k}$$

### 3.3 Feature analysis definition

The rationale behind the feature analysis assumes:
- Extra features should tested 'above' or 'given' the model.
- Although we use logistic regression which is GLM, we don't assume any behavior of the feature
- Rather, we check if there's a constant that we can add to the model in different neighborhoods of $x$ that will minmize it's Cross Entropy within that neighborhood.


Let $\sigma^{-1}(.)$ denote the logit function: $\sigma^{-1}(p) = \log \frac{p}{1-p}$

Let $\sigma(.)$ denote the sigmoid function: $\sigma(x) = \frac{e^x}{1+e^x} = \frac{1}{1+e^{-x}} = 1-\sigma(-x)$

The Cross Entropy in neighborhood $g_i$ is : 

$$-\sum_{\{k\in g_i\}} 
        w_k \left[ 
            y_k \log(s_k) + (1-y_k) \log(1-s_k)
        \right]$$
        
For each neighborhood we check if there exists a bias $a$ that can reduce the cross entropy within that neighborhood. Define $L_i(a)$ as the cross entropy in the neighborhood of $g_i$, as a function of some bias $a$ we wish to add to the model score, all additions are done in the logit scale:

$$L_i(a) = 
    -\sum_{\{k\in g_i\}} 
        w_k \left[ 
            y_k \log\left(\sigma(a+\sigma^{-1}(s_k))\right) + 
            (1-y_k) \log\left(1-\sigma(a+\sigma^{-1}(s_k))\right)
        \right]$$

In words: $a$ is the required additive adjustment, in log-odds scale, so that the model would fit the data in the neighborhood of $g_i$.

It's easy to see that $L_i(0)$ is just the model's cross-entropy in $g_i$: 

$$L_i(0) = -\sum_{\{k\in g_i\}} w_k \left[ y_k \log(s_k) + (1-y_k) \log(1-s_k)\right]$$

Define $\delta_i:= \underset{a}{\text{argmin}}\ L_i(a)$

Plot the pairs: $(m_i, \delta_i)$ and observe the visual relationship.

### 3.4 A linear feature example

The procedure is as follows:

1. Draw some intercept $$\beta_0\in\mathbb{R}$$
2. Draw a weight vector $$\mathbf{\beta} \in [-1,1]^p$$
3. Assign $$\text{results} = []$$ (an empty list)<br>
4. For k in 1,2,3,...,N repeat:
- draw $\mathbf{x}_k$ from $[-1,1]^p$
- assign $\mu_k \leftarrow \beta_0 + \mathbf{x}_k^T\mathbf{\beta}$
- assign $\pi_k \leftarrow \frac{e^{\mu_k}}{1+e^{\mu_k}}$
- draw $y_k$ from $\text{Ber}(\pi_k)$ (either 0 or 1)
- assign $\text{results}[k] \leftarrow (y_k, p_k, \mu_k, \mathbf{x}_k)$

Learn a partial model $m'$ by omitting 1 feature $x_j$ from $\mathbf{x}$. Let $s'$ denote the score of $m'$
Run the contribution tool over the data set $\{(s'_k, x_{j,k}, y_k)\}_{k=1}^N$


## 4. Adding a feature to the model

Once we agree with the definition of the feature (we might want to perfrom some pre-processing) we would like to update the model's separation hyperplane with an additional coordinate. To do so we keep the separation hyperplane constant and only allow a new slope and bias to be learned.

#### Separation hyperplane adjustment procedure

Let:

$s\in(0,1)$ denote a score from a classification model<br>
$y\in\{0,1\}$ denote a label<br>
$w>0$ denote a weight<br>
$x\in\mathbb{R}$ denote a contesting real feature <br>

Given a dataset that is selected for the procedure: $\mathcal{D}=\{(y_i, s_i, x_i, w_i)\}_{i=1}^n$

Define: 

$$L(\beta_0, \beta_1; \mathcal{D}):= 
    -\sum_{i=1}^n w_i \left[
        y_i \log\left(\sigma(\beta_0 + \beta_1 x_i +\sigma^{-1}(s_i) )\right) + 
        (1-y_i) \log\left(1-\sigma(\beta_0 + \beta_1 x_i +\sigma^{-1}(s_i))\right)
        \right]$$
        
Learn $\beta_0, \beta_1$ by miniming $L(\beta_0, \beta_1; \mathcal{D})$ over them. This can be achieved very efficiently with L-BFGS or other first order minimizers (or higher).