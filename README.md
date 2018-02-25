# NewsMultirank

## How to use the fake/poor news detector ?

First, do git clone the repo in the command line:

```git clone repo
cd NewsMultirrank
pip3 -r install requirements.txt 
```

To run the app:
```./server 
python3 app.py
```
Now save to post:
```
localhost:8000/prediction
```
*(Warnings : port can change and has to be checked)*

## Some explanations

From the chrome extension , we do post request to this endpoint with a json that contains title and text of an online article.  
It activates the flask and runs the tensorflow program and gives a response to flask. This will be deployed by the chrome extension.
 
 
 
