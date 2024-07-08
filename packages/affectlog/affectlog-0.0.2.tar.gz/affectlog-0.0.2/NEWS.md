## Changelog

### v0.0.2 (2024-02-28)

* **Dependencies:**
  * Increased the dependencies to `python>=3.8`, `pandas>=1.5.0`, `numpy>=1.23.3`.
  * Added `python==3.11` to CI.
* **TensorFlow/Keras Compatibility:**
  * Added `keras.src.models.sequential.Sequential` to classes with a known `predict_function`; this fixes changes in `keras==3.0.0` and `tensorflow==2.16.0`.
  * Turned off `verbose` in the predict method of tensorflow/keras models to address changes in `tensorflow>=2.9.0`.
* **Warnings and Errors:**
  * Updated the warning occurring when specifying `variable_splits`.
  * Fixed an error occurring in `predict_profile()` when a DataFrame has MultiIndex in `pandas>=1.3.0`.
  * Fixed Gaussian `norm()` calculation in `model_profile()` from `pi*sqrt(2)` to `sqrt(2*pi)`.
  * Fixed a warning (future error) between `prepare_numerical_categorical()` and `prepare_x()` with `pandas==2.1.0`.
  * Fixed a warning (future error) concerning the default value of `numeric_only` in `pandas.DataFrame.corr()` in `affectlog.aspect.calculate_assoc_matrix()`.
* **Explainer Enhancements:**
  * Improved `Explainer` object to better handle new dependencies and compatibility issues.

### v0.0.1 (2023-12-16) 

* **Precision and Recall Functions:**
  * Added handling for `ZeroDivisionError` in precision and recall functions to prevent crashes.
* **Warnings and Alerts:**
  * Added a warning to `calculate_depend_matrix()` when there is a variable with only one value to notify users of potential issues.
* **Exploratory Data Analysis (EDA) Plots:**
  * Fixed missing EDA plots in the AL360 module, enhancing the visualization and analysis capabilities.
* **Predict Parts Explanations:**
  * Fixed baseline positions in the subplots of the predict parts explanations: BreakDown, Shap, ensuring accurate visual representation.
* **Model and Predict Enhancements:**
  * Improved model and predict functionalities to align with the latest updates and user feedback.
