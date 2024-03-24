import requests
import os

USER_MANAGEMENT_API_URL = "http://127.0.0.1:8000/user-management/"
CREDIT_CARD_API_URL = "http://127.0.0.1:8000/creditcard-management/"

def login_update_profile_photo_logout(filename: str):
	######### Login #########
	creds = ("user2", "2resu1234")
	login_response = requests.post(USER_MANAGEMENT_API_URL+"login/", auth=creds)
	
	if login_response.status_code != 200:	
		print(f"[ FAIL ] Login as {creds} got unexpected RESPONSE CODE = {login_response.status_code}")
		print(login_response.text)
		return -1

	token = login_response.json()["token"]
	print(f"[ INFO ] Login successful as {creds[0]}\nToken: {token}")

	######### update photo #########
	# file_path = os.path.join("media", "user_avatars", filename)
	# file_path = filename

	headers = {
		"Authorization": f"Token {token}",
		# "Content-Disposition": f"attachment; filename: {filename}",
	}

	files = {"file": (filename, open(filename, "rb"))}
	credit_card_response = requests.put(USER_MANAGEMENT_API_URL+"update-profile-photo/"+filename, headers=headers, files=files)

	print(f"[ TEST ] Profile photo update request status_code: {credit_card_response.status_code}")
	
	if len(credit_card_response.text) <= 120:
		print(credit_card_response.text)
	else:
		with open("test_client.output.log.txt", "a") as f:
			f.write("\n"+credit_card_response.text)
		print(credit_card_response.text[:120], "...")

	######### Logout #########
	logout_response = requests.post(USER_MANAGEMENT_API_URL+"logout/",
						headers={
							"Authorization": f"Token {token}",
						})
	print(f"[ INFO ] Logout status_code: {logout_response.status_code}")
	print(logout_response.text)

def login_create_card_logout(file_path: str):
	""" logs in and attempts to create a credit card via facial recognition auth """
	######### Login #########
	creds = ("user2", "2resu1234")
	login_response = requests.post(USER_MANAGEMENT_API_URL+"login/", auth=creds)
	
	if login_response.status_code != 200:	
		print(f"[ FAIL ] Login as {creds} got unexpected RESPONSE CODE = {login_response.status_code}")
		print(login_response.text)
		return -1

	token = login_response.json()["token"]
	print(f"[ INFO ] Login successful as {creds[0]}\nToken: {token}")

	######### Create Credit Card #########
	# file_path = os.path.join("media", "user_avatars", filename)
	file_path = file_path
	filename = file_path.split("\\")[-1]

	headers = {
		"Authorization": f"Token {token}",
		# "Content-Disposition": f"attachment; filename: {filename}",
	}

	files = {"file": (filename, open(file_path, "rb"))}
	credit_card_response = requests.post(CREDIT_CARD_API_URL+"create/"+filename, headers=headers, files=files)

	print(f"[ TEST ] Credit Card request status_code: {credit_card_response.status_code}")
	
	if len(credit_card_response.text) <= 120:
		print(credit_card_response.text)
	else:
		with open("test_client.output.log.txt", "a") as f:
			f.write("\n"+credit_card_response.text)
		print(credit_card_response.text[:120], "...")

	######### Logout #########
	logout_response = requests.post(USER_MANAGEMENT_API_URL+"logout/",
						headers={
							"Authorization": f"Token {token}",
						})
	print(f"[ INFO ] Logout status_code: {logout_response.status_code}")
	print(logout_response.text)

if __name__ == '__main__':
	PHOTO1 = None
	PHOTO2 = None

	if ((PHOTO1 == None) or (PHOTO2 == None)):
		print("Please configure paths for PHOTO1 and PHOTO2")
		print(f"PHOTO1 = {PHOTO1}\nPHOTO2 = {PHOTO2}")
		quit()

	else:
		login_create_card_logout(file_path=PHOTO1)
		# login_update_profile_photo_logout(filename=PHOTO1)