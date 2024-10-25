# from .eth_connection import contract, w3
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from web3 import Web3
from .serializers import UserContractAddressSerializer
import traceback
import os
from rest_framework import serializers

ganache_url = 'http://127.0.0.1:7545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
if not web3.is_connected():
    raise Exception("Failed to connect to Ganache")

def load_abi():
    with open(os.path.join('CryptoManager', 'abis', 'contract_abi.json'), 'r') as abi_file:
        return json.load(abi_file)

contract_abi = load_abi()



@api_view(['GET'])
def get_user_certificates(request):
    user_address = request.data.get('user_address')
    contract_address = request.data.get('contract_address')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    print(request)

    if not user_address:
        return Response({'error': 'user_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        certificate_addresses = contract.functions.getUserCertificates(user_address).call()

        if not certificate_addresses:
            return Response({'message': 'No certificates found for this user.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(certificate_addresses)

    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_certificate(request, id):
    user_address = request.data.get('user_address')
    contract_address = request.data.get('contract_address')

    if not user_address:
        return Response({'error': 'user_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    if not contract_address:
        return Response({'error': 'contract_address is required'}, status=status.HTTP_400_BAD_REQUEST)

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    try:
        certificates = contract.functions.getUserCertificates(user_address).call()

        for cert in certificates:
            if cert[0] == id:
                return Response({
                    'id': cert[0],
                    'data': cert[1],
                    'owner': cert[2],
                    'issuer': cert[3],
                    'status': cert[4],
                    'link': cert[5],
                    'isVerified': cert[6],
                    'type': cert[7],
                })

        return Response({'message': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def issue_certificate(request):
    contract_address = request.data.get('contract_address')
    user_address = request.data.get('user_address')
    reviewer_address = request.data.get('reviewer_address')
    data = request.data.get('data')
    pdf_link = request.data.get('pdf_link')

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    try:
        tx_hash = contract.functions.issueCertificate(user_address, reviewer_address, data, pdf_link).transact({
            'from': '0xD8c9972925aE666373fc31A1472643D388555199',
            'gas': 2000000,
        })
        return Response({'message': 'Certificate issued successfully.', 'tx_hash': tx_hash.hex()}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def check_status(request, token_id):
    contract_address = request.data.get('contract_address')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    try:
        status = contract.functions.getCertificateStatus(token_id).call()
        return Response({'token_id': token_id, 'status': status})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def get_bytecode_and_abi(request):
    try:
        file_path_bytecode = 'CryptoManager/bytecode/bytecode.bin'
        file_path_abi = 'CryptoManager/abis/contract_abi.json'

        if not os.path.exists(file_path_bytecode):
            return Response({'error': 'Bytecode  not found'}, status=status.HTTP_404_NOT_FOUND)
        if not os.path.exists(file_path_abi):
            return Response({'error': 'ABI file not found'}, status=status.HTTP_404_NOT_FOUND)

        with open(file_path_bytecode, 'rb') as f:
            bytecode_data = f.read().decode('utf-8')

        with open(file_path_abi, 'r') as f:
            abi_data = json.load(f)

        return Response({
            'bytecode': bytecode_data,
            'abi': abi_data
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
