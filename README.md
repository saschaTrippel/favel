FAVEL
=
<i>Fact Validation Ensemble Learner</i>

The vision of this project is to explore the possibility to train a supervised machine learning algorithm based on the results of several fact validation approaches.

To achieve this vision this project offers:
* A software which can automatically
    1. Validate a dataset on multiple fact validation approaches
    2. Use the results of the fact validation approaches to train a supervised machine learning algorithm
    3. Validate the dataset on the trained machine learning model
* Two datasets that can be used for evaluation

# Structure of the Repository
* Software: Software for exploring the vision
* Evaluation: The software will save results to this directory
* Analysis: Rudamentory script to plot diagrams based on the results in Evaluation
* Favel_Dataset: First dataset
* FinalDataset_Hard: Second dataset

# Installation
```
git clone https://github.com/saschaTrippel/favel
cd favel/Software
```

# Usage
* To conduct an experiment with the software execute the following steps:
    1. Create a direcotry inside the Evaluation directory.\
        The name of the directory is the name of the experiment \
        Example: ```favel/Evaluation/experiment42```
    2. Create a configuration file ```favel.conf``` inside the experiment directory. \
        The configuration file defines the set of fact validation approaches and the machine learning algorithm. \
        A basic configuration file is ```favel/Evaluation/example/favel.conf``` \
        For more advaced configuration options look at ```favel/Software/MLService/README.md``` \
        Example: ```favel/Evaluation/experiment42/favel.conf```
    3. Execute the software. \
        For the software to be able to use fact validation approaches, these approaches might have to be started manually. \
        An exaustive description how to run the software can be found in the following section. \
        Results will be saved to the ```favel/Evaluation/``` directory. \
        Example: ```python3 favel/Software/Favel.py -d favel/FinalDataset_Hard -e experiment42```

## How to run

```
python3 Favel.py [options]
```

## How to run test

```
python3 -m unittest
```

### Options
* ```-e EXPERIMENT, --experiment EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory
* ```-b EXPERIMENT, --batch EXPERIMENT``` name of the experiment, corresponds with the name of the experiment folder in the ```Evaluation``` directory.
Experiment will be run in batch mode, meaning that an experiment will be executed with every subset of the specified set of fact validation approaches.
* ```-d DATA, --data DATA``` path to the dataset to validate
* ```-w, --write``` write everything to disk. If this flag is set, all possible outputs are written to disk. This includes models, normalizers, predicate encoders, and dataframes.
If the flag is not set, only the overview is written to disk.
* ```-c, --containers``` automatically Start/Stop containers which encapsulate the fact validation approaches

# Additional Resources

## Datasets
* [FactBench](https://github.com/saschaTrippel/FactBench-Dataset_2022)
* [BPDP](https://github.com/saschaTrippel/BPDP-Dataset_2022)
* [Favel](https://github.com/saschaTrippel/favel/tree/main/Favel_Dataset)
* [Favel-hard](https://github.com/saschaTrippel/favel/tree/main/FinalDataset_Hard)

## Fact Validation Approaches
* <https://github.com/saschaTrippel/knowledgestream> offers multiple algorithms
* <https://github.com/palaniappan1/COPAAL> offers COPAAL

## File structure


- [**Analysis**](Analysis)
- [**Evaluation**](Evaluation)
    - [**eval001**](Evaluation/eval001)
    - ...
- [**FAVEL DATASET**](Favel_Dataset): Our dataset with simple example.  You can find The [**Documentation**](Favel_Dataset/README.md) in the folder.
  
- [**FAVEL DATASET HARD**](FinalDataset_Hard) : Our dataset with harder example.  You can find The [**Documentation**](Favel_Dataset/README.md) in the folder.
  
- [**Software**](Software): The software for favel
    - [**ContainerService**](Software/ContainerService) : This folder contains all the fact validations approaches used in this software with Dockerfile to lauch them. As well as the ContainerService responsible of launching and stopping containers programmatically.
        - [**adamic_adar**](Software/ContainerService/adamic_adar)
        - [**copaal**](Software/ContainerService/copaal)
        - [**degree_product**](Software/ContainerService/degree_product)
        - [**gfc**](Software/ContainerService/gfc)
        - [**jaccard**](Software/ContainerService/jaccard)
        - [**katz**](Software/ContainerService/katz)
        - [**klinker**](Software/ContainerService/klinker)
        - [**knowledgestream**](Software/ContainerService/knowledgestream)
        - [**pathent**](Software/ContainerService/pathent)
        - [**pra**](Software/ContainerService/pra)
        - [**predpath**](Software/ContainerService/predpath)
        - [**relklinker**](Software/ContainerService/relklinker)
        - [**simrank**](Software/ContainerService/simrank)
    - [**controller**](Software/controller): The controller of the application. Calling other module or organizing the work from input to output.
    - [**datastructures**](Software/datastructures): The data structure defining classes like Assertion as a python object and Definition of custom class exceptions
        - [**exceptions**](Software/datastructures/exceptions): Custom module exceptions
    - [**FactValidationService**](Software/FactValidationService): Module containing fact validation services responsible of validating the insertions he gets as input. It sends fact to the containers, gets the response, and caches if necessary.
        - [**Interface_documentation**](Software/FactValidationService/Interface_documentation)
    - [**InputService**](Software/InputService): The input service, reads the input dataset and transform it into a format that the software can easily use.
    - [**FAVEL ML Service**](Software/MLService): The Machine learning service. Responsible of receiving a dataset of fact validation with scores from different approaches, train a given machine learning model and test a given assertion to predict it's veracity using the trained model
        - [**models**](Software/MLService/models)
    - [**FAVEL Output Service**](Software/OutputService): Write the result in an evaluation format like Gerbil or in the evaluation folder.
    - [**test**](Software/test): All the test written for the software
