import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../gamification/providers/gamification_provider.dart';
import '../../../history/score_history_screen.dart';
import '../../../../core/api/ai_tutor_service.dart';

class ScienceQuestScreen extends ConsumerStatefulWidget {
  const ScienceQuestScreen({super.key});
  @override
  ConsumerState<ScienceQuestScreen> createState() => _ScienceQuestScreenState();
}

class _ScienceQuestScreenState extends ConsumerState<ScienceQuestScreen> {
  int _score = 0;
  int _current = 0;
  bool _finished = false;
  bool _loading = true;
  List<Map<String, dynamic>> _questions = [];

  @override
  void initState() {
    super.initState();
    _loadQuestions();
  }

  Future<void> _loadQuestions() async {
    final aiService = AiTutorService();
    final questions = await aiService.generateQuiz("Science", "Grade 8");
    setState(() {
      _questions = questions.isNotEmpty ? questions : _fallbackQuestions();
      _loading = false;
    });
  }

  List<Map<String, dynamic>> _fallbackQuestions() => [
    {"q": "What gas do plants absorb during photosynthesis?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"q": "Largest planet?", "options": ["Earth", "Saturn", "Jupiter", "Mars"], "answer": "Jupiter"},
    {"q": "Boiling point of water?", "options": ["50C", "75C", "100C", "120C"], "answer": "100C"},
    {"q": "Powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "answer": "Mitochondria"},
    {"q": "Bones in adult human body?", "options": ["196", "206", "216", "226"], "answer": "206"},
  ];

  void _answer(String selected) {
    if (selected == _questions[_current]["answer"]) {
      setState(() => _score++);
      ref.read(gamificationProvider.notifier).addPoints(10);
    }
    if (_current < _questions.length - 1) {
      setState(() => _current++);
    } else {
      ref.read(gamificationProvider.notifier).completeQuiz();
      ScoreHistory.addScore("Science", _score, _questions.length);
      setState(() => _finished = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return Scaffold(
        appBar: AppBar(title: const Text("Science Quest"), backgroundColor: Colors.purple, foregroundColor: Colors.white),
        body: const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          CircularProgressIndicator(color: Colors.purple),
          SizedBox(height: 16),
          Text("AI is generating fresh questions...", style: TextStyle(fontSize: 16)),
        ])),
      );
    }
    if (_finished) {
      return Scaffold(
        appBar: AppBar(title: const Text("Science"), backgroundColor: Colors.purple, foregroundColor: Colors.white),
        body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Icon(Icons.celebration, size: 80, color: Colors.purple),
          const SizedBox(height: 16),
          Text("Score: $_score / ${_questions.length}", style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          Text("+${_score * 10} points earned!", style: const TextStyle(fontSize: 18, color: Colors.green)),
          const SizedBox(height: 24),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("Back to Dashboard")),
          const SizedBox(height: 12),
          ElevatedButton.icon(
            onPressed: () { setState(() { _loading = true; _score = 0; _current = 0; _finished = false; }); _loadQuestions(); },
            icon: const Icon(Icons.refresh),
            label: const Text("Play Again with New Questions"),
            style: ElevatedButton.styleFrom(backgroundColor: Colors.purple, foregroundColor: Colors.white),
          ),
        ])),
      );
    }
    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("Science Quest"), backgroundColor: Colors.purple, foregroundColor: Colors.white),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          LinearProgressIndicator(value: (_current + 1) / _questions.length, color: Colors.purple),
          const SizedBox(height: 8),
          Text("Question ${_current + 1} / ${_questions.length}", style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 12),
          Text(q["q"], style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          ...(q["options"] as List).map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: ElevatedButton(
              onPressed: () => _answer(opt.toString()),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              child: Text(opt.toString(), style: const TextStyle(fontSize: 16)),
            ),
          )),
          Text("Score: $_score", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }
}