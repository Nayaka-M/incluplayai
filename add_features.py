import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {path}")

write("lib/main.dart", """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'features/auth/login_screen.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IncluPlayAI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.green), useMaterial3: true),
      home: const LoginScreen(),
    );
  }
}
""")

write("lib/features/auth/login_screen.dart", """
import 'package:flutter/material.dart';
import '../dashboard/presentation/dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _nameController = TextEditingController();
  String _selectedGrade = "Grade 8";
  final List<String> _grades = ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"];

  void _startLearning() {
    if (_nameController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Please enter your name!")));
      return;
    }
    Navigator.pushReplacement(context, MaterialPageRoute(
      builder: (_) => DashboardScreen(studentName: _nameController.text.trim(), grade: _selectedGrade),
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Colors.green[700]!, Colors.blue[600]!],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.school, size: 80, color: Colors.white),
                  const SizedBox(height: 16),
                  const Text("IncluPlayAI", style: TextStyle(fontSize: 36, fontWeight: FontWeight.bold, color: Colors.white)),
                  const Text("AI-Powered Learning for Every Child", style: TextStyle(fontSize: 16, color: Colors.white70)),
                  const SizedBox(height: 40),
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(20)),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text("Welcome! Tell us about yourself", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 20),
                        TextField(
                          controller: _nameController,
                          decoration: InputDecoration(
                            labelText: "Your Name",
                            prefixIcon: const Icon(Icons.person),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                        ),
                        const SizedBox(height: 16),
                        DropdownButtonFormField<String>(
                          value: _selectedGrade,
                          decoration: InputDecoration(
                            labelText: "Select Grade",
                            prefixIcon: const Icon(Icons.grade),
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          items: _grades.map((g) => DropdownMenuItem(value: g, child: Text(g))).toList(),
                          onChanged: (v) => setState(() => _selectedGrade = v!),
                        ),
                        const SizedBox(height: 24),
                        ElevatedButton(
                          onPressed: _startLearning,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green[700],
                            foregroundColor: Colors.white,
                            minimumSize: const Size(double.infinity, 56),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          ),
                          child: const Text("Start Learning!", style: TextStyle(fontSize: 18)),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
""")

write("lib/features/history/score_history_screen.dart", """
import 'package:flutter/material.dart';

class ScoreEntry {
  final String subject;
  final int score;
  final int total;
  final DateTime date;
  ScoreEntry({required this.subject, required this.score, required this.total, required this.date});
}

class ScoreHistory {
  static final List<ScoreEntry> _history = [];
  static void addScore(String subject, int score, int total) {
    _history.insert(0, ScoreEntry(subject: subject, score: score, total: total, date: DateTime.now()));
  }
  static List<ScoreEntry> get history => _history;
}

class ScoreHistoryScreen extends StatelessWidget {
  const ScoreHistoryScreen({super.key});
  @override
  Widget build(BuildContext context) {
    final history = ScoreHistory.history;
    return Scaffold(
      appBar: AppBar(title: const Text("Score History"), backgroundColor: Colors.green[700], foregroundColor: Colors.white),
      body: history.isEmpty
        ? const Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            Icon(Icons.history, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text("No quizzes completed yet!", style: TextStyle(fontSize: 18, color: Colors.grey)),
          ]))
        : ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: history.length,
            itemBuilder: (context, index) {
              final e = history[index];
              final percent = (e.score / e.total * 100).round();
              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  leading: CircleAvatar(
                    backgroundColor: percent >= 70 ? Colors.green : Colors.orange,
                    child: Text("$percent%", style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                  ),
                  title: Text(e.subject, style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text("${e.date.day}/${e.date.month}/${e.date.year}"),
                  trailing: Text("${e.score}/${e.total}", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ),
              );
            },
          ),
    );
  }
}
""")

