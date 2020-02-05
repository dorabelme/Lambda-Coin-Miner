import requests
import json
import time


class Dreamy:
    def get(self, URL=None, headers=None, cooldown=1):
        if not URL:
            raise Exception("No URL supplied")

        successful = False
        while not successful:
            try:
                response = requests.get(
                    URL,
                    headers=headers
                ).json()
                if "errors" in response and response["errors"]:
                    print(f"Error: {response['errors']}")
                    cooldown = response["cooldown"]
                    time.sleep(cooldown)
                else:
                    successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)

        return response

    def post(self, URL=None, headers=None, data={}, cooldown=1):
        if not URL:
            return {"errors": ["No URL supplied"]}

        successful = False
        while not successful:
            try:
                response = requests.post(
                    URL,
                    headers=headers,
                    data=json.dumps(data),
                ).json()
                if "errors" in response and response["errors"]:
                    print(f"Error: {response['errors']}")
                    cooldown = response["cooldown"]
                    time.sleep(cooldown)
                else:
                    successful = True
            except ValueError:
                print("Error:  Non-json response")
                print("Response returned:")
                print(response)

        return response


dreamy = Dreamy()
