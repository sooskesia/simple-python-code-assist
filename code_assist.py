import sys
import openai

openai.api_key = "YOUR_API_KEY"

def code_assist(prompt):
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=100,
        temperature=0.2,
        stop=["#", "\"\"\""]
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else ""
    suggestion = code_assist(user_input)
    print(suggestion)
