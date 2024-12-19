# Context
-----------
In this study, we explore different recommandation system for a newspaper magazine.

# Tech used
--------------
* ALS : matrice factorization for collaborative implicit filtering
* Cosine_similarity approach : find the best related article based on article embeddings 
* Model evaluation: custom metrics based on hitpoint (1 point if recommandation is present on the 10 next readings)
* Model deployment : Azure Function
* Front end : Streamlit