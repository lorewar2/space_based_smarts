from openai import OpenAI

client = OpenAI(api_key='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') 

def generate_question(Deficulity, Subject):
    messages = [{"role": "system", "content": f"You are an intelligent assistant. This is for a {Deficulity} student. Generate a multiple choice question in {Subject} and answer in the format: Question? A) Option 1 B) Option 2 C) Option 3 D) Option 4. Indicate the correct answer."}]
    chat = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages) 
    reply = chat.choices[0].message.content

    question, option_a, option_b, option_c, option_d, correct_answer = parse_reply(reply)
    #print(f"ChatGPT: {reply}")
    print("Question:", question)
    print("Option A:", option_a)
    print("Option B:", option_b)
    print("Option C:", option_c)
    print("Option D:", option_d)
    print("Correct Answer:", correct_answer)
    messages.append({"role": "assistant", "content": reply})
    # print(f"ChatGPT: {reply}") 
    # messages.append({"role": "assistant", "content": reply})
    return question, option_a, option_b, option_c, option_d, correct_answer

#messages = [{"role": "system", "content": "You are an intelligent assistant. This is for a highschool student. Generate a multiple-choice question in mathematics and answer in the format: Question? A) Option 1 B) Option 2 C) Option 3 D) Option 4. Indicate the correct answer."}]

def parse_reply(reply):
    """
    Parses the reply from the ChatGPT model to extract the question, options, and the correct answer.
    """
    # Initialize variables to ensure they are bound even if parsing fails.
    question = option_a = option_b = option_c = option_d = correct_answer = "Not found"
    try:
        parts = reply.split("A)")
        question = parts[0].split("Question:")[-1].strip()
        options_part = parts[1]

        options = options_part.split(" B)")
        option_a = options[0].strip()
        option_b = options[1].split(" C)")[0].strip()
        option_c = options[1].split(" C)")[1].split(" D)")[0].strip()
        option_d = options[1].split(" C)")[1].split(" D)")[1].split(".")[0].strip()
        correct_answer= options[1].split(" C)")[1].split(" D)")[1].split(')')[1].strip()

        # New logic to extract the correct answer
        # correct_answer_prefix = "The correct answer is "
        # if correct_answer_prefix in reply:
        #     start_index = reply.index(correct_answer_prefix) + len(correct_answer_prefix)
        #     correct_answer = reply[start_index:start_index + 3]  # Assuming format is "X)"
        # else:
        #     correct_answer = "Unknown"  # Fallback if the format doesn't match

    except Exception as e:

        return question, option_a, option_b, option_c, option_d, correct_answer
    except IndexError:
        # If parsing fails due to unexpected format, log an error and return None values
        print("Failed to parse the reply correctly.")
        return None, None, None, None, None, None