# FactValidationService
The service is used to validate a list of facts on multiple fact validation algorithms.
The algorithms are executed in different processes, which are connected through a TCP interface.

## Interface
The interface differs for supervised and unsupervised approaches.

![Unsupervised communication](Interface_documentation/Unsupervised_Sequence-Diagram.png)

![Supervised communication](Interface_documentation/Supervised_Sequence-Diagram.png)

## Fact Validation Algorithms
Implementations that support this interface are:

* <https://github.com/saschaTrippel/knowledgestream> offers multiple algorithms
* <https://github.com/palaniappan1/COPAAL> offers COPAAL
