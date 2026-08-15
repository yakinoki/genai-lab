import os

from google import genai


def main():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain what a Forward Deployed Engineer does in three sentences.",
    )

    print(response.text)


if __name__ == "__main__":
    main()