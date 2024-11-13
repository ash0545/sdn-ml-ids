# IDS Controller

> [!WARNING]
> This is a legacy controller and only works partially.

This section provides details for the IDS controller, as well as usage instruction.

## Table of Contents

- [IDS Controller](#ids-controller)
  - [Table of Contents](#table-of-contents)
  - [Controller Description](#controller-description)
  - [Model Used](#model-used)
  - [Usage Instructions](#usage-instructions)

## Controller Description

This controller uses the same collection process as the [Collector Controller](../).

However, instead of the flows being collected being written to CSV files, this controller passes on the data to the `MachineLearningAlgo` object's (initialized within the `__init__` method of the controller) `classify` method.

The `MachineLearningAlgo` class loads the Random Forest(RF), Principal Component Analysis(PCA) and RobustScaler(RS) objects. It then performs the required preprocessing before logging the prediction. This is done every 10 seconds.

## Model Used

The controller uses a RF model for classification of flows. This was trained on the MCAD dataset, and may not account for the specifics of your usecase and topology.

Input to the model is first transformed using the same division transformation described in previous sections. The following 13 features is then scaled using RS, after which it is reduced to 5 features using PCA. This is finally passed into the model, which performs multi-class classification - outputting one of the following: ddos, r2l, u2r, probe, web, normal.

## Usage Instructions

1. Run the Ryu controller Python file in conjunction with the `ofctl_rest` application through ryu-manager: `ryu-manager <file.py> ryu.app.ofctl_rest`
2. Setup your topology, ensuring it is properly configured to use your controller.
3. Once flows start being generated in the topology, the controller will begin logging the predictions.

> [!CAUTION]
> The controller by default gives a prediction every 10 seconds. If no flows as generated within 10 seconds after the controller has been started, an error will occur. The controller will then have to be restarted for predictions to start working again.
>
> This can be avoided by generating packets immediately after the controller is started, using something akin to the `pingall` command from mininet.
