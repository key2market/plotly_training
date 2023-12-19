import functions as f

context = f.load_prompts("prompts", "generate_question.txt", "context.txt", "question")
print(context)
