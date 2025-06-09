# SpectraBias-TruthTuner-2025
SpectraBias -- Your lens into media alignment | Bias Detection in Indian News Articles

**SpectraBias** is a project designed to detect political bias in Indian Published English news articles. It combines a machine learning model with a web interface to analyze and visualize the ideological leaning (Left, Centre, Right) of headlines or full articles.

**Truth Tuner** is a contest for developing a machine learning model that can detect bias in news articles published in India. The goal is to create an algorithm that can accurately assess the degree and direction (left or right) of bias in the content, helping users understand how news may be skewed based on political or ideological leanings.

# News Bias Detection Project
This repository contains the codebase and methodology behind our project: News Bias Detection[_SpectraBias_]. Our goal is to build a robust system that can classify Indian English news articles and headlines into political orientations — left-leaning, centrist, or right-leaning — based on their language and content features.

## Overview

- Developed a transformer-based classifier **_[google/bigbird-roberta-base]_**
- Curated and labeled a dataset from multiple news sources
- Built a user-friendly web interface to test the model
- Designed with extensibility and research in mind

## Folder Structure

- `/Dataset-Collection` – Code and Architecture for Dataset Collection
- `/Model` – Code and configs for training the model
- `/WebApp` – Code for running the browser-based app

## Dataset Notice

We created our own dataset using custom scripts and manual labeling. However, we have **not made the dataset public**. If you're a researcher or student interested in using it for non-commercial purposes, feel free to contact us.

## Technologies Used
- Python
- Jupyter Notebook
- Beautiful Soup, Selenium, Request, RE
- Transformers (Hugging Face)
- google/bigbird-roberta-base
- NLTK, Scikit-Learn, WandB, Pandas
- Matplotlib, Seaborn (for visualizations)

## License

- The **code** in this repository is under the [MIT License](./LICENSE)
- The **documentation, reports, dataset, and methodology** are under the [Creative Commons Attribution-NonCommercial 4.0 License](./CC_LICENSE.txt)


## Acknowledgements

This project draws a source of inspiration for improvement purposes from [Media Bias Analysis in Indian News Articles](https://github.com/coderishabh11/Media-Bias-Analysis-in-Indian-News-Articles) by [coderishabh11](https://github.com/coderishabh11), which is licensed under the MIT License. We have reused and adapted certain parts of their code and methodology in our own work.

We thank the original authors for their contribution to the open-source community.

We are similarly indebted to the Google News Service and various Indian media outlets for contributing towards our dataset.


## Final Thoughts

We believe that transparency in media is essential, and building tools to detect bias is a step toward that goal. Contributions, feedback, or collaborations are always welcome.


## Contact

If you’d like access to the dataset or want to collaborate:
- Email: [abhirup1504@gmail.com] or [swar16.work@gmail.com]
