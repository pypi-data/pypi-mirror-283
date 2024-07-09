from promptflow import tool
import urllib.request
import json
import os
import ssl


@tool
def get_place_intelligence_flow_api(allowed, chat_input):
    allowed = True

    if (
        allowed
        and not os.environ.get("PYTHONHTTPSVERIFY", "")
        and getattr(ssl, "_create_unverified_context", None)
    ):
        ssl._create_default_https_context = ssl._create_unverified_context

        data = {"chat_input": json.dumps(chat_input)}

        body = str.encode(json.dumps(data))

        url = "https://place-intelligence-test.eastus.inference.ml.azure.com/score"
        # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
        api_key = "o3qjsPtas1sMG2BYvKCSg8PavCs7gjfr"
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        # The azureml-model-deployment header will force the request to go to a specific deployment.
        # Remove this header to have the request observe the endpoint traffic rules
        headers = {
            "Content-Type": "application/json",
            "Authorization": ("Bearer " + api_key),
            "azureml-model-deployment": "place-intelligence-test",
        }

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            decoded_string = result.decode("utf-8")
            json_data = json.loads(decoded_string)
            chat_output = json_data.get("chat_output", "")

            return chat_output
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", "ignore"))
            return "The request failed with status code: " + str(error.code)
    return False


get_place_intelligence_flow_api(
    allowed=True, chat_input={"message": "양양에 있는 매장 추천해줘", "image": ""}
)
