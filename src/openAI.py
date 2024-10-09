from openai import OpenAI
client = OpenAI()

def get_gpt_responce(document_text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial expert assistant at  Securities and Exchange Commission."},
            {
                "role": "user",
                "content": f"Based on the following text from an S-1 form document, determine if it is an IPO filing. Just reply with 'yes' or 'no'.\n\n{document_text}"
            }
        ]
    )
    return completion.choices[0].message['content'].strip()

