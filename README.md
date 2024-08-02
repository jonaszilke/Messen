# Messen

This project contains a bunch of webscraping scripts, that are used to get information for all exhibitors on a trade fair.

## Table of Contents

- [Messen](#messen)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)

## Description

You can find example files in the ```./2024/June``` directory.
Please use the files ```cableworld.py```, ```chemspec.py``` and ```deutschevet.py``` as orientation.
There are also templates for new exhibition-scripts in ```./templates/...```.

## Installation

Install all required packages with 
```bash
pip install .
```
Ensure that the appropriate WebDriver for your browser version is installed and configured before running the scripts.
In this project we used the Chrome Driver. If another browser is used, please adapt the file ```config.py```