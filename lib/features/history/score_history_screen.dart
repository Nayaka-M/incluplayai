
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
