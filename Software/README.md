FAVEL
=
<i>Fact Validation Ensemble Learner</i>

# Usage
To evaluate one Machine Learning Algorithm with one set of fact validation approaches, create a directory in the Evaluation folder.\
This directory represents one experiment. \
Inside the direcotry, there has to be a configuration file ```favel.conf```, which specifies the ML-Algorithm and the set of fact validation approaches.

## How to run

```
python3 Favel.py [options]
```

### Options
* ```-e EXPIRIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory
* ```-d DATA, --data DATA``` path to the dataset to validate
* ```-c, --cache``` Check the cache for correctness

### Optional ContainerService
  ```-sc, --containers``` 
+ To be added next to [options]
+ To Start/Stop containers, if not already running on VM

# Architecture
![Favel component diagram](FavelArchitecture.png)
