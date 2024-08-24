# Overview

<!-- Create and deploy ML project -->
## ML model creation 

- Collect data
- Create a model using `sklearn` and save it using `pickle`
- Create a `streamlit` app to run the model
- Upload the app to `GitHub`
- Create an account on `streamlit`
- Deploy the app on `streamlit`

<!-- https://sentiment-analys.streamlit.app/ -->

## Git and GitHub Steps

- `git init` - Initialize a local git repository
- `git add .` - Add all files to staging area
- `git commit -m "message"` - Commit changes to local repository
- `git remote add origin <remote repository URL>` - Add a remote repository
- `git remote -v` - Verify remote repository
- `git push -u origin master` - Push changes to remote repository

# Sentiment Analysis

- This is a simple project to demonstrate the deployment of a machine learning model using `streamlit` and `GitHub`.
- The model is trained on the `Reddit` dataset to classify the sentiment of a movie review as positive, negative and negative.
- The model is trained using `sklearn` and saved using `pickle`.
- The model is a `Logistic Regression` model.
- Accuracy of the model is `0.89`.
- The model is deployed on `streamlit` and can be accessed [here](https://sentiment-analys.streamlit.app/).