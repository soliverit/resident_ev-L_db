# Part L RdSAP estimator residential retrofit evaluator database interfaces

### Disclaimer
The dataset is dervied from publicly available data which is missing some desirable data, including the RdSAP version behind the existing results. It is intended as entry point for people interested in machine learning in building energy performance.

That said, for estate analysis the models are "significantly better than a guess".

### The dataset
The dataset contains 124 million estimated retrofit results for all (not corrupt) domestic EPCs in England and Wales. Data are divided into regions labelled similar to "domestic-E06000002-Middlesbrough". Each region dataset contains:

- certificates.csv&emsp;&emsp;# File containing data retrieve from https://opendatacommunities.org/home
- targets.csv&emsp;&emsp;&emsp;  # The environmental targets also present in the certificates table
- retrofits.csv&emsp;&emsp;&emsp;# The retrofit results and indiciative costs (excluding heating cost)
- train.csv&emsp;&emsp;&emsp;&emsp; # The data used to train the estimator

Estimates made using the https://github.com/soliverit/depc_emulator GradientBoostingRegressor model.

### Related works (Nondomestic)
```
Saleh Seyedzadeh, Farzad Pour Rahimian, Stephen Oliver, Sergio Rodriguez, Ivan Glesk,
Machine learning modelling for predicting non-domestic buildings energy performance: A model to support deep energy retrofit decision-making,
Applied Energy,
Volume 279,
2020,
115908,
ISSN 0306-2619,
https://doi.org/10.1016/j.apenergy.2020.115908.
```
### Summary
This repository contains basic interfaces for the Resident_Ev-L dataset. Currently:

- Ruby
- Python

### Getting Started

- Download the dataset from https://drive.google.com/file/d/1CjMk9K3JEb3xhWsrG4Iwi8VtHJV9GOmV/view?usp=sharing
Unzip the data into a somewhere convenient. The root of that directory is where we'll put the interfaces.

- Download the repository or file
`
git clone https://github.com/soliverit/resident_ev-L_db.git
`

*Python*
```python
from re_data_set import REDataset
##
# Open a dataset using the path to a region's dataset
##
reDataSet = REDataset("./epc_data/domestic-E06000002-Middlesbrough/")
reDataSet.load()
## Remove records with important data missing
reDataSet.filterErrors()
##
# Accessors
##
# Get Record
record    = reDataSet[0]
# Get Record value
value     = record["roof-Eff"]
##
# Iterator
##
for record in reDataSet.records:
  pass
```
*Ruby*
```ruby
require "./re_data_set.rb"
##
# Open a dataset using the path to a region's dataset
##
reDataSet = REDataset.new("./epc_data/domestic-E06000002-Middlesbrough")
reDataSet.load
## Remove records with important data missing
reDataSet.filterErrors
##
# Accessors
##
# Get Record
record    = reDataSet[0]
# Get Record value (Property keys are :symbols not "strings")
value     = record[:"roof-Eff"]
##
# Iterator
##
reDataSet.each{|data| "..."}
```
