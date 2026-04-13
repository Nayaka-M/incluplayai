import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../gamification/providers/gamification_provider.dart';
import '../../subjects/math/presentation/math_quest_screen.dart';
import '../../subjects/science/presentation/science_quest_screen.dart';
import '../../../core/api/ai_tutor_service.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final progress = ref.watch(gamificationProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text("IncluPlayAI"),
        backgroundColor: Colors.green[700],
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("Welcome, Nayaka!", style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
            Text("Tiruchirappalli - Grade 8", style: TextStyle(fontSize: 16, color: Colors.grey[600])),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(color: Colors.green[50], borderRadius: BorderRadius.circular(16)),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Column(children: [const Text("Points"), Text("\${progress.points}", style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold))]),
                  Column(children: [const Text("Streak"), Text("\${progress.streak} days", style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.orange))]),
                ],
              ),
            ),
            const SizedBox(height: 32),
            const Text("Choose Subject", style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildCard(context, "Mathematics", Colors.blue, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const MathQuestScreen()))),
            _buildCard(context, "Science", Colors.purple, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ScienceQuestScreen()))),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => _showAiTutor(context),
              icon: const Icon(Icons.smart_toy),
              label: const Text("Ask AI Tutor (RAG)"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                foregroundColor: Colors.white,
                minimumSize: const Size(double.infinity, 56),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCard(BuildContext context, String title, Color color, VoidCallback onTap) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: CircleAvatar(backgroundColor: color.withOpacity(0.2), child: Icon(Icons.book, color: color)),
        title: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
        trailing: const Icon(Icons.arrow_forward_ios),
        onTap: onTap,
      ),
    );
  }

  void _showAiTutor(BuildContext context) {
    final controller = TextEditingController();
    final aiService = AiTutorService();
    String aiAnswer = "";

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setModalState) => Padding(
          padding: EdgeInsets.only(bottom: MediaQuery.of(ctx).viewInsets.bottom + 20, left: 20, right: 20, top: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text("AI Tutor (Semantic Search + RAG)", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              TextField(controller: controller, decoration: const InputDecoration(hintText: "What is photosynthesis?", border: OutlineInputBorder()), maxLines: 2),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: () async {
                  if (controller.text.isEmpty) return;
                  setModalState(() => aiAnswer = "Thinking...");
                  final answer = await aiService.askQuestion(controller.text);
                  setModalState(() => aiAnswer = answer);
                },
                style: ElevatedButton.styleFrom(minimumSize: const Size(double.infinity, 48)),
                child: const Text("Ask AI"),
              ),
              if (aiAnswer.isNotEmpty) ...[
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(color: Colors.purple[50], borderRadius: BorderRadius.circular(8)),
                  child: Text(aiAnswer),
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
