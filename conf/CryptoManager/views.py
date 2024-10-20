# from .eth_connection import contract, w3
import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from web3 import Web3
from .serializers import CertificateSerializer
import traceback
import os

ganache_url = 'http://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
if not web3.is_connected():
    raise Exception("Failed to connect to Ganache")

def load_abi():
    with open(os.path.join('CryptoManager', 'abis', 'contract_abi.json'), 'r') as abi_file:
        return json.load(abi_file)

contract_abi = load_abi()
contract_address = '0x28565C5BE280D0f1987BbA30d821F0794f3743D7'
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
user_address = '0x7317cc78e1384E8E9FcDA2404c4f62B4CAC87A16'


@api_view(['GET'])
def get_user_certificates(request,user_address):
    if not user_address:
        return Response({'error': 'user_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        certificate_addresses = contract.functions.getUserCertificateAddresses(user_address).call()

        if not certificate_addresses:
            return Response({'message': 'No certificates found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        # serializer = CertificateSerializer(many=True)
        return Response(certificate_addresses)

    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_certificate(request, id,user_address):

    try:
        certificate_ids, certificate_data = contract.functions.getUserCertificateAddresses(user_address).call()
        if id not in certificate_ids:
            return Response({'message': 'No certificate found for this ID.'}, status=status.HTTP_404_NOT_FOUND)

        index = certificate_ids.index(id)
        return Response({
            'id': certificate_ids[index],
            'data': certificate_data[index]
        })

    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def issue_certificate(request):
    user_address = '0x7317cc78e1384E8E9FcDA2404c4f62B4CAC87A16'
    reviewer_address = '0xEC53481b1a1a2EE7EBCf3fd07Ca62cD2024b3b43'
    data = 'Certificate data here'
    pdf_link = 'http://link-to-pdf.com'


    try:
        tx_hash = contract.functions.issueCertificate(user_address, reviewer_address, data, pdf_link).transact({
            'from': '0x7317cc78e1384E8E9FcDA2404c4f62B4CAC87A16',
            'gas': 2000000,
        })
        return Response({'message': 'Certificate issued successfully.', 'tx_hash': tx_hash.hex()}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def check_status(request, contract_address, token_id):
    try:
        status = contract.functions.getCertificateStatus(token_id).call()
        return Response({'token_id': token_id, 'status': status})
    except Exception as e:
        return Response({'error': str(e)}, status=400)