from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv
from pprint import pprint

def main():
    model = ChatOpenRouter(
        model="openai/gpt-oss-120b:free",
        temperature=0,
        max_tokens=1024,
        max_retries=2,
        # other params...
    )


    messages = [
        (
            "system",
            "You are a helpful assistant that analyzes sentiment in English input text and classify it in Urdu. The categories are Postive, Negative and Neutral",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = model.invoke(messages)
    with open("ur.txt", "w") as file:
        file.write(str(ai_msg.content))



if __name__=="__main__":
    load_dotenv(".env")
    main()

