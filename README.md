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
    - [**eval002**](Evaluation/eval002)
    - [**eval003**](Evaluation/eval003)
    - [**eval004**](Evaluation/eval004)
    - [**eval005**](Evaluation/eval005)
    - [**eval006**](Evaluation/eval006)
    - [**eval007**](Evaluation/eval007)
    - [**example**](Evaluation/example)
- [**FAVEL DATASET**](Favel_Dataset)
    - [**Files**](Favel_Dataset/Files)
        - [**Correct**](Favel_Dataset/Files/Correct)
        - [**Wrong**](Favel_Dataset/Files/Wrong)
    - [**Turtle**](Favel_Dataset/Turtle)
        - [**Test**](Favel_Dataset/Turtle/Test)
            - [**Correct**](Favel_Dataset/Turtle/Test/Correct)
                - [**Movie-Director**](Favel_Dataset/Turtle/Test/Correct/Movie-Director)
                - [**Movie-Producer**](Favel_Dataset/Turtle/Test/Correct/Movie-Producer)
                - [**Movie-ProductionCompany**](Favel_Dataset/Turtle/Test/Correct/Movie-ProductionCompany)
                - [**Movie-Starring**](Favel_Dataset/Turtle/Test/Correct/Movie-Starring)
                - [**Scientist-AcademicDiscipline**](Favel_Dataset/Turtle/Test/Correct/Scientist-AcademicDiscipline)
                - [**Scientist-Award**](Favel_Dataset/Turtle/Test/Correct/Scientist-Award)
                - [**Scientist-KnownFor**](Favel_Dataset/Turtle/Test/Correct/Scientist-KnownFor)
                - [**University-Affiliation**](Favel_Dataset/Turtle/Test/Correct/University-Affiliation)
                - [**University-City**](Favel_Dataset/Turtle/Test/Correct/University-City)
                - [**University-Type**](Favel_Dataset/Turtle/Test/Correct/University-Type)
            - [**Wrong**](Favel_Dataset/Turtle/Test/Wrong)
                - [**Movie-Director**](Favel_Dataset/Turtle/Test/Wrong/Movie-Director)
                - [**Movie-Producer**](Favel_Dataset/Turtle/Test/Wrong/Movie-Producer)
                - [**Movie-ProductionCompany**](Favel_Dataset/Turtle/Test/Wrong/Movie-ProductionCompany)
                - [**Movie-Starring**](Favel_Dataset/Turtle/Test/Wrong/Movie-Starring)
                - [**Scientist-AcademicDiscipline**](Favel_Dataset/Turtle/Test/Wrong/Scientist-AcademicDiscipline)
                - [**Scientist-Award**](Favel_Dataset/Turtle/Test/Wrong/Scientist-Award)
                - [**Scientist-KnownFor**](Favel_Dataset/Turtle/Test/Wrong/Scientist-KnownFor)
                - [**University-Affiliation**](Favel_Dataset/Turtle/Test/Wrong/University-Affiliation)
                - [**University-City**](Favel_Dataset/Turtle/Test/Wrong/University-City)
                - [**University-Type**](Favel_Dataset/Turtle/Test/Wrong/University-Type)
        - [**Train**](Favel_Dataset/Turtle/Train)
            - [**Correct**](Favel_Dataset/Turtle/Train/Correct)
                - [**Movie-Director**](Favel_Dataset/Turtle/Train/Correct/Movie-Director)
                - [**Movie-Producer**](Favel_Dataset/Turtle/Train/Correct/Movie-Producer)
                - [**Movie-productionCompany**](Favel_Dataset/Turtle/Train/Correct/Movie-productionCompany)
                - [**Movie-Starring**](Favel_Dataset/Turtle/Train/Correct/Movie-Starring)
                - [**Scientist-AcademicDiscipline**](Favel_Dataset/Turtle/Train/Correct/Scientist-AcademicDiscipline)
                - [**Scientist-Award**](Favel_Dataset/Turtle/Train/Correct/Scientist-Award)
                - [**Scientist-KnownFor**](Favel_Dataset/Turtle/Train/Correct/Scientist-KnownFor)
                - [**University-Affiliation**](Favel_Dataset/Turtle/Train/Correct/University-Affiliation)
                - [**University-City**](Favel_Dataset/Turtle/Train/Correct/University-City)
                - [**University-Type**](Favel_Dataset/Turtle/Train/Correct/University-Type)
            - [**Wrong**](Favel_Dataset/Turtle/Train/Wrong)
                - [**Movie-Director**](Favel_Dataset/Turtle/Train/Wrong/Movie-Director)
                - [**Movie-Producer**](Favel_Dataset/Turtle/Train/Wrong/Movie-Producer)
                - [**Movie-ProductionCompany**](Favel_Dataset/Turtle/Train/Wrong/Movie-ProductionCompany)
                - [**Movie-Starring**](Favel_Dataset/Turtle/Train/Wrong/Movie-Starring)
                - [**Scientist-AcademicDiscipline**](Favel_Dataset/Turtle/Train/Wrong/Scientist-AcademicDiscipline)
                - [**Scientist-Award**](Favel_Dataset/Turtle/Train/Wrong/Scientist-Award)
                - [**Scientist-KnownFor**](Favel_Dataset/Turtle/Train/Wrong/Scientist-KnownFor)
                - [**University-Affiliation**](Favel_Dataset/Turtle/Train/Wrong/University-Affiliation)
                - [**University-City**](Favel_Dataset/Turtle/Train/Wrong/University-City)
                - [**University-Type**](Favel_Dataset/Turtle/Train/Wrong/University-Type)
