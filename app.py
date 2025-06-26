import streamlit as st
import random
from quiz100 import malware_questions, pentest_questions, forensics_questions, cloud_questions
from quiz100 import network_questions, vmware_questions, iot_questions, appsec_questions
from quiz100 import reverse_engineering_questions, cryptography_questions

# Combine all questions
all_questions = malware_questions + pentest_questions + forensics_questions + cloud_questions + \
                network_questions + vmware_questions + iot_questions + appsec_questions + \
                reverse_engineering_questions + cryptography_questions

st.title("🔐 Cybersecurity Field Recommendation Quiz")
st.write("Answer questions based on your interests and programming language knowledge. Get a cybersecurity field recommendation!")

st.sidebar.header("Your Profile")
interests = st.sidebar.multiselect("Choose your cybersecurity interests:", sorted(set(q["field"] for q in all_questions)))
languages = st.sidebar.multiselect("Which programming languages do you know?", sorted(set(q["language_required"] for q in all_questions if q["language_required"] != "N/A")))

def filter_questions(questions, interests, languages):
    return [q for q in questions if q["field"] in interests or q.get("language_required") in languages]

selected_questions = filter_questions(all_questions, interests, languages)
random.shuffle(selected_questions)
selected_questions = selected_questions[:10]

user_answers = {}

if selected_questions:
    st.header("📝 Quiz Questions")
    for idx, q in enumerate(selected_questions):
        user_choice = st.radio(f"Q{idx+1}: {q['question']}", q['options'], key=q['id'])
        user_answers[q["id"]] = user_choice

    if st.button("Submit Quiz"):
        score = 0
        field_scores = {}
        for q in selected_questions:
            correct = q["correct_answer"]
            user = user_answers.get(q["id"])
            if user == correct:
                score += 1
                field_scores[q["field"]] = field_scores.get(q["field"], 0) + 1

        st.success(f"✅ Your Total Score: {score}/{len(selected_questions)}")

        if field_scores:
            max_score = max(field_scores.values())
            top_fields = [f for f, s in field_scores.items() if s == max_score]
            st.markdown("### 🧠 Recommended Field(s):")
            for f in top_fields:
                st.markdown(f"- **{f}**")
        else:
            st.warning("⚠️ No strong recommendation based on current answers.")
else:
    st.info("⬅️ Select your interests and languages to start the quiz.")