write("lib/features/gamification/providers/gamification_provider.dart", """
import 'package:flutter_riverpod/flutter_riverpod.dart';

class GamificationState {
  final int points;
  final int streak;
  final int quizzesCompleted;
  GamificationState({this.points = 245, this.streak = 7, this.quizzesCompleted = 0});
  GamificationState copyWith({int? points, int? streak, int? quizzesCompleted}) {
    return GamificationState(
      points: points ?? this.points,
      streak: streak ?? this.streak,
      quizzesCompleted: quizzesCompleted ?? this.quizzesCompleted,
    );
  }
}

class GamificationNotifier extends Notifier<GamificationState> {
  @override
  GamificationState build() => GamificationState();
  void addPoints(int amount) => state = state.copyWith(points: state.points + amount);
  void completeQuiz() => state = state.copyWith(quizzesCompleted: state.quizzesCompleted + 1);
}

final gamificationProvider = NotifierProvider<GamificationNotifier, GamificationState>(GamificationNotifier.new);
""")

write("lib/features/dashboard/presentation/dashboard_screen.dart", """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../gamification/providers/gamification_provider.dart';
import '../../subjects/math/presentation/math_quest_screen.dart';
import '../../subjects/science/presentation/science_quest_screen.dart';
import '../../subjects/tamil/tamil_screen.dart';
import '../../subjects/evs/evs_screen.dart';
import '../../../core/api/ai_tutor_service.dart';
import '../../history/score_history_screen.dart';

class DashboardScreen extends ConsumerWidget {
  final String studentName;
  final String grade;
  const DashboardScreen({super.key, required this.studentName, required this.grade});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final progress = ref.watch(gamificationProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text("IncluPlayAI", style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.green[700],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ScoreHistoryScreen())),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: LinearGradient(colors: [Colors.green[700]!, Colors.green[400]!]),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 30,
                    backgroundColor: Colors.white,
                    child: Text(studentName[0].toUpperCase(), style: TextStyle(fontSize: 24, color: Colors.green[700], fontWeight: FontWeight.bold)),
                  ),
                  const SizedBox(width: 16),
                  Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text("Welcome, \$studentName!", style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white)),
                    Text(grade, style: const TextStyle(color: Colors.white70)),
                  ]),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Row(children: [
              Expanded(child: _statCard("Points", "\${progress.points}", Icons.star, Colors.amber)),
              const SizedBox(width: 12),
              Expanded(child: _statCard("Streak", "\${progress.streak}d", Icons.local_fire_department, Colors.orange)),
              const SizedBox(width: 12),
              Expanded(child: _statCard("Quizzes", "\${progress.quizzesCompleted}", Icons.quiz, Colors.blue)),
            ]),
            const SizedBox(height: 24),
            const Text("Choose Subject", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            _buildCard(context, "Mathematics", "Algebra, Geometry & More", Icons.calculate, Colors.blue,
                () => Navigator.push(context, MaterialPageRoute(builder: (_) => const MathQuestScreen()))),
            _buildCard(context, "Science", "Physics, Chemistry & Biology", Icons.science, Colors.purple,
                () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ScienceQuestScreen()))),
            _buildCard(context, "Tamil", "Language & Literature", Icons.menu_book, Colors.orange,
                () => Navigator.push(context, MaterialPageRoute(builder: (_) => const TamilScreen()))),
            _buildCard(context, "EVS", "Environment & Nature", Icons.eco, Colors.green,
                () => Navigator.push(context, MaterialPageRoute(builder: (_) => const EVSScreen()))),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () => _showAiTutor(context),
              icon: const Icon(Icons.smart_toy),
              label: const Text("Ask AI Tutor (RAG + Semantic Search)", style: TextStyle(fontSize: 16)),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 60),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _statCard(String label, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12), border: Border.all(color: color.withOpacity(0.3))),
      child: Column(children: [
        Icon(icon, color: color, size: 24),
        const SizedBox(height: 4),
        Text(value, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
      ]),
    );
  }

  Widget _buildCard(BuildContext context, String title, String subtitle, IconData icon, Color color, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
          child: Icon(icon, color: color, size: 28),
        ),
        title: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
        subtitle: Text(subtitle, style: TextStyle(color: Colors.grey[600])),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: onTap,
      ),
    );
  }

  void _showAiTutor(BuildContext context) {
    final controller = TextEditingController();
    final aiService = AiTutorService();
    String aiAnswer = "";
    bool isLoading = false;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setModalState) => Padding(
          padding: EdgeInsets.only(bottom: MediaQuery.of(ctx).viewInsets.bottom + 20, left: 20, right: 20, top: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(children: [
                const Icon(Icons.smart_toy, color: Colors.deepPurple),
                const SizedBox(width: 8),
                const Text("AI Tutor", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
              ]),
              const Text("Ask anything from NCERT syllabus", style: TextStyle(color: Colors.grey)),
              const SizedBox(height: 16),
              TextField(
                controller: controller,
                decoration: InputDecoration(
                  hintText: "What is photosynthesis?",
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  prefixIcon: const Icon(Icons.question_answer),
                ),
                maxLines: 2,
              ),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: isLoading ? null : () async {
                  if (controller.text.isEmpty) return;
                  setModalState(() { isLoading = true; aiAnswer = ""; });
                  final answer = await aiService.askQuestion(controller.text);
                  setModalState(() { isLoading = false; aiAnswer = answer; });
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.deepPurple,
                  foregroundColor: Colors.white,
                  minimumSize: const Size(double.infinity, 48),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: isLoading ? const CircularProgressIndicator(color: Colors.white) : const Text("Ask AI"),
              ),
              if (aiAnswer.isNotEmpty) ...[
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(color: Colors.purple[50], borderRadius: BorderRadius.circular(12)),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Text("AI Answer:", style: TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple)),
                    const SizedBox(height: 8),
                    Text(aiAnswer),
                  ]),
                ),
              ],
              const SizedBox(height: 8),
            ],
          ),
        ),
      ),
    );
  }
}
""")

