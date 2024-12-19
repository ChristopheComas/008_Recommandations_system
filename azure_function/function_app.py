import azure.functions as func
import logging
import json
import pickle
from implicit.als import AlternatingLeastSquares
import scipy.sparse as sp
from scipy.sparse import coo_matrix
import numpy as np

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="recommandationv5", methods=["GET"])

def recommandations(req: func.HttpRequest) -> func.HttpResponse:

    # Get user_id from query parameters or request body
    user_id = req.params.get('user_id')

    # Load model and files
    try:
        # Ensure the model is loaded properly
        model = AlternatingLeastSquares(factors=50, use_gpu=False)
        model =  model.load("model_als.npz")
    except Exception as e:
        return func.HttpResponse(
            "Error loading model", status_code=500
        )

    try:
        with open("user_mapping.pkl", "rb") as f:
            user_mapping = pickle.load(f)

        with open("article_mapping.pkl", "rb") as f:
            article_mapping = pickle.load(f)

        sparse_matrix = sp.load_npz("sparse_matrix.npz")
    except Exception as e:
        return func.HttpResponse(
            "Error loading mappings or sparse matrix", status_code=500
         )

    if not user_id:
        try:
            req_body = req.get_json()
        except ValueError:
            req_body = {}
        user_id = req_body.get('user_id')

    


    # erreur arrive dans ce bloc DEBUT 
    if user_id:

        idx_user = user_mapping[int(user_id)]

        try:
            # recommend items for a user
            recommendations = model.recommend(idx_user, sparse_matrix[idx_user], N=10)[0].tolist()
            
            articles_recommended = []
            for idx in recommendations :
                for article in article_mapping.items() :
                    if article[1] == idx :
                        articles_recommended.append(article[0])
                        break
        except Exception as e:
            return func.HttpResponse(
                "Error while predicting", status_code=500
            )
     # erreur arrive dans ce bloc FIN 
   


        response = {
            "recommandations": [int(i) for i in articles_recommended]
        }

    return func.HttpResponse(
            body=json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )
