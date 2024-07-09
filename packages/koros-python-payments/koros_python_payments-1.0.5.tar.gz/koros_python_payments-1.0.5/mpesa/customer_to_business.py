import base64
import datetime
import requests
import os

from dotenv import load_dotenv
from .access_token import AccessToken
load_dotenv()


class CustomerToBusiness:	
	def stk_push(self,amount, phone,bill_reference,transaction_description =""):
		if transaction_description == "":
			transaction_description = "Payment REquest for Bill Reference "+bill_reference
		time = datetime.datetime.now()
		timestamp = time.strftime('%Y%m%d%H%M%S')
		if os.getenv('MPESA_ENV') == "1":
			api_url = os.getenv('MPESA_LIVE_CUSTOMER_TO_BUSINESS_URL')
			data = os.getenv('MPESA_LIVE_BUSINESS_SHORTCODE') + os.getenv('MPESA_LIVE_PASSKEY') + timestamp
			callback_url = os.getenv('MPESA_LIVE_CALLBACK_URL')
			busines_shortcode = os.getenv('MPESA_LIVE_BUSINESS_SHORTCODE')
		else:
			api_url = os.getenv('MPESA_TEST_CUSTOMER_TO_BUSINESS_URL')
			data = os.getenv('MPESA_TEST_BUSINESS_SHORTCODE') + os.getenv('MPESA_TEST_PASSKEY') + timestamp
			callback_url = os.getenv('MPESA_TEST_CALLBACK_URL')
			busines_shortcode = os.getenv('MPESA_TEST_BUSINESS_SHORTCODE')
		encoded_string = base64.b64encode(data.encode())
		password = encoded_string.decode('utf-8')
		token = AccessToken()
		access_token=token.get_access_token()
		headers = {"Authorization": "Bearer %s" % access_token }
		request = {
            "BusinessShortCode": busines_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": busines_shortcode,
            "PhoneNumber": phone,
            "CallBackURL": callback_url,
            "AccountReference": bill_reference,
            "TransactionDesc": transaction_description
        }
		response = requests.post(api_url, json = request, headers=headers)
		json_response = response.json()
		return (json_response)
	
	def decode_stk_callback(self,data):
		body = data.get('Body', {})
		stk_callback = body.get('stkCallback', {})
		merchant_request_id = stk_callback.get('MerchantRequestID', '')
		checkout_request_id = stk_callback.get('CheckoutRequestID', '')
		result_code = stk_callback.get('ResultCode', '')
		result_desc = stk_callback.get('ResultDesc', '')
		callback_metadata = stk_callback.get('CallbackMetadata', {})
		items = callback_metadata.get('Item', [])

		mpesa_transaction_code =None
		phone_number = None
		transaction_date =None
		amount =None 

		for item in items:
			name = item.get('Name', '')
			value = item.get('Value', '')
			if name == "Amount":
				amount = value
			if name == "TransactionDate":
				transaction_date = value
			if name == "PhoneNumber":
				phone_number = value
			if name == "MpesaReceiptNumber":
				mpesa_transaction_code = value
				
		decoded_data = {
			'merchant_request_id': merchant_request_id,
			'checkout_request_id' : checkout_request_id,
			'result_code' : result_code,
			'result_description': result_desc,
			'amount': amount,
			'mpesa_transaction_code': mpesa_transaction_code,
			'transaction_date' : transaction_date,
			'phone_number' :phone_number
		}
		return decoded_data
	    
