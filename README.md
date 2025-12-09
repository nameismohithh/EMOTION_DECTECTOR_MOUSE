Mouse Emotion Detection Using Mouse Movement Patterns

This project implements a machine learning–based system that predicts a user’s emotional state in real time using mouse movement patterns. The system analyzes behavioral data such as movement speed, acceleration, smoothness, and click activity to classify emotions. All data for the model is self-generated, and no external datasets are required.

The project provides:

A script for collecting labeled mouse movement data

A machine learning training pipeline (designed for Google Colab)

A real-time graphical interface for emotion detection

A fully offline workflow once the model is trained

This repository demonstrates a novel application of behavioral biometrics in human–computer interaction.

Features

Self-collected behavioral dataset (mouse movement + timestamps)

Real-time emotion prediction using a Random Forest classifier

GUI-based visualization of predicted emotions

No external image, audio, or text datasets required

Platform-independent Python implementation

Modular code structure for reuse and extension

Emotions Detected

The system is designed to classify the following emotion categories:

Calm

Focused

Stressed

Angry

These classes may be modified or extended depending on the user’s dataset.
-----------------------------------------------------------------------------------------

System Overview
1. Data Collection

Mouse movements and click events are captured using the pynput library.
Each data point includes:

X and Y position

Timestamp

Click information

User-provided emotion label

The output is stored in mouse_raw_data.csv.

2. Feature Extraction

During training, the following features are computed:

Time difference (Δt)

Distance between successive points

Movement speed

Click flag

3. Model Training

A Random Forest classifier is trained on the extracted features.
Training is performed in Google Colab for convenience.

The resulting files are:

mouse_mood_model.sav

mouse_mood_label_encoder.sav

4. Real-Time Prediction

A Tkinter-based GUI displays the predicted emotion in real time.
The system updates predictions every 200 milliseconds based on a sliding window of recent mouse movements.