write("lib/features/subjects/math/presentation/math_quest_screen.dart", """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../gamification/providers/gamification_provider.dart';
import '../../../history/score_history_screen.dart';

class MathQuestScreen extends ConsumerStatefulWidget {
  const MathQuestScreen({super.key});
  @override
  ConsumerState<MathQuestScreen> createState() => _MathQuestScreenState();
}

class _MathQuestScreenState extends ConsumerState<MathQuestScreen> {
  int _score = 0;
  int _current = 0;
  bool _finished = false;

  final List<Map<String, dynamic>> _questions = [
    {"q": "What is 12 x 12?", "options": ["124", "144", "132", "148"], "answer": "144"},
    {"q": "Square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"},
    {"q": "25% of 200?", "options": ["25", "40", "50", "75"], "answer": "50"},
    {"q": "3x = 21, x = ?", "options": ["5", "6", "7", "8"], "answer": "7"},
    {"q": "Area of circle radius 7 (pi=22/7)?", "options": ["144", "154", "164", "174"], "answer": "154"},
    {"q": "Value of pi?", "options": ["3.14", "3.41", "3.12", "3.16"], "answer": "3.14"},
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
      ScoreHistory.addScore("Mathematics", _score, _questions.length);
      setState(() => _finished = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_finished) {
      return Scaffold(
        appBar: AppBar(title: const Text("Mathematics"), backgroundColor: Colors.blue, foregroundColor: Colors.white),
        body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Icon(Icons.celebration, size: 80, color: Colors.blue),
          const SizedBox(height: 16),
          Text("Score: \$_score / \${_questions.length}", style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          Text("+\${_score * 10} points earned!", style: const TextStyle(fontSize: 18, color: Colors.green)),
          const SizedBox(height: 24),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("Back to Dashboard")),
        ])),
      );
    }
    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("Math Quest"), backgroundColor: Colors.blue, foregroundColor: Colors.white),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          LinearProgressIndicator(value: (_current + 1) / _questions.length, color: Colors.blue),
          const SizedBox(height: 20),
          Text("Question \${_current + 1} / \${_questions.length}", style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 12),
          Text(q["q"], style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          ...(q["options"] as List<String>).map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: ElevatedButton(
              onPressed: () => _answer(opt),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              child: Text(opt, style: const TextStyle(fontSize: 16)),
            ),
          )),
          Text("Score: \$_score", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }
}
""")

