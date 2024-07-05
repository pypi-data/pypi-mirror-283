# koros_python_payments

A python package for connecting to payments platforms like MPESA,PayPal,RazorPay

## Installation

```bash
pip install koros-python-payments

```

## Configuration

Create an env file and add the following:
Update the configuration according to your needs

```python

MPESA_ENV=0 #0 means the sandbox credentails will be used while 1 means live credentations will be used

#Test
MPESA_TEST_CONSUMER_KEY=""
MPESA_TEST_CONSUMER_SECRET=""
MPESA_TEST_TOKEN_URL="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
MPESA_TEST_INITIATOR="testapi"
MPESA_TEST_PASSWORD="Safaricom999!*!"
MPESA_TEST_B2C_PARTY_A=600997
MPESA_TEST_B2C_RESULT_URL=""
MPESA_TEST_B2C_QUEUE_TIMEOUT_URL=""
MPESA_TEST_B2C_URL="https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
MPESA_TEST_B2C_COMMAND_ID = "BusinessPayment"
MPESA_TEST_BUSINESS_SHORTCODE = 174379
MPESA_TEST_PASSKEY = ""
MPESA_TEST_CUSTOMER_TO_BUSINESS_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
MPESA_TEST_CALLBACK_URL = "http://localhost:8000"
MPESA_TEST_TRANSACTION_QUERY_URL = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"
MPESA_TEST_TRANSACTION_QUERY_RESULT_URL="http://localhost:8000/callback/transaction-query/"
MPESA_TEST_TRANSACTION_QUERY_QUEUE_TIMEOUT_URL="https://localhost/callback/transaction-query"
MPESA_TEST_TRANSACTION_QUERY_IDENTIFIER_TYPE='4'
MPESA_TEST_TRANSACTION_QUERY_COMMAND_ID = "TransactionStatusQuery"
MPESA_TEST_TRANSACTION_QUERY_TRANSACTION_CODE = "OEI2AK4Q16"
MPESA_TEST_TRANSACTION_QUERY_PARTY_A= 600987
MPESA_TEST_TRANSACTION_ORIGINATOR_CONVERSATION_ID = ""
MPESA_TEST_CERT_PATH='./certs/SandboxCertificate.cer' #certificate is already uploaded in the package


#Live
MPESA_LIVE_CONSUMER_KEY=""
MPESA_LIVE_CONSUMER_SECRET=""
MPESA_LIVE_TOKEN_URL="https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
MPESA_LIVE_INITIATOR=""
MPESA_LIVE_PASSWORD=""
MPESA_LIVE_B2C_PARTY_A=""
MPESA_LIVE_B2C_RESULT_URL=""
MPESA_LIVE_B2C_QUEUE_TIMEOUT_URL=""
MPESA_LIVE_B2C_URL="https://api.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
MPESA_LIVE_B2C_COMMAND_ID = "BusinessPayment"
MPESA_LIVE_BUSINESS_SHORTCODE =""
MPESA_LIVE_PASSKEY = ""
MPESA_LIVE_CUSTOMER_TO_BUSINESS_URL = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
MPESA_LIVE_CALLBACK_URL = ""
MPESA_LIVE_TRANSACTION_QUERY_URL = "https://api.safaricom.co.ke/mpesa/transactionstatus/v1/query"
MPESA_LIVE_TRANSACTION_QUERY_RESULT_URL=""
MPESA_LIVE_TRANSACTION_QUERY_QUEUE_TIMEOUT_URL=""
MPESA_LIVE_TRANSACTION_QUERY_IDENTIFIER_TYPE='4'
MPESA_LIVE_TRANSACTION_QUERY_COMMAND_ID = "TransactionStatusQuery"
MPESA_LIVE_TRANSACTION_QUERY_TRANSACTION_CODE = "OEI2AK4Q16"
MPESA_LIVE_TRANSACTION_QUERY_PARTY_A=
MPESA_LIVE_TRANSACTION_ORIGINATOR_CONVERSATION_ID = ""
```


## Make STK Push/ Request payment from user

```python

from mpesa.customer_to_business import CustomerToBusiness

def make_skt_push():
    amount = 1
    phone = "254712345678"
    bill_reference = "12345"
    customer_to_business=CustomerToBusiness()
    repsonse=customer_to_business.stk_push(amount,phone,bill_reference)
    response_code = repsonse.get("ResponseCode","")
    if response_code == "0":
        #Request was  successful, stk sent to customer
        customerMessage = response.get("CustomerMessage","")
        print(customerMessage)
    else:
        #Request was not successful, stk sent to customer
        errorMessage = response.get("errorMessage","")
        print(errorMessage)

```