- [**FAVEL DATASET**](FinalDataset_Hard)
    - [**Files**](FinalDataset_Hard/Files)
        - [**Correct**](FinalDataset_Hard/Files/Correct)
        - [**Wrong**](FinalDataset_Hard/Files/Wrong)
    - [**Turtle**](FinalDataset_Hard/Turtle)
        - [**Test**](FinalDataset_Hard/Turtle/Test)
            - [**Correct**](FinalDataset_Hard/Turtle/Test/Correct)
                - [**movie-director**](FinalDataset_Hard/Turtle/Test/Correct/movie-director)
                - [**movie-producer**](FinalDataset_Hard/Turtle/Test/Correct/movie-producer)
                - [**movie-productionCompany**](FinalDataset_Hard/Turtle/Test/Correct/movie-productionCompany)
                - [**movie-starring**](FinalDataset_Hard/Turtle/Test/Correct/movie-starring)
                - [**scientist-academicDiscipline**](FinalDataset_Hard/Turtle/Test/Correct/scientist-academicDiscipline)
                - [**scientist-award**](FinalDataset_Hard/Turtle/Test/Correct/scientist-award)
                - [**scientist-birthplace**](FinalDataset_Hard/Turtle/Test/Correct/scientist-birthplace)
                - [**scientist-deathPlace**](FinalDataset_Hard/Turtle/Test/Correct/scientist-deathPlace)
                - [**university-affiliation**](FinalDataset_Hard/Turtle/Test/Correct/university-affiliation)
                - [**university-chancellor**](FinalDataset_Hard/Turtle/Test/Correct/university-chancellor)
                - [**university-city**](FinalDataset_Hard/Turtle/Test/Correct/university-city)
            - [**Wrong**](FinalDataset_Hard/Turtle/Test/Wrong)
                - [**movie-director**](FinalDataset_Hard/Turtle/Test/Wrong/movie-director)
                - [**movie-producer**](FinalDataset_Hard/Turtle/Test/Wrong/movie-producer)
                - [**movie-productionCompany**](FinalDataset_Hard/Turtle/Test/Wrong/movie-productionCompany)
                - [**movie-starring**](FinalDataset_Hard/Turtle/Test/Wrong/movie-starring)
                - [**scientist-academicDiscipline**](FinalDataset_Hard/Turtle/Test/Wrong/scientist-academicDiscipline)
                - [**scientist-award**](FinalDataset_Hard/Turtle/Test/Wrong/scientist-award)
                - [**scientist-birthPlace**](FinalDataset_Hard/Turtle/Test/Wrong/scientist-birthPlace)
                - [**scientist-deathPlace**](FinalDataset_Hard/Turtle/Test/Wrong/scientist-deathPlace)
                - [**university-affiliation**](FinalDataset_Hard/Turtle/Test/Wrong/university-affiliation)
                - [**university-chancellor**](FinalDataset_Hard/Turtle/Test/Wrong/university-chancellor)
                - [**university-city**](FinalDataset_Hard/Turtle/Test/Wrong/university-city)
        - [**Train**](FinalDataset_Hard/Turtle/Train)
            - [**Correct**](FinalDataset_Hard/Turtle/Train/Correct)
                - [**movie-director**](FinalDataset_Hard/Turtle/Train/Correct/movie-director)
                - [**movie-producer**](FinalDataset_Hard/Turtle/Train/Correct/movie-producer)
                - [**movie-productionCompany**](FinalDataset_Hard/Turtle/Train/Correct/movie-productionCompany)
                - [**movie-starring**](FinalDataset_Hard/Turtle/Train/Correct/movie-starring)
                - [**scientist-academicDiscipline**](FinalDataset_Hard/Turtle/Train/Correct/scientist-academicDiscipline)
                - [**scientist-award**](FinalDataset_Hard/Turtle/Train/Correct/scientist-award)
                - [**scientist-birthplace**](FinalDataset_Hard/Turtle/Train/Correct/scientist-birthplace)
                - [**scientist-deathPlace**](FinalDataset_Hard/Turtle/Train/Correct/scientist-deathPlace)
                - [**university-affiliation**](FinalDataset_Hard/Turtle/Train/Correct/university-affiliation)
                - [**university-chancellor**](FinalDataset_Hard/Turtle/Train/Correct/university-chancellor)
                - [**university-city**](FinalDataset_Hard/Turtle/Train/Correct/university-city)
            - [**Wrong**](FinalDataset_Hard/Turtle/Train/Wrong)
                - [**movie-director**](FinalDataset_Hard/Turtle/Train/Wrong/movie-director)
                - [**movie-producer**](FinalDataset_Hard/Turtle/Train/Wrong/movie-producer)
                - [**movie-productionCompany**](FinalDataset_Hard/Turtle/Train/Wrong/movie-productionCompany)
                - [**movie-starring**](FinalDataset_Hard/Turtle/Train/Wrong/movie-starring)
                - [**scientist-academicDiscipline**](FinalDataset_Hard/Turtle/Train/Wrong/scientist-academicDiscipline)
                - [**scientist-award**](FinalDataset_Hard/Turtle/Train/Wrong/scientist-award)
                - [**scientist-birthPlace**](FinalDataset_Hard/Turtle/Train/Wrong/scientist-birthPlace)
                - [**scientist-deathPlace**](FinalDataset_Hard/Turtle/Train/Wrong/scientist-deathPlace)
                - [**university-affiliation**](FinalDataset_Hard/Turtle/Train/Wrong/university-affiliation)
                - [**university-chancellor**](FinalDataset_Hard/Turtle/Train/Wrong/university-chancellor)
                - [**university-city**](FinalDataset_Hard/Turtle/Train/Wrong/university-city)
- [**Software**](Software)
    - [**ContainerService**](Software/ContainerService)
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
    - [**controller**](Software/controller)
    - [**datastructures**](Software/datastructures)
        - [**exceptions**](Software/datastructures/exceptions)
    - [**FactValidationService**](Software/FactValidationService)
        - [**Interface_documentation**](Software/FactValidationService/Interface_documentation)
    - [**InputService**](Software/InputService)
    - [**FAVEL ML Service**](Software/MLService)
        - [**models**](Software/MLService/models)
    - [**FAVEL Output Service**](Software/OutputService)
    - [**test**](Software/test)