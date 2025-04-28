# pip install azure-ai-inference
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from ai import API_KEY

debug = True

def email_generation(query):
  # Alliant's OpenAI key should go here
  # API key is found at: Azure > rcualfml > Launch Studio > Endpoints > Azure OpenAI Services > malfgpt-4o-mini > Key
  api_key = API_KEY.api_key

  # property_address = '830 33rd St, Boulder, CO 80303' # sample address
  property_address = query

  # Specific endpoint to use
  client = ChatCompletionsClient(
      # Will eventually use final tuned model for endpoint
      endpoint='https://rcualfopenai4.openai.azure.com/openai/deployments/malfgpt-4o-mini',
      credential=AzureKeyCredential(api_key)
  )

  payload = {
    "messages": [
      {
        "role": "user",

        # Sample payload with generic response
        "content": "Generate an email to send to a realtor of a home sale, from the seller. Include the address" + str(property_address) + " in the email and state that you have new banking details ready to send over. Generate bank numbers for Alpine Bank. Signature should be short: just the name."

        ### Update to this payload for final model
        # "content": property_address
      }
    ],
    "max_tokens": 4096,
    "temperature": 1,
    "top_p": 1,
    "stop": []
  }
  response = client.complete(payload)

  print("Response:", response.choices[0].message.content) # reponse field (actual message being printed)

  return(response.choices[0].message.content)

  # Below is the details about the model and usage
  # print("Model:", response.model)
  # print("Usage:")
  # print("	Prompt tokens:", response.usage.prompt_tokens)
  # print("	Total tokens:", response.usage.total_tokens)
  # print("	Completion tokens:", response.usage.completion_tokens)