<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<p align="center"><img src="https://github.com/ActurialCapital/synthetica/blob/main/docs/static/logo.png" alt="logo" width="90%" height="90%"></p>

| Overview | |
|---|---|
| **Open Source** |  [![BSD 3-clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://github.com/ActurialCapital/synthetica/blob/main/LICENSE) |
| **Code** |  [![!pypi](https://img.shields.io/pypi/v/python-synthetica?color=orange)](https://pypi.org/project/python-synthetica/) [![!python-versions](https://img.shields.io/pypi/pyversions/python-synthetica)](https://www.python.org/) |
| **CI/CD** | [![!codecov](https://img.shields.io/codecov/c/github/ActurialCapital/synthetica?label=codecov&logo=codecov)](https://codecov.io/gh/ActurialCapital/synthetica) |
| **Downloads** | ![PyPI - Downloads](https://img.shields.io/pypi/dw/python-synthetica) ![PyPI - Downloads](https://img.shields.io/pypi/dm/python-synthetica) [![Downloads](https://static.pepy.tech/personalized-badge/python-synthetica?period=total&units=international_system&left_color=grey&right_color=blue&left_text=cumulative%20(pypi))](https://pepy.tech/project/python-synthetica) |


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
        <ul>
            <li><a href="#introduction">Introduction</a></li>
        </ul>
        <ul>
            <li><a href="#built-with">Built With</a></li>
        </ul>
    </li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

### Introduction

`Synthetica` is a versatile and robust tool for generating synthetic time series data. Whether you are engaged in financial modeling, IoT data simulation, or any project requiring realistic time series data to create correlated or uncorrelated signals, `Synthetica` provides high-quality, customizable generated datasets. Leveraging advanced statistical techniques and machine learning algorithms, `Synthetica` produces synthetic data that closely replicates the characteristics and patterns of real-world data.

The project latest version incorporates a wide array of models, offering an extensive toolkit for generating synthetic time series data. This version includes features like:

* `GeometricBrownianMotion`
* `AutoRegressive`
* `NARMA`
* `Heston`
* `CIR`
* `LevyStable`
* `MeanReverting`
* `Merton`
* `Poisson`
* `Seasonal`

However, the `SyntheticaAdvenced` version elevates the capabilities further, integrating more sophisticated deep learning data-driven algorithms, such as `TimeGAN`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* `numpy = "^1.26.4"`
* `pandas = "^2.2.2"`
* `scipy = "^1.13.1"`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Installation

```sh
$ pip install python-synthetica
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Getting Started

Once you have cloned the repository, you can start using `Synthetica` to generate synthetic time series data. Here are some initial steps to help you kickstart your exploration:

```python
>>> import synthetica as sth
```

In this example, we are using the following parameters for illustration purposes:

* `length=252`: The length of the time series
* `num_paths=5`: The number of paths to generate
* `seed=123`: Reseed the `numpy` singleton `RandomState` instance for reproduction

**Initialize the model**: Using the `GeometricBrownianMotion` (GBM) model: This approach initializes the model with a specified path length, number of paths, and a fixed random seed:

```python
>>> model = sth.GeometricBrownianMotion(length=252, num_paths=5, seed=123)
```

**Generate random signals**: The transform method then generates the random signals accordingly:

```python
>>> model.transform() # Generate random signals
```

<p align="center"><img src="https://github.com/ActurialCapital/synthetica/blob/main/docs/static/gbm_random_transform.png" alt="chart-1" width="75%" height="75%"></p>

**Generate correlated paths**: This process ensures that the resulting features are highly positively correlated, leveraging the Cholesky decomposition method to achieve the desired `matrix` correlation structure:

```python
>>> model.transform(matrix) # Produces highly positively correlated features
```

<p align="center"><img src="https://github.com/ActurialCapital/synthetica/blob/main/docs/static/gbm_corr_transform.png" alt="chart-2"  width="75%" height="75%"></p>


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Notes

### Cholesky Decomposition

The Cholesky transformation (or Cholesky decomposition) is a mathematical technique used to decompose a positive definite matrix into the product of a lower triangular matrix and its transpose. This is particularly useful in various fields such as numerical analysis, optimization, and financial modeling.

#### Mathematical Definition

Given a positive definite matrix $\(A\)$, the Cholesky decomposition is a factorization such that:
$\[ A = L L^T \]$
where:
- $\(A\)$ is a positive definite matrix.
- $\(L\)$ is a lower triangular matrix.
- $\(L^T\)$ is the transpose of $\(L\)$.

### Applications

1. **Numerical Stability**: The Cholesky decomposition is more numerically stable than other decomposition methods for positive definite matrices.
2. **Solving Linear Systems**: It is used to solve linear systems of equations efficiently.
3. **Simulating Correlated Random Variables**: In finance and statistics, it is used to generate correlated random variables from uncorrelated ones.

### Implementation

In the context of synthetic data generation, the Cholesky transformation can be used to apply a correlation structure to a set of uncorrelated random variables.

### Example Implementation in Python

Here's a simple example of how to implement and use the Cholesky transformation in Python:

```python
import numpy as np

# Generate a positive definite matrix (covariance matrix)
def generate_positive_definite_matrix(size):
    A = np.random.rand(size, size)
    return np.dot(A, A.T) + size * np.eye(size)

# Apply Cholesky decomposition
def cholesky_transform(data, cov_matrix):
    # Perform Cholesky decomposition
    L = np.linalg.cholesky(cov_matrix)
    # Transform the data
    transformed_data = np.dot(data, L.T)
    return transformed_data

# Example usage
np.random.seed(42)
size = 5  # Size of the covariance matrix
cov_matrix = generate_positive_definite_matrix(size)

# Generate synthetic data (uncorrelated random variables)
data = np.random.randn(100, size)

# Apply Cholesky transformation to impose the correlation structure
transformed_data = cholesky_transform(data, cov_matrix)

print("Original Data:\n", data[:5])
print("Transformed Data:\n", transformed_data[:5])
```

### Explanation

1. **generate_positive_definite_matrix**:
   - Generates a random positive definite matrix. This can be a covariance matrix in practical scenarios.

2. **cholesky_transform**:
   - Performs Cholesky decomposition on the covariance matrix to obtain the lower triangular matrix \(L\).
   - Transforms the original uncorrelated data by multiplying it with \(L^T\) to introduce the desired correlation structure.

3. **Example Usage**:
   - Generates synthetic uncorrelated data.
   - Applies the Cholesky transformation to this data using the generated covariance matrix.
   - The transformed data now exhibits the correlation structure defined by the covariance matrix.

### In the Context of the `LevyStable` Class

The `cholesky_transform` method in the `LevyStable` class would be used to apply a correlation structure to the generated synthetic data. This would allow for the generation of more realistic synthetic data that incorporates correlations between different paths or time series.

Here is how you could integrate and test the `cholesky_transform` method in the `LevyStable` class:

### Positive Definiteness

#### What positive definite means in a covariance matrix

A covariance matrix is considered positive definite if it satisfies the following key properties:

1. It is symmetric, meaning the matrix is equal to its transpose.
2. For any non-zero vector $x$, $x^T * C * x > 0$, where $C$ is the covariance matrix and $x^T$ is the transpose of $x$.
3. All of its eigenvalues are strictly positive.

Positive definiteness in a covariance matrix has important implications:

1. It ensures the matrix is invertible, which is crucial for many [statistical techniques](https://stats.stackexchange.com/questions/52976/is-a-sample-covariance-matrix-always-symmetric-and-positive-definite).
2. It guarantees that the matrix represents a [valid probability distribution](https://statproofbook.github.io/P/covmat-psd.html).
3. It allows for unique solutions in [optimization problems](https://gowrishankar.info/blog/why-covariance-matrix-should-be-positive-semi-definite-tests-using-breast-cancer-dataset/) and ensures the stability of certain algorithms.
4. It indicates that no linear combination of the variables has zero variance, meaning all variables contribute [meaningful information](https://math.stackexchange.com/questions/114072/what-is-the-proof-that-covariance-matrices-are-always-semi-definite).

A covariance matrix that is positive semi-definite (allowing for eigenvalues to be non-negative rather than strictly positive) is still valid, but may indicate linear dependencies among variables.

In practice, sample covariance matrices are often positive definite if the number of observations exceeds the number of variables and there are no perfect linear relationships among the variables.

#### Implementation

`synthetica` automatically finds the nearest positive-definite matrix to input using `nearest_positive_definite` python function. it is directly sourced from [Computing a nearest symmetric positive semidefinite matrix](https://doi.org/10.1016/0024-3795(88)90223-6).

#### Other Sources

* [MatLab](https://www.mathworks.com/matlabcentral/fileexchange/42885-nearestspd)
* [StackOverflow](https://stackoverflow.com/questions/43238173/python-convert-matrix-to-positive-semi-definite)
* [Gist](https://gist.github.com/fasiha/fdb5cec2054e6f1c6ae35476045a0bbd)

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the BSD-3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