write("lib/features/subjects/science/presentation/science_quest_screen.dart", """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../gamification/providers/gamification_provider.dart';
import '../../../history/score_history_screen.dart';

class ScienceQuestScreen extends ConsumerStatefulWidget {
  const ScienceQuestScreen({super.key});
  @override
  ConsumerState<ScienceQuestScreen> createState() => _ScienceQuestScreenState();
}

class _ScienceQuestScreenState extends ConsumerState<ScienceQuestScreen> {
  int _score = 0;
  int _current = 0;
  bool _finished = false;

  final List<Map<String, dynamic>> _questions = [
    {"q": "What gas do plants absorb during photosynthesis?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"q": "Largest planet?", "options": ["Earth", "Saturn", "Jupiter", "Mars"], "answer": "Jupiter"},
    {"q": "Boiling point of water?", "options": ["50C", "75C", "100C", "120C"], "answer": "100C"},
    {"q": "States of matter?", "options": ["2", "3", "4", "5"], "answer": "3"},
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
    if (_finished) {
      return Scaffold(
        appBar: AppBar(title: const Text("Science"), backgroundColor: Colors.purple, foregroundColor: Colors.white),
        body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Icon(Icons.celebration, size: 80, color: Colors.purple),
          const SizedBox(height: 16),
          Text("Score: \$_score / \${_questions.length}", style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          Text("+\${_score * 10} points earned!", style: const TextStyle(fontSize: 18, color: Colors.green)),
          const SizedBox(height: 24),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("Back to Dashboard")),
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
          const SizedBox(height: 20),
          Text("Question \${_current + 1} / \${_questions.length}", style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 12),
          Text(q["q"], style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          ...(q["options"] as List<String>).map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: ElevatedButton(
              onPressed: () => _answer(opt),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              child: Text(opt, style: const TextStyle(fontSize: 16)),
            ),
          )),
          Text("Score: \$_score", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }
}
""")

write("lib/features/subjects/tamil/tamil_screen.dart", """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../gamification/providers/gamification_provider.dart';
import '../../history/score_history_screen.dart';

class TamilScreen extends ConsumerStatefulWidget {
  const TamilScreen({super.key});
  @override
  ConsumerState<TamilScreen> createState() => _TamilScreenState();
}

class _TamilScreenState extends ConsumerState<TamilScreen> {
  int _score = 0;
  int _current = 0;
  bool _finished = false;

  final List<Map<String, dynamic>> _questions = [
    {"q": "Who wrote Thirukkural?", "options": ["Kambar", "Thiruvalluvar", "Avvaiyar", "Ilango"], "answer": "Thiruvalluvar"},
    {"q": "How many kurals are in Thirukkural?", "options": ["1000", "1330", "1500", "1200"], "answer": "1330"},
    {"q": "Tamil is classified as which type of language?", "options": ["Modern", "Classical", "Medieval", "Ancient"], "answer": "Classical"},
    {"q": "How many letters in Tamil alphabet?", "options": ["216", "247", "230", "260"], "answer": "247"},
    {"q": "Which epic is about Kovalan and Kannagi?", "options": ["Manimekalai", "Silappatikaram", "Kambaramayanam", "Purananuru"], "answer": "Silappatikaram"},
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
      ScoreHistory.addScore("Tamil", _score, _questions.length);
      setState(() => _finished = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_finished) {
      return Scaffold(
        appBar: AppBar(title: const Text("Tamil"), backgroundColor: Colors.orange, foregroundColor: Colors.white),
        body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Icon(Icons.celebration, size: 80, color: Colors.orange),
          const SizedBox(height: 16),
          Text("Score: \$_score / \${_questions.length}", style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          Text("+\${_score * 10} points earned!", style: const TextStyle(fontSize: 18, color: Colors.green)),
          const SizedBox(height: 24),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("Back to Dashboard")),
        ])),
      );
    }
    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("Tamil Quest"), backgroundColor: Colors.orange, foregroundColor: Colors.white),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          LinearProgressIndicator(value: (_current + 1) / _questions.length, color: Colors.orange),
          const SizedBox(height: 20),
          Text("Question \${_current + 1} / \${_questions.length}", style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 12),
          Text(q["q"], style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          ...(q["options"] as List<String>).map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: ElevatedButton(
              onPressed: () => _answer(opt),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              child: Text(opt, style: const TextStyle(fontSize: 16)),
            ),
          )),
          Text("Score: \$_score", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }
}
""")

