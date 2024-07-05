# OLS_pipeline

A Python package to preprocess data, fit models, and calculate VIF.

## Installation

You can install the package using pip:


## Usage

```python
import OLS_pipeline.pipeline as OLS_pipe

data_path = "path/to/your/data.csv"

dependent_var = 'Green Bond Issuance'
independent_vars = ['COVID_Impact_Measure', 'GDP Growth', 'Financial Development', 'Conventional Bond Issuance']
normalize_cols = ['Stringency Index', 'Covid Cases', 'Covid Death']
weight_dict = {'Stringency Index': 0.3, 'Covid Cases': 0.3, 'Covid Death': 0.4}
interaction_pairs = [('COVID_Impact_Measure', 'Financial Development')]

results = OLS_pipe.pipeline(data_path, dependent_var, independent_vars, normalize_cols, weight_dict, interaction_pairs)
fixed_effects_results, random_effects_model, vif_data = results 
```