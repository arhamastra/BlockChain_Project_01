Blockchain API
A simple blockchain implementation with a REST API built using Flask. This project can be run locally, on Google Colab, or deployed to Render.

Features
Create transactions
Mine blocks with Proof of Work
Validate blockchain integrity
RESTful API endpoints
API Endpoints
GET / - API information
POST /transaction/new - Create a new transaction
GET /mine - Mine a new block
GET /chain - Get the full blockchain
GET /validate - Validate the blockchain
Running Locally
Install dependencies:
bash
pip install -r requirements.txt
Run the application:
bash
python blockchain_app.py
Access the API at http://localhost:5000
Running on Google Colab
Upload Blockchain_Colab.ipynb to Google Colab
Get your ngrok token from ngrok dashboard
Run each cell in order
Use the generated public URL to access your API
Deploying to Render
Step 1: Prepare Your GitHub Repository
Create a new repository on GitHub
Add these files to your repository:
blockchain_app.py
requirements.txt
README.md
Step 2: Deploy on Render
Go to Render and sign up/login
Click "New +" and select "Web Service"
Connect your GitHub repository
Configure the service:
Name: blockchain-api (or your preferred name)
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn blockchain_app:app
Click "Create Web Service"
Your API will be deployed and accessible at the provided Render URL!

Usage Examples
Create a Transaction
bash
curl -X POST http://your-url/transaction/new \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "Alice",
    "recipient": "Bob",
    "product_data": "Product A"
  }'
Mine a Block
bash
curl http://your-url/mine
Get the Blockchain
bash
curl http://your-url/chain
Validate the Blockchain
bash
curl http://your-url/validate
Project Structure
blockchain-api/
├── blockchain_app.py      # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── Blockchain_Colab.ipynb # Google Colab notebook
Technologies Used
Python 3
Flask - Web framework
Gunicorn - WSGI HTTP Server
Hashlib - Cryptographic hashing
License
MIT License

