# PyMTDEvaluator 2.0

PyMTDEvaluator is a tool for time-based Moving Target Defense (MTD) evaluation. The 2.0 version updates the previous one by providing support for Multi-Criteria Decision Making methods and also a improved graphical user interface. The manual below will guide you after [PyMTDEvaluator installation.](https://github.com/matheustor4/PyMTDEvaluator2/blob/main/README.md#installation) 

## Interface selection

PyMTDEvaluator features three interface options. The users can select their preferred ones at tool startup. 

They are Classical, Modern, and Upload XML file.

![image](https://github.com/user-attachments/assets/70c734ff-4099-4820-9fea-7411e9ce488e)

### Classical interface

The classical interface resembles the previous version of PyMTDEvaluator. It is devoted to the users of the previous versions that intend to continue to use the tool in a familiar interface. 

![image](https://github.com/user-attachments/assets/65f9fd44-7e2c-4d4e-a6f8-a99d20226dac)

### Modern interface

The modern interface features the option of save/load the parameters in a XML file. Besides that, the interface also presents tooltips for each of the fields. Compared to the previous interface, it has improved aesthetics and user experience (i.e., experiment parameters only appear if the experiment function is selected).  

![image](https://github.com/user-attachments/assets/0656184e-3f98-48d0-b0a4-d63e5ff0701b)

### Upload XML interface

Consists of a simple system dialog to feed the tool directly (i.e., without need to interact with the classical or modern interface) with a previously saved XML file. It is particularly useful in the combination of previous scenarios. 

![image](https://github.com/user-attachments/assets/4a76df22-a8cb-4cea-86bc-a9791270b29f)

## Parameters definition

We present the information for each field of PyMTDEvaluator below.

`Downtime per movement (min)` - Minutes of system downtime due to each MTD movement.

`Cost per movement ($)` - Monetary cost related to each MTD movement.

`Movement Trigger (h)` - Time (in hours) between MTD movements.

`Time for attack success (h)` - Expected time (in hours) for the attack to reach success in a system without MTD.

`Evaluation time (h)` - Target time (in hours) for the simulation environment. For example, evaluation time of 24 hours will produce simulation results for the first day of the system under attack.


### Experiment

PyMTDEvaluator also features the *Experiment* option. The *Experiment* consists of conducting a series of evaluations varying the desired parameters. 

*Experiment - Movement Trigger* feature performs evaluations varying `Movement Trigger` parameter. It is helpful to compare different scheduling of MTD actions. The user selects the minimum value (`Movement Trigger (h) - MIN`), the maximum value (`Movement Trigger (h) - MAX`), and the step/increment (`Movement Trigger (h) - Step`). 

The same idea applies in the context of *Experiment - Time for attack success*. It will produce results from a series of evaluations varying `Time for attack success` parameter. It is useful to compare the behavior of the MTD considering different attack rates. For example, supposing heavy or light DoS, or even attacker with different techinical abilities.

The user can run both experiments in the same PyMTDEvaluator run. In this scenario, the tool will produce results for every combination of the selected experiment parameters. 

### Multi-Criteria Decision Making

The Multi-Criteria Decision Making (MCDM) feature performs the comparison of the scenarios computed in a *Experiment* evaluation. It is possible to combine different scenarios in PyMTDEvaluator (i.e., merging results of multiple runs of the tool). However, **the MDCM only considers the current scenario, not the previous ones**. The "historical" MCDM is a intended feature for the upcoming version of the tool.

In PyMTDEvaluator, the weights are measured in percentage. This way, the sum of the weights should be equal do 100. The weights represent the importance assigned to each metric. T

## Understanding PyMTDEvaluator output

An extensive explanation of PyMTDEvaluator can be found in Section 6 of the following document: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4777777 

### Progress bar
![image](https://github.com/user-attachments/assets/57944b10-9317-4d20-9b66-4e2965e888c7)

## Illustrative case example

PyMTDEvaluator Docker container has multiple example XML files for the user to test the tool. 

They are mainly based on the paramters presented in Table 1 of the document: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4777777.

| Parameter                       | Description                                                                  | Value                                                                      |
| ------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| ``Movement Trigger``        | Time interval for MTD action                                                 | From 0.5 hours to 25.5 hours with a 5-hour step (using experiment feature) |
| ``Time for attack success`` | Expected time for the attacker to reach success if the system is without MTD | 24 hours                                                                   |
| ``Downtime per movement``   | System downtime associated to each MTD action                                | 4 seconds                                                                  |
| ``Cost per movement``       | Monetary cost per MTD action                                                 | 0.3 $                                                                      |
| ``Evaluation time``         | Time target for the simulation run                                           | 48 hours                                                                   |

The main parameters are as follows

## Further information and bug reporting

Feel free to contact matheustor4 \dot\ professor \at\ gmail \dot\ com for more information and bug reporting. 




