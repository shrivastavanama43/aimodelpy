# AI Health Akinator style Q&A in Python (console app)

QUESTIONS = {
    "physical": [
        {"id": "polyuria", "text": "Do you feel excessive thirst or urination? (yes/no)"},
        {"id": "fatigue", "text": "Are you experiencing unexplained tiredness frequently? (yes/no)"},
        {"id": "bp_headache", "text": "Do you often get headaches or blurred vision? (yes/no)"},
        {"id": "wheezing", "text": "Do you experience wheezing or shortness of breath? (yes/no)"},
        {"id": "smoking", "text": "Do you smoke or use tobacco products? (yes/no)"},
        {"id": "age", "text": "What's your age? (type a number)"}
    ],
    "mental": [
        {"id": "sleep_change", "text": "Have you noticed changes in your sleep patterns? (yes/no)"},
        {"id": "mood_low", "text": "Do you often feel down, depressed, or hopeless? (yes/no)"},
        {"id": "worry", "text": "Do you experience excessive worry or panic? (yes/no)"},
        {"id": "concentrate", "text": "Is concentrating on tasks difficult lately? (yes/no)"},
        {"id": "stressors", "text": "Please describe any major stressors (work, exams, relationships) below."}
    ]
}

def mock_infer(domain, answers):
    score = 0
    if domain == "physical":
        if answers.get("polyuria") == "yes": score += 3
        if answers.get("fatigue") == "yes": score += 2
        if answers.get("bp_headache") == "yes": score += 2
        if answers.get("wheezing") == "yes": score += 3
        if answers.get("smoking") == "yes": score += 2
        age = int(answers.get("age", "0")) if answers.get("age", "0").isdigit() else 0
        if age > 45: score += 1

        diabetesScore = (0.6 if answers.get("polyuria") == "yes" else 0) + (0.3 if answers.get("fatigue") == "yes" else 0) + (0.1 if age > 45 else 0)
        hypertensionScore = (0.6 if answers.get("bp_headache") == "yes" else 0) + (0.2 if answers.get("smoking") == "yes" else 0)
        asthmaScore = (0.8 if answers.get("wheezing") == "yes" else 0)

        return {
            "overall": min(100, score * 10),
            "predictions": [
                {"name": "Diabetes (suspected)", "prob": round(diabetesScore * 100)},
                {"name": "Hypertension (suspected)", "prob": round(hypertensionScore * 100)},
                {"name": "Asthma (suspected)", "prob": round(asthmaScore * 100)}
            ]
        }
    else:
        # mental health
        if answers.get("sleep_change") == "yes": score += 2
        if answers.get("mood_low") == "yes": score += 4
        if answers.get("worry") == "yes": score += 3
        if answers.get("concentrate") == "yes": score += 2
        if len(answers.get("stressors", "").strip()) > 10: score += 1

        depression = (0.7 if answers.get("mood_low") == "yes" else 0) + (0.2 if answers.get("sleep_change") == "yes" else 0)
        anxiety = (0.7 if answers.get("worry") == "yes" else 0) + (0.2 if answers.get("concentrate") == "yes" else 0)
        stress = (0.6 if len(answers.get("stressors", "")) > 10 else 0) + (0.2 if answers.get("worry") == "yes" else 0)

        return {
            "overall": min(100, score * 12),
            "predictions": [
                {"name": "Depression (suspected)", "prob": round(depression * 100)},
                {"name": "Anxiety (suspected)", "prob": round(anxiety * 100)},
                {"name": "Stress (suspected)", "prob": round(stress * 100)}
            ]
        }

def main():
    print("Welcome to AI Health Akinator (Console Version)")
    domain = ""
    while domain not in ["physical", "mental"]:
        domain = input("Would you like to screen for [physical] or [mental] health? ").strip().lower()

    answers = {}
    for q in QUESTIONS[domain]:
        ans = input(q["text"] + " ").strip().lower()
        # For yes/no questions validate entries
        if 'yesno' in q.get('type', '') or "yes/no" in q["text"]:
            while ans not in ['yes', 'no', 'maybe'] and q["id"] != "age":
                print("Please answer with 'yes', 'no', or 'maybe'.")
                ans = input(q["text"] + " ").strip().lower()
        answers[q["id"]] = ans

    result = mock_infer(domain, answers)

    print("\nAI Health Akinator Results:")
    print(f"Overall risk score: {result['overall']}%")
    print("Findings:")
    for p in result['predictions']:
        seriousness = 'High' if p['prob'] >= 70 else 'Moderate' if p['prob'] >= 40 else 'Low'
        print(f" - {p['name']}: {p['prob']}% risk (Suggested seriousness: {seriousness})")

    print("\nLifestyle recommendations (quick):")
    print("- Maintain balanced diet: reduce refined sugar, increase vegetables & lean protein.")
    print("- Daily light exercise: 30 minutes brisk walk or home workout.")
    print("- Sleep hygiene: consistent sleep schedule, avoid screens 1 hour before bed.")
    print("- For respiratory symptoms: avoid smoking, check for allergies/asthma triggers.")
    print("- Seek professional help for moderate/high mental health scores.")

if _name_ == "_main_":
    main()
