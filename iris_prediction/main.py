from sklearn import datasets, ensemble
import streamlit as st
import pandas as pd

st.title(""" 
Simple Iris Prediction App
         
Using Random Forest Classifier
""")

st.subheader("Data from scikit-learn")

iris = datasets.load_iris(as_frame=True)

def user_input_features():
    sepal_length = st.sidebar.slider("Sepal length", 7.9, 4.3, 5.8)
    sepal_width = st.sidebar.slider("Sepal width", 2.0, 4.4, 3.0)
    petal_length = st.sidebar.slider("Petal Length", 1.0, 6.9, 3.7)
    petal_width = st.sidebar.slider("Petal Width", 0.1, 2.5, 1.2)

    aDict = {"sepal length (cm)": sepal_length,
            "sepal width (cm)": sepal_width,
            "petal length (cm)": petal_length,
            "petal width (cm)": petal_width}
    
    return aDict

st.subheader("Iris Data - First 10 rows")
st.write(iris["data"][0:10])

st.subheader("Iris Data Statistics")
df=pd.DataFrame(iris["data"])
st.write(df.describe())

classifier = ensemble.RandomForestClassifier()
X = iris["data"]
Y = iris["target"]
classifier.fit(X, Y)


st.subheader("Features to predict")
user_df = pd.DataFrame(data=user_input_features(), index=[0])
st.write(user_df)

result = classifier.predict(user_df)
result_prob = classifier.predict_proba(user_df)

st.subheader("Predicted Flower")
st.write(iris.target_names[result])
st.write(result_prob)



