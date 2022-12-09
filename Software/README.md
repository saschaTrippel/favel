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
* ```-e EXPERIMENT, --experiment EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory
* ```-b EXPERIMENT, --batch EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory.
Experiment will be run in batch mode, meaning that an experiment will be executed with every subset of the specified set of fact validation approaches.
* ```-d DATA, --data DATA``` path to the dataset to validate
* ```-c, --containers``` automatically Start/Stop containers

