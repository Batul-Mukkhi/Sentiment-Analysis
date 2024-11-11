# Sentiment Analysis Using RNN for Sequential Text Data

This project implements sentiment analysis using a Recurrent Neural Network (RNN) to classify text data into positive or negative sentiment. The model is trained on sequential text data, leveraging RNN's capability to understand context over a sequence of words or sentences.

## Project Overview

Sentiment analysis is the process of determining the emotion behind text, often used to assess customer feedback, social media posts, and reviews. By implementing an RNN, this project demonstrates how neural networks can be trained to understand sequential relationships in text, enabling accurate predictions of sentiment.

## Features

- Data preprocessing and tokenization of text
- Embedding layers for word vectorization
- RNN layers for sequential processing
- Training, validation, and testing of the model
- Evaluation metrics including accuracy, precision, and recall

## Dataset

For this project, we use a dataset of movie reviews that are labeled as positive or negative. You can use any dataset with labeled text for sentiment analysis. Common options include:

- [IMDb Movie Reviews](https://ai.stanford.edu/~amaas/data/sentiment/)
- [Twitter Sentiment Analysis](https://www.kaggle.com/c/twitter-sentiment-analysis2)

Ensure the dataset has two columns: `text` (review) and `label` (sentiment).

## Prerequisites

Make sure you have the following dependencies installed:

- Python (version 3.6 or higher)
- TensorFlow (version 2.0 or higher)
- NumPy
- pandas
- matplotlib
## Usage

1. Download the IMDb movie review dataset from the provided link.
2. Extract the dataset and locate the train and test folders.
3. Update the paths to the train and test folders in the code, as specified in the comments.
4. Run the `model.py` script.


