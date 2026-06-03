import sys
from nutricompare.main import build_application
from nutricompare.application.dto.chat_request import ChatRequest

question = " ".join(sys.argv[1:]) or "How many calories are in 2 eggs and 100g chicken?"

print("\n================ LIVE BACKEND FLOW ================\n")

print("0) User Question")
print("   →", question)

app = build_application()

ask_use_case = getattr(app, "ask_nutrition_question_use_case", None)
if ask_use_case is None:
    ask_use_case = getattr(app, "ask_question_use_case", None)

if ask_use_case is None:
    print("\nERROR: Could not find AskNutritionQuestionUseCase in application container.")
    print("Available attributes:")
    print(dir(app))
    sys.exit(1)

print("\n1) ChatRequest is created")
request = ChatRequest(user_question=question)
print("   → ChatRequest(user_question=...)")

print("\n2) AskNutritionQuestionUseCase.execute() is called")
print("   → It forwards request.user_question to ChatService")

response = ask_use_case.execute(request)

print("\n3) ChatService finished processing")
print("   → Returned ChatResponse")

answer = response.result

print("\n4) NutritionAnswer created")
print("   → Contains original question + Model A response + Model B response")

print("\n5) Model A Response")
print("   Model:", answer.model_a_response.provider, "/", answer.model_a_response.model_name)
print("   Answer preview:")
print(answer.model_a_response.answer[:800])

print("\n6) Model B Response")
print("   Model:", answer.model_b_response.provider, "/", answer.model_b_response.model_name)
print("   Answer preview:")
print(answer.model_b_response.answer[:800])

print("\n7) Final answer is ready to be shown in the UI")
print("   → Streamlit displays Model A answer, Model B answer, and later judge/evaluation data.")

print("\n================ END OF FLOW ================\n")
