import re

fixes = {
    "lib/features/dashboard/presentation/dashboard_screen.dart": [
        ('"\${progress.points}"', '"${progress.points}"'),
        ('"\${progress.streak} days"', '"${progress.streak} days"'),
        ('"\${_score * 10} points earned!"', '"${_score * 10} points earned!"'),
        ('"\${_current + 1} / \${_questions.length}"', '"${_current + 1} / ${_questions.length}"'),
        ('"\${_score} / \${_questions.length}\\\\n+\${_score * 10} points earned!"', '"${_score} / ${_questions.length}\\n+${_score * 10} points earned!"'),
        ('Text("\$_score")', 'Text("$_score")'),
    ],
    "lib/core/api/ai_tutor_service.dart": [
        (r'"\$baseUrl/ask"', '"$baseUrl/ask"'),
        (r'"Server error: \${response.statusCode}"', '"Server error: ${response.statusCode}"'),
    ],
    "lib/features/subjects/math/presentation/math_quest_screen.dart": [
        ('"\${_current + 1} / \${_questions.length}"', '"${_current + 1} / ${_questions.length}"'),
        ('"\${_score * 10} points earned!"', '"${_score * 10} points earned!"'),
        ('"Score: \$_score / \${_questions.length}\\\\n+\${_score * 10} points earned!"', '"Score: \$_score / \${_questions.length}\\n+\${_score * 10} points earned!"'),
        ('Text("\$_score")', 'Text("$_score")'),
    ],
    "lib/features/subjects/science/presentation/science_quest_screen.dart": [
        ('"\${_current + 1} / \${_questions.length}"', '"${_current + 1} / ${_questions.length}"'),
        ('"\${_score * 10} points earned!"', '"${_score * 10} points earned!"'),
        ('"Score: \$_score / \${_questions.length}\\\\n+\${_score * 10} points earned!"', '"Score: \$_score / \${_questions.length}\\n+\${_score * 10} points earned!"'),
        ('Text("\$_score")', 'Text("$_score")'),
    ],
}

for filepath, replacements in fixes.items():
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed: {filepath}")

print("\nAll fixed! Now press R in the Flutter terminal for hot restart.")