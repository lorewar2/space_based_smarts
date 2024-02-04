from openai import OpenAI

client = OpenAI(api_key='') 
# messages = [ {"role": "system", "content": 
# 			"You are a intelligent assistant."} ] 
# while True: 
# 	message = input("User : ") 
# 	if message: 
# 		messages.append( 
# 			{"role": "user", "content": message}, 
# 		) 
# 		chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages) 
# 	reply = chat.choices[0].message.content 
# 	print(f"ChatGPT: {reply}") 
# 	messages.append({"role": "assistant", "content": reply}) 

Deficulity = input("Enter the deficulity of the question: ")
Subject = input("Enter the subject of the question: ")

messages = [{"role": "system", "content": "You are an intelligent assistant. This is for a highschool student. Generate a multiple-choice question in mathematics and answer in the format: Question? A) Option 1 B) Option 2 C) Option 3 D) Option 4. Indicate the correct answer."}]

def parse_reply(reply):
    try:
        # Split the reply to separate the question from the options
        parts = reply.split("\nA")
        question = parts[0].strip()
        options_part = "A" + parts[1].strip()

        # Split the options part to get individual options
        options = options_part.split("\nB")
        option_a = options[0].strip()
        options = options[1].split("\nC")
        option_b = options[0].strip()
        options = options[1].split("\nD")
        option_c = options[0].strip()
        option_parts = options[1].split(".")
        option_d = option_parts[0].strip()

        # Assuming the correct answer is explicitly stated after the options
        # This line might need adjustment based on how the correct answer is presented
        correct_answer = option_parts[-1].strip().split(" ")[-1].strip()

        return question, option_a, option_b, option_c, option_d, correct_answer
    except IndexError:
        # If parsing fails due to unexpected format, return None values
        return None, None, None, None, None, None



while True:
    message = input("User (enter 'generate' to create a question or 'exit' to quit): ")
    if message.lower() == 'exit':
        break
    elif message.lower() == 'generate':
        try:
            chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
            reply = chat.choices[0].message.content
            question, option_a, option_b, option_c, option_d, correct_answer = parse_reply(reply)
            print(f"ChatGPT: {reply}")
            print("Question:", question)
            print("Option A:", option_a)
            print("Option B:", option_b)
            print("Option C:", option_c)
            print("Option D:", option_d)
            print("Correct Answer:", correct_answer)
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid input. Please type 'generate' to create a question or 'exit' to quit.")
