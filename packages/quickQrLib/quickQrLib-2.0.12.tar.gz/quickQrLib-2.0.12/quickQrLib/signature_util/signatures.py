from django import utils
from django.conf import settings 
from rest_framework.response import Response
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json
import base64
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.status import HTTP_403_FORBIDDEN
import logging
from django.http import HttpResponse
import os
from typing import List, Dict


logger = logging.getLogger(__name__)

current_directory = os.path.dirname(os.path.abspath(__file__))
# print("CURRENT DIRECTORY:", current_directory)

pem_file_path = os.path.join(current_directory, "public_key.pem")
# print("pem_file_path:", pem_file_path)

def load_public_key(pem_file_path):
    try:
        # Read the PEM file
        with open(pem_file_path, "rb") as pem_file:
            pem_data = pem_file.read()
        
        # Load the public key from the PEM data
        public_key = serialization.load_pem_public_key(
            pem_data,
            backend=default_backend()
        )
        # print("public_key:", public_key)
        logger.info("Public key loaded successfully.")
        return public_key
    except Exception as e:
        print(f"ERROR LOADING PUBLIC KEY: {e}\n\n")
        logger.error(f"Error loading public key: {e}")
        return None

public_key = load_public_key(pem_file_path)
    
class SignatureActions:
    '''Where permissions are a dictionary of permissions'''
    @classmethod
    def sign_permissions(cls, permissions)->List[Dict]:
        signed_permissions = []
        msg = ""
        status_code = status.HTTP_100_CONTINUE
        try:
            private_key = serialization.load_pem_private_key(
                settings.PRIVATE_KEY,
                password=None,
                backend=default_backend()
            )
            if permissions:
                for permission in permissions:
                    json_permission = json.dumps(permission, default=str)
                    signature = private_key.sign(
                        json_permission.encode('utf-8'),
                        padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                        ),
                        hashes.SHA256()
                    )
                    permission["signature"] = base64.b64encode(signature).decode('utf-8')
                    signed_permissions.append(permission)
            else:
                msg = "No permissions to sign"
                status_code = status.HTTP_400_BAD_REQUEST                
                return msg, status_code, False
        except Exception as e:
            # Handle the exception (log, raise, etc.)
            print(f"Error signing permissions: {e}")
            logger.error(f"Error signing permissions: '{type(e).__name__}'")
            msg = "Error signing permissions"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return msg, status_code, False
        status_code = status.HTTP_200_OK
        return signed_permissions, status_code, True 
              
    @classmethod
    def verify_header_permissions(cls, permission, signature):
        if permission and signature:
            signature_bytes = base64.b64decode(signature)
            try:
                json_permission= json.loads(permission)
                json_dumped_permission = json.dumps(json_permission, default=str)
                public_key.verify(
                    signature_bytes,
                    json_dumped_permission.encode('utf-8'),
                    # data_to_verify,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                return json_permission
            except Exception as e:
                logger.error(f"Error verifying header permissions:'{str(e)}'")
                return False
        return False

class SignatureCheckMixin:
    def __init__ (self, permission_type = 'model', *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        permission_result, special_result = self.is_signature_valid(request)
        #Returns permissions dictionary if valid, else empty dict
        if not permission_result and not special_result:
            return HttpResponse('message: Invalid permissions', status=403)
        else:
            request.permission= permission_result
            request.special_permission= special_result
            return super().dispatch(request, *args, **kwargs)

    def is_signature_valid(self, request):
        # Check the signature 
        permission = None 
        signature = None
        special_permission = None
        special_signature = None
        if request.META.get('HTTP_PERMISSION'):  
            permission = request.META.get('HTTP_PERMISSION')
            signature = request.META.get('HTTP_PERMISSION_SIGNATURE')
        if request.META.get('HTTP_SPECIAL_PERMISSION'):
            special_permission = request.META.get('HTTP_SPECIAL_PERMISSION')
            special_signature = request.META.get('HTTP_SPECIAL_PERMISSION_SIGNATURE')   
        return SignatureActions.verify_header_permissions(permission, signature, special_permission, special_signature)
    
if __name__ == '__main__': 
    pass