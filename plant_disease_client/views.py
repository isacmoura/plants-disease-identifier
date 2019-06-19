import datetime
import pickle
import boto3
import json
import os
import base64
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from api.settings import BASE_DIR

from custom import image_converter

ACCESS_KEY = 'AKIAX6QDEDMNNXOWS7UJ'
SECRET_KEY = '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'

s3client = boto3.client('s3',
                        aws_access_key_id = ACCESS_KEY, 
                        aws_secret_access_key = SECRET_KEY, 
)

#response = s3client.get_object()

@api_view(['GET'])
def __index__function(request):
    return render(request, 'index.html', {})

@api_view(['POST'])
def predict_feedback(request):
    try:
        return None
    except Exception as e:
        return None

@api_view(['POST','GET'])
def predict_plant_disease(request):
    try:
        if request.method == "GET" :
            return render(request, 'predict.html')
        else:
            if request.body:
                request_data = request.data["plant_image"]

                file_txt = open(f"{datetime.datetime.now()}.txt", 'w')
                file_txt.write(request_data)
                file_txt.close()
                
                
                header, image_data = request_data.split(';base64,')
                image_array, err_msg = image_converter.convert_image(image_data)
                if err_msg == None :
                    model_file = f"{BASE_DIR}/ml/conv_model.pk1"
                    saved_classifier_model = pickle.load(open(model_file,'rb'))
                    prediction = saved_classifier_model.predict(image_array) 
                    label_binarizer = pickle.load(open(f"{BASE_DIR}/ml/label_transform.pk1",'rb'))
                    return_data = {
                        "error" : "0",
                        "data" : f"{label_binarizer.inverse_transform(prediction)[0]}"
                    }
                else :
                    return_data = {
                        "error" : "4",
                        "message" : f"Error : {err_msg}"
                    }
            else :
                return_data = {
                    "error" : "1",
                    "message" : "Request Body is empty",
                }
    except Exception as e:
        return_data = {
            "error" : "3",
            "message" : f"Error : {str(e)}",
        }
    return HttpResponse(json.dumps(return_data), content_type='application/json; charset=utf-8')