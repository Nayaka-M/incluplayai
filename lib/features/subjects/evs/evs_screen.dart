import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import '../../gamification/providers/gamification_provider.dart';
import '../../history/score_history_screen.dart';

class EVSScreen extends ConsumerStatefulWidget {
  const EVSScreen({super.key});
  @override
  ConsumerState<EVSScreen> createState() => _EVSScreenState();
}

class _EVSScreenState extends ConsumerState<EVSScreen> {
  int _score = 0;
  int _current = 0;
  bool _finished = false;
  bool _loading = true;
  String? _error;
  String? _selectedAnswer;
  bool _answered = false;
  List<Map<String, dynamic>> _questions = [];

  @override
  void initState() {
    super.initState();
    _loadQuestions();
  }

  Future<void> _loadQuestions() async {
    setState(() { _loading = true; _error = null; });
    try {
      final res = await http.post(
        Uri.parse('http://127.0.0.1:8000/quiz'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'subject': 'Environmental Studies (EVS)', 'grade': 'Grade 8'}),
      ).timeout(const Duration(seconds: 30));
      final data = jsonDecode(res.body);
      final qs = List<Map<String, dynamic>>.from(data['questions']);
      if (qs.isEmpty) throw Exception('No questions returned');
      setState(() { _questions = qs; _loading = false; });
    } catch (e) {
      setState(() { _error = e.toString(); _loading = false; });
    }
  }

  void _answer(String selected) {
    if (_answered) return;
    final correct = selected == _questions[_current]["answer"];
    setState(() { _selectedAnswer = selected; _answered = true; if (correct) _score++; });
    if (correct) ref.read(gamificationProvider.notifier).addPoints(10);
    Future.delayed(const Duration(milliseconds: 900), () {
      if (!mounted) return;
      if (_current < _questions.length - 1) {
        setState(() { _current++; _selectedAnswer = null; _answered = false; });
      } else {
        ref.read(gamificationProvider.notifier).completeQuiz();
        ref.read(gamificationProvider.notifier)
            .updateSubjectProgress('EVS', _score, _questions.length);
        ScoreHistory.addScore("EVS", _score, _questions.length);
        setState(() => _finished = true);
      }
    });
  }

  Color _buttonColor(String opt) {
    if (!_answered) return Colors.white;
    if (opt == _questions[_current]["answer"]) return Colors.green.shade100;
    if (opt == _selectedAnswer) return Colors.red.shade100;
    return Colors.white;
  }

  Color _buttonBorder(String opt) {
    if (!_answered) return Colors.grey.shade300;
    if (opt == _questions[_current]["answer"]) return Colors.green;
    if (opt == _selectedAnswer) return Colors.red;
    return Colors.grey.shade300;
  }

  @override
  Widget build(BuildContext context) {
    const color = Color(0xFF3B6D11);
    if (_loading) return _buildLoading(color);
    if (_error != null) return _buildError(color);
    if (_finished) return _buildFinished(color);

    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("EVS Quest"), backgroundColor: color, foregroundColor: Colors.white),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          LinearProgressIndicator(
            value: (_current + 1) / _questions.length,
            color: color, backgroundColor: Colors.grey.shade200),
          const SizedBox(height: 8),
          Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            Text("Question ${_current + 1} / ${_questions.length}",
                style: const TextStyle(color: Colors.grey)),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(20)),
              child: Row(children: [
                Icon(Icons.auto_awesome, size: 14, color: color),
                const SizedBox(width: 4),
                Text("AI Generated", style: TextStyle(fontSize: 11, color: color, fontWeight: FontWeight.w500)),
              ]),
            ),
          ]),
          const SizedBox(height: 16),
          Text(q["q"] ?? q["question"] ?? '', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          ...(q["options"] as List).map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: GestureDetector(
              onTap: () => _answer(opt.toString()),
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
                decoration: BoxDecoration(
                  color: _buttonColor(opt.toString()),
                  border: Border.all(color: _buttonBorder(opt.toString()), width: 1.5),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(opt.toString(), style: const TextStyle(fontSize: 16)),
              ),
            ),
          )),
          const SizedBox(height: 8),
          Text("Score: $_score", style: const TextStyle(fontSize: 16, color: Colors.grey)),
        ]),
      ),
    );
  }

  Widget _buildLoading(Color color) => Scaffold(
    appBar: AppBar(title: const Text("EVS Quest"), backgroundColor: color, foregroundColor: Colors.white),
    body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      CircularProgressIndicator(color: color),
      const SizedBox(height: 20),
      const Text("Generating AI questions...", style: TextStyle(fontSize: 16)),
      const SizedBox(height: 8),
      Text("Powered by Groq + NCERT syllabus", style: TextStyle(fontSize: 13, color: Colors.grey[600])),
    ])),
  );

  Widget _buildError(Color color) => Scaffold(
    appBar: AppBar(title: const Text("EVS Quest"), backgroundColor: color, foregroundColor: Colors.white),
    body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      const Icon(Icons.wifi_off, size: 60, color: Colors.grey),
      const SizedBox(height: 16),
      const Text("Could not connect to backend", style: TextStyle(fontSize: 16)),
      const SizedBox(height: 24),
      ElevatedButton.icon(
        onPressed: _loadQuestions,
        icon: const Icon(Icons.refresh),
        label: const Text("Try Again"),
        style: ElevatedButton.styleFrom(backgroundColor: color, foregroundColor: Colors.white),
      ),
    ])),
  );

  Widget _buildFinished(Color color) => Scaffold(
    appBar: AppBar(title: const Text("EVS"), backgroundColor: color, foregroundColor: Colors.white),
    body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      const Icon(Icons.celebration, size: 80, color: Color(0xFF3B6D11)),
      const SizedBox(height: 16),
      Text("Score: $_score / ${_questions.length}",
          style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
      Text("+${_score * 10} points earned!", style: const TextStyle(fontSize: 18, color: Colors.green)),
      const SizedBox(height: 8),
      Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(20)),
        child: Row(mainAxisSize: MainAxisSize.min, children: [
          Icon(Icons.auto_awesome, size: 16, color: color),
          const SizedBox(width: 6),
          Text("Questions were AI-generated", style: TextStyle(color: color, fontSize: 13)),
        ]),
      ),
      const SizedBox(height: 24),
      ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("Back to Dashboard")),
      const SizedBox(height: 12),
      TextButton.icon(
        onPressed: () {
          setState(() { _score = 0; _current = 0; _finished = false; _selectedAnswer = null; _answered = false; });
          _loadQuestions();
        },
        icon: const Icon(Icons.refresh),
        label: const Text("Try New Questions"),
      ),
    ])),
  );
}