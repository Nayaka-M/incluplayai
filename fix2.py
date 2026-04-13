import os

fixes = [
    ("lib/features/dashboard/presentation/dashboard_screen.dart", [
        (r'"\${progress.points}"', '"${progress.points}"'),
        (r'"\${progress.streak}d"', '"${progress.streak}d"'),
        (r'"\${progress.quizzesCompleted}"', '"${progress.quizzesCompleted}"'),
        (r"'\$baseUrl/ask'", "'$baseUrl/ask'"),
        (r'"Server error: \${response.statusCode}"', '"Server error: ${response.statusCode}"'),
        (r'"\$studentName!"', '"$studentName!"'),
        (r'"\$studentName"', '"$studentName"'),
    ]),
    ("lib/core/api/ai_tutor_service.dart", [
        (r"'\$baseUrl/ask'", "'$baseUrl/ask'"),
        (r'"Server error: \${response.statusCode}"', '"Server error: ${response.statusCode}"'),
    ]),
    ("lib/features/subjects/math/presentation/math_quest_screen.dart", [
        (r'"Score: \$_score / \${_questions.length}"', '"Score: $_score / ${_questions.length}"'),
        (r'"+\${_score * 10} points earned!"', '"+${_score * 10} points earned!"'),
        (r'"Question \${_current + 1} / \${_questions.length}"', '"Question ${_current + 1} / ${_questions.length}"'),
        (r'"Score: \$_score"', '"Score: $_score"'),
    ]),
    ("lib/features/subjects/science/presentation/science_quest_screen.dart", [
        (r'"Score: \$_score / \${_questions.length}"', '"Score: $_score / ${_questions.length}"'),
        (r'"+\${_score * 10} points earned!"', '"+${_score * 10} points earned!"'),
        (r'"Question \${_current + 1} / \${_questions.length}"', '"Question ${_current + 1} / ${_questions.length}"'),
        (r'"Score: \$_score"', '"Score: $_score"'),
    ]),
    ("lib/features/subjects/tamil/tamil_screen.dart", [
        (r'"Score: \$_score / \${_questions.length}"', '"Score: $_score / ${_questions.length}"'),
        (r'"+\${_score * 10} points earned!"', '"+${_score * 10} points earned!"'),
        (r'"Question \${_current + 1} / \${_questions.length}"', '"Question ${_current + 1} / ${_questions.length}"'),
        (r'"Score: \$_score"', '"Score: $_score"'),
    ]),
    ("lib/features/subjects/evs/evs_screen.dart", [
        (r'"Score: \$_score / \${_questions.length}"', '"Score: $_score / ${_questions.length}"'),
        (r'"+\${_score * 10} points earned!"', '"+${_score * 10} points earned!"'),
        (r'"Question \${_current + 1} / \${_questions.length}"', '"Question ${_current + 1} / ${_questions.length}"'),
        (r'"Score: \$_score"', '"Score: $_score"'),
    ]),
]

for filepath, replacements in fixes:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    changed = "FIXED" if content != original else "no changes"
    print(f"{changed}: {filepath}")

print("\nDone! Press R in Flutter terminal for hot restart.")