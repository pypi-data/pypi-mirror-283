import ollama

def test_ollama(number):
    test_system_prompt = (f"Tell me a joke.\n")

    response = ollama.chat(model="llama3", messages=[
        {
            "role": "system",
            "content": test_system_prompt
        }
    ], options={"temperature": 2})

    return response["message"]["content"]