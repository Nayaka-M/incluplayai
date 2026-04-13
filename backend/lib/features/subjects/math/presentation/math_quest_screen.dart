import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../gamification/providers/gamification_provider.dart';

class MathQuestScreen extends ConsumerStatefulWidget {
  const MathQuestScreen({super.key});
  @override
  ConsumerState<MathQuestScreen> createState() => _MathQuestScreenState();
}

class _MathQuestScreenState extends ConsumerState<MathQuestScreen> {
  int _score = 0;
  int _current = 0;

  final List<Map<String, dynamic>> _questions = [
    {"q": "What is 12 x 12?", "options": ["124", "144", "132", "148"], "answer": "144"},
    {"q": "What is the square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"q": "What is 25% of 200?", "options": ["25", "40", "50", "75"], "answer": "50"},
    {"q": "Solve: 3x = 21, x = ?", "options": ["5", "6", "7", "8"], "answer": "7"},
  ];

  void _answer(String selected) {
    final correct = _questions[_current]["answer"];
    if (selected == correct) {
      setState(() => _score++);
      ref.read(gamificationProvider.notifier).addPoints(10);
    }
    if (_current < _questions.length - 1) {
      setState(() => _current++);
    } else {
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text("Quiz Complete!"),
          content: Text("Score: \$_score / \${_questions.length}\n+\${_score * 10} points earned!"),
          actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text("OK"))],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("Math Quest"), backgroundColor: Colors.blue),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Question \${_current + 1} / \${_questions.length}", style: const TextStyle(color: Colors.grey)),
            const SizedBox(height: 20),
            Text(q["q"], style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 30),
            ...(q["options"] as List<String>).map((opt) => Padding(
              padding: const EdgeInsets.only(bottom: 12),
              child: ElevatedButton(
                onPressed: () => _answer(opt),
                style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 50)),
                child: Text(opt, style: const TextStyle(fontSize: 16)),
              ),
            )),
            const SizedBox(height: 20),
            Text("Score: \$_score", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }
}
