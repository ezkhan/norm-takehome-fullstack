from openai import OpenAI
client = OpenAI(api_key="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")

response = client.responses.create(
    model="gpt-5-nano",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
