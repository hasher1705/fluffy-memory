import os

from django.shortcuts import redirect, render
from rest_framework.decorators import api_view

from hfc_poc.settings import BASE_DIR


# Create your views here.
@api_view(['POST'])
def upload(request):
    loan_number = request.data.get('loan_number')
    document_type = request.data.get('document_type')
    uploaded_file = request.FILES.get('document')
    user_folder = os.path.join(BASE_DIR, 'details', str(loan_number), str(document_type))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    img_save_path = os.path.join(user_folder, uploaded_file.name)
    with open(img_save_path, 'wb+') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    return redirect("documents/")


@api_view(['GET'])
def get_loan_numbers(request):
    loan_number_dir = os.path.join(BASE_DIR, "details")
    loan_number_list = os.listdir(loan_number_dir)
    context = {
        'loan_number_list': loan_number_list
    }
    return render(request, 'core/display.html', context)


@api_view(['POST'])
def get_json_response(request):
    loan_number = request.data.get('loan_number')
    document_type = request.data.get('document_type')
    document_dir = os.path.join(BASE_DIR, "details", str(loan_number), str(document_type))
    if os.path.isdir(document_dir):
        data = {"message": "Success"}
    else:
        data = {"message": document_type + " does not exist for loan number:" + loan_number}

    return render(request, 'core/display_output.html', data)
