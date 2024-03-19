# bracelet
  Using XGBoost algorithm to detect the rapid Increase in heart rate indicating a panic attack and also detecting the decreasing slope of the heart ﻿rate and oxygen in the blood. We covered two possible scenarios in drowning - struggling and obscured and fainting undetected. We covered two possible scenarios in drowning - struggling and obscured and fainting undetected. We used pulse oximeter sensor MAX30102 to measure Vital signs, and we used Raspberry pi pico microcontroller to run the algorithm of the detection and open the inflatable device for helping the victim. 

  # Live video 

  


https://github.com/Yassmin-gamal/Bracelet-/assets/66153260/62801a7b-30ee-4c7b-9034-28299e075a30



# Decision algorithm
Based on our experimentation and evaluation of various machine learning algorithms, the XGBoost Classifier emerged as the top performer with the highest accuracy of 93.6%. It is renowned for its speed and accuracy and is widely used in data science competitions.

The Gaussian SVM classifier, Linear SVM, and Regular boosting classifier also delivered notable results with an accuracy of 91%. These algorithms have proven to be effective in classification tasks as will be explained 

In terms of deep learning approaches, the LSTM model utilizing all five features achieved the highest accuracy of 91%. LSTM as will be explained, a type of recurrent neural network, is particularly suitable for analyzing time series data and has demonstrated its capability in various applications. The simpler DNN model achieved an accuracy of 90% as will be explained , further highlighting the effectiveness of deep learning methods.

Considering the overall performance and results obtained from our experimentation, we have selected the XGBoost Classifier as the preferred algorithm due to its outstanding accuracy and reputation for achieving excellent results across various problem domains.



# The immediate loss of consciousness situation
 To mitigate the risk of undetected dangerous situations, an additional safety measure can be implemented by integrating an optical heart rate and oxygen saturation sensor, specifically a pulse oximeter, into the wristband. This sensor uses infrared light to see the expansion of your arteries as your heart pumps blood through them. 

By incorporating a pulse oximeter , it becomes possible to monitor the individual's oxygen saturation levels. A significant drop in oxygen saturation can be indicative of the loss of consciousness underwater and the initial stages of drowning. This enables the system to detect potential drowning incidents that may go unnoticed through other means of detection.

The inclusion of a pulse oximeter enhances the effectiveness and reliability of the sensor wristband, providing an additional layer of safety to prevent drowning in unusual and potentially dangerous scenarios.

 # The Disturbed Oxygen Saturation Values
To address the variability and outliers in oxygen saturation values, a method based on the interquartile range (IQR) is implemented. The oxygen saturation values are assumed to follow a normal distribution. The IQR, which represents the range of the middle 50% of the dataset, is used as a measure of variability.

The process of removing outliers illustrated is performed locally within consecutive time windows, each containing 10 measurements. The oxygen saturation values within each window are sorted, and based on the sorted sequence, the IQR is calculated using Equation (1). The lower and upper limits for non-outlier data are then determined using Equation (2) and Equation (3) respectively. When a new oxygen saturation value is received, all previously rejected values from the calculations are reconsidered. This ensures that outliers that were initially discarded are reevaluated in light of the most recent data. 

By applying this approach , the aim is to reduce the impact of outliers and improve the accuracy and reliability of the oxygen saturation measurements for further analysis and detection of potential drowning incidents.

    IRQ = Q3 - Q1                            (1)
    SPO2 (lowertrsh) =Q1−10⋅IRQ              (2)
    SPO2 (uppertrsh) =Q3+10⋅IRQ              (3)

   # Truncated Linear Regression
In order to analyze the relationship between successive values of oxygen saturation, a linear regression model was utilized. However, this regression analysis was applied only to selected data points that were deemed free of outliers, creating a truncated linear regression.

The slope estimator, denoted as b-hat (bˆ), was determined using the ordinary least squares (OLS) method. This method calculates the best-fit line that minimizes the sum of the squared differences between the observed and predicted values. The formula for estimating the oxygen saturation slope (bˆ) using OLS is described by Equation (4).

By performing this truncated linear regression analysis, the aim is to assess the trend or direction of the relationship between successive oxygen saturation values, providing insights into the dynamics of saturation changes over time.
   
        bˆ=cov(t,SPO2) / var(t)                   (4)
where:
              SPO2 is a vector of valid oxygen saturation values without outliers;
              t is a time vector.


# ]ecision algorithm
In order to trigger the alarm and activate the bracelet, a prolonged decrease in both heart rate and oxygen saturation is required. However, relying solely on a single regression slope with a fixed threshold for triggering the alarm proved to be too sensitive to fluctuations in oxygen saturation.

To address this issue, specific threshold values were established for both the oxygen saturation (SPO2) slope and heart rate (HR) slope. The SPO2 slope threshold represents the minimum slope value of oxygen saturation that is not considered dangerous and was set at -0.05 %s. Similarly, the HR slope threshold, indicating the minimum slope value of heart rate that is not considered dangerous, was set at -0.2 bps ز

If the slopes of both SPO2 and HR fall below these respective thresholds, the time_counter is incremented. This counter keeps track of the duration of slope values below the thresholds and triggers the alarm if it exceeds the time threshold set for five consecutive measurements.

To minimize the delay at the beginning of the measurement when a person stops moving if fewer than 10 measurements are available, no outliers are removed from the data.

This decision algorithm diagram outlines the operation and flow of the algorithm, ensuring timely activation of the alarm while considering the dynamic changes in both heart rate and oxygen saturation.

Integrating the two cases of a prolonged decrease in heart rate and oxygen saturation, if either of them is detected as true, we can enable the bracelet to be activated automatically using a servo motor. This integration ensures that in critical situations where a person experiences a significant drop in heart rate or oxygen saturation, the bracelet is immediately triggered to assist in keeping the individual afloat and alerting lifeguards for assistance.

By automating the activation process, we enhance the efficiency and effectiveness of the drowning detection and rescue system. It eliminates the need for manual intervention or delayed response, allowing for rapid assistance and potentially saving lives in emergency situations. The integration of the automatic activation mechanism further enhances the overall safety and reliability of the system.


## Authors
1. Yassmin Gamal.
2. Yara Khalid.
3. Menna Swilam.
 