write("lib/features/subjects/evs/evs_screen.dart", """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
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

  final List<Map<String, dynamic>> _questions = [
    {"q": "Main cause of global warming?", "options": ["Rainfall", "Greenhouse gases", "Wind", "Snow"], "answer": "Greenhouse gases"},
    {"q": "Which layer protects Earth from UV rays?", "options": ["Troposphere", "Stratosphere", "Ozone layer", "Mesosphere"], "answer": "Ozone layer"},
    {"q": "Recycling helps reduce?", "options": ["Sunlight", "Waste", "Water", "Air"], "answer": "Waste"},
    {"q": "Which is a renewable energy source?", "options": ["Coal", "Petroleum", "Solar energy", "Natural gas"], "answer": "Solar energy"},
    {"q": "What is deforestation?", "options": ["Planting trees", "Removing forests", "Watering plants", "Growing crops"], "answer": "Removing forests"},
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
      ScoreHistory.addScore("EVS", _score, _questions.length);
      setState(() => _finished = true);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_finished) {
      return Scaffold(
        appBar: AppBar(title: const Text("EVS"), backgroundColor: Colors.green, foregroundColor: Colors.white),
        body: Center(child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
          const Icon(Icons.celebration, size: 80, color: Colors.green),
          const SizedBox(height: 16),
          Text("Score: \$_score / \${_questions.length}", style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
          Text("+\${_score * 10} points earned!", style: const TextStyle(fontSize: 18, color: Colors.green)),
          const SizedBox(height: 24),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text("Back to Dashboard")),
        ])),
      );
    }
    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("EVS Quest"), backgroundColor: Colors.green, foregroundColor: Colors.white),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          LinearProgressIndicator(value: (_current + 1) / _questions.length, color: Colors.green),
          const SizedBox(height: 20),
          Text("Question \${_current + 1} / \${_questions.length}", style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 12),
          Text(q["q"], style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          ...(q["options"] as List<String>).map((opt) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: ElevatedButton(
              onPressed: () => _answer(opt),
              style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 52), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              child: Text(opt, style: const TextStyle(fontSize: 16)),
            ),
          )),
          Text("Score: \$_score", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }
}
""")

write("lib/core/api/ai_tutor_service.dart", """
import 'dart:convert';
import 'package:http/http.dart' as http;

class AiTutorService {
  static const String baseUrl = "http://127.0.0.1:8000";

  Future<String> askQuestion(String question) async {
    try {
      final response = await http.post(
        Uri.parse('\$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({"question": question}),
      ).timeout(const Duration(seconds: 15));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['answer'] ?? "No answer found.";
      } else {
        return "Server error: \${response.statusCode}";
      }
    } catch (e) {
      return "Cannot connect to backend. Make sure uvicorn is running.";
    }
  }
}
""")

print("\nAll files created successfully!")
print("\nNext steps:")
print("1. cd backend && python data_sample.py")
print("2. cd backend && uvicorn main:app --reload")
print("3. flutter run -d chrome")