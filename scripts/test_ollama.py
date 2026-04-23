from langchain_ollama import ChatOllama


def main():

    llm = ChatOllama(
        model="llama3.1",
        temperature=0,
        # other params...
    )

    messages = [
        (
            "system",
            "You are a helpful assistant that analyzes sentiment in English input text and classify it in Urdu. The categories are Postive, Negative and Neutral",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = llm.invoke(messages)
    with open("ur.txt", "w") as file:
        file.write(str(ai_msg.content))
