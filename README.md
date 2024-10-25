# NFTVC-achievements
CryptoManager API
CryptoManager is a blockchain-based certificate management system that allows users to issue, manage, and verify certificates using Ethereum smart contracts. The system interacts with the blockchain through Web3 and provides a REST API for certificate-related operations.

# Stack
Python/Django: API Framework for backend services.
Web3.py: Python library for interacting with the Ethereum blockchain.
Ganache: Local Ethereum blockchain for development and testing.
Ethereum Smart Contracts: Smart contracts manage certificates and transactions.
REST Framework: Django REST Framework for API building.
# API Endpoints
1. Get User Certificates
GET /api/user-certificates/

Retrieve all certificates associated with a user's Ethereum address.

Request Parameters (in JSON body):

user_address: Public Ethereum address of the user.
contract_address: Address of the deployed smart contract managing certificates.
Response:

A list of certificate addresses or a 404 if no certificates are found.
Example Request:

{
  "user_address": "0x123...",
  "contract_address": "0x456..."
}
2. Get a Specific Certificate
GET /api/certificates/{id}/

Retrieve details of a specific certificate by its ID.

Request Parameters (in JSON body):

user_address: Public Ethereum address of the user.
contract_address: Address of the deployed smart contract.
Response:

Detailed certificate data, including ID, owner, issuer, status, and more.
Example Request:

{
  "user_address": "0x123...",
  "contract_address": "0x456..."
}
3. Issue a New Certificate
POST /api/issue-certificate/

Issue a new certificate to a user by interacting with the Ethereum smart contract.

Request Parameters (in JSON body):

contract_address: Smart contract's Ethereum address.
user_address: Ethereum address of the certificate recipient.
reviewer_address: Ethereum address of the certificate reviewer.
data: Metadata for the certificate.
pdf_link: Link to the certificate in PDF format.
Response:

Returns a success message and the transaction hash.
Example Request:

{
  "contract_address": "0x789...",
  "user_address": "0x123...",
  "reviewer_address": "0x456...",
  "data": "Certificate Data",
  "pdf_link": "link"
}
4. Check Certificate Status
GET /api/check-status/{token_id}/

Check the status of a certificate by its token ID.

Request Parameters (in JSON body):

contract_address: Smart contract's Ethereum address.
Response:

Returns the certificate status (e.g., valid, revoked).
Example Request:

{
  "contract_address": "0x456..."
}
5. Get Smart Contract ABI and Bytecode
GET /api/contract/

Fetches the ABI and bytecode for the deployed smart contract.

Response:

Returns the contract's ABI and bytecode files.
# Installation and Setup
1. Clone the repository:
git clone <repository_url>
cd CryptoManager
2. Install dependencies:
pip install -r requirements.txt
3. Run
python manage.py runserver
<!-- 3. Setup Ganache:
Ensure Ganache is installed and running on http://127.0.0.1:7545.
Update the ganache_url variable in your views if needed.
4. Configure Smart Contracts:
Deploy your smart contract to Ganache.
Save the ABI file in CryptoManager/abis/contract_abi.json and bytecode in CryptoManager/bytecode/bytecode.bin.
5. Start the Django development server:
python manage.py runserver

Quickstart with Docker
Clone the repository:

git clone <repository_url>
cd CryptoManager
Build and start the application using Docker Compose:

docker-compose up --build -->
