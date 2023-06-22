Özön, Derin, 

Thura, Aw, 

Tumor Predictor 2023.1

https://mygit.th-deg.de/diminished7/sas-ds-app

# Project Description

Tumor Predictor 2023.1 is a desktop app that predicts if a MRI scan of a brain contains a tumor.
More info found in the [Wiki](https://mygit.th-deg.de/diminished7/sas-ds-app/-/wikis/home)

# Installation

	pip install -r .\requirements.txt

# Basic Usage

The app might take a while to start, a splash image is provided as a loading screen. Once the app is live there are two sliders that change Entropy and Homogeneity respectively. Each time a slider value is changed the visualisation and the perdiction updates with given values.

# Implementation of the Requests

## Implemented
	• A Desktop App with PyQT6 has to be developed.
	• A requirements.txt file must be used to list the used Python modules
	• A README.md file must be created with the structure described in part 01.
	• The module venv must be used.
	• A free data source must be used. You may find it for example at Kaggle,
	SciKit (but not the built-in ones), or other
	• There must be a data import (predefined format and content of CSV)
	• The data must be analyzed with Pandas methods, so that a user gets on overview.
	• You may use the functions dataframe.info(), dataframe.describe() and/or dataframe.corr()
	for that.
	• You may also use other metrics or diagrams to do this.
	• A Scikit training model algorithm (e.g. from Aurélien Géron, Chapter 4) must be applied.
	• Pandas and Numpy may be used optionally
	• Create 1 or 2 output canvas, i.e. for data visualization
	• The app must react to the change of input parameter with a new prediction with visualization.
	• Create at least 3 input widgets (2 must be different) that change some feature variables.
	• At least 3 statistical metrics over the input data must be shown

## Not Implemented
	• The data must be read from a file after clicking on a (menu) button.


# Work done

Aw Thura - Making visualisations and creating the model <br>
Derin Ozon - Creating the interface and connecting the model
