# MyKMeansProject

This package provides Python bindings to run KMeans and GeoKMeans algorithms using a C++ backend.

## Installation

You can install this package using pip:

```bash
pip install mykmeansproject
```


Usage

```python
from mykmeansproject.kmeans import run_lloyd_kmeans, run_geokmeans

# Example usage
results = run_lloyd_kmeans(
    100,
    0.0001,
    12,
    17,
    [
        "./Breastcancer.csv",
        "./CreditRisk.csv",
        "./census.csv",
        "./birch.csv"
    ]
)

# Access results
for result in results:
    print(result.loop_counter)
    print(result.to_dict())

```