# decibel_thresholding
The decibel thresholding code is designed to run on a small single board computer with an external microphone. The training script is run to determine the normal operating decibel range for the location of the sensor package.

![training_decibel](https://user-images.githubusercontent.com/45575958/232609716-35319ed8-c020-4e6b-9d89-e9c43a580208.png)

After the normal range has been determined by the training script, we run the testing script. The testing script will detect anomalies if the decibel range falls outside fo the normal decibel range for a minimum of 3 seconds. When a sound anomaly is detected, the anomaly is recorded and saved to a file so that operators can listen to the anomalies.

![anomalies](https://user-images.githubusercontent.com/45575958/232609781-81acbf63-ac5e-43bb-bf2c-8b34503b6af8.png)
