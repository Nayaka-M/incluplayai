import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../gamification/providers/gamification_provider.dart';
import '../../subjects/math/presentation/math_quest_screen.dart';
import '../../subjects/science/presentation/science_quest_screen.dart';
import '../../subjects/tamil/tamil_screen.dart';
import '../../subjects/evs/evs_screen.dart';
import '../../chat/ai_chat_screen.dart';
import '../../history/score_history_screen.dart';
import '../../profile/profile_screen.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  final String studentName;
  final String grade;
  const DashboardScreen({super.key, required this.studentName, required this.grade});
  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeAnim;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 800));
    _fadeAnim = CurvedAnimation(parent: _controller, curve: Curves.easeOut);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final progress = ref.watch(gamificationProvider);
    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F5),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1D9E75),
        elevation: 0,
        title: const Text(
          'IncluPlayAI',
          style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.person, color: Colors.white),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ProfileScreen(
                  studentName: widget.studentName,
                  grade: widget.grade,
                ),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.history, color: Colors.white),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ScoreHistoryScreen()),
            ),
          ),
        ],
      ),
      body: FadeTransition(
        opacity: _fadeAnim,
        child: SingleChildScrollView(
          child: Column(
            children: [
              _buildHeader(progress),
              Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildProgressCard(progress),
                    const SizedBox(height: 20),
                    const Text(
                      'Choose subject',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                    ),
                    const SizedBox(height: 12),
                    _buildSubjectCard(
                      'Mathematics', 'Algebra, geometry & more',
                      Icons.calculate, const Color(0xFF185FA5),
                      progress.subjectProgress['Mathematics'] ?? 0.0,
                      () => Navigator.push(context, _route(const MathQuestScreen())),
                    ),
                    _buildSubjectCard(
                      'Science', 'Physics, chemistry & biology',
                      Icons.science, const Color(0xFF534AB7),
                      progress.subjectProgress['Science'] ?? 0.0,
                      () => Navigator.push(context, _route(const ScienceQuestScreen())),
                    ),
                    _buildSubjectCard(
                      'Tamil', 'Language & literature',
                      Icons.menu_book, const Color(0xFFBA7517),
                      progress.subjectProgress['Tamil'] ?? 0.0,
                      () => Navigator.push(context, _route(const TamilScreen())),
                    ),
                    _buildSubjectCard(
                      'EVS', 'Environment & nature',
                      Icons.eco, const Color(0xFF3B6D11),
                      progress.subjectProgress['EVS'] ?? 0.0,
                      () => Navigator.push(context, _route(const EVSScreen())),
                    ),
                    const SizedBox(height: 16),
                    _buildAiButton(),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader(GamificationState progress) {
    return Container(
      decoration: const BoxDecoration(
        color: Color(0xFF1D9E75),
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(24),
          bottomRight: Radius.circular(24),
        ),
      ),
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 28),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Hello, ${widget.studentName}!',
            style: const TextStyle(
              color: Colors.white, fontSize: 22, fontWeight: FontWeight.w600,
            ),
          ),
          Text(
            widget.grade,
            style: const TextStyle(color: Colors.white70, fontSize: 13),
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              _statChip(progress.points.toString(), 'Points', const Color(0xFF1D9E75)),
              const SizedBox(width: 10),
              _statChip('${progress.streak} days', 'Streak', const Color(0xFFBA7517)),
              const SizedBox(width: 10),
              _statChip(progress.quizzesCompleted.toString(), 'Quizzes', const Color(0xFF185FA5)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _statChip(String value, String label, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 10),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Text(
              value,
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: color),
            ),
            const SizedBox(height: 2),
            Text(label, style: const TextStyle(fontSize: 11, color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildProgressCard(GamificationState progress) {
    final done = progress.subjectProgress.values.where((v) => v >= 1.0).length;
    final total = progress.subjectProgress.length;
    final ratio = total == 0 ? 0.0 : done / total;
    final percent = (ratio * 100).toInt();
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Weekly progress', style: TextStyle(color: Colors.grey, fontSize: 13)),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                done == 0 ? 'No subjects completed yet' : '$done of $total subjects done',
                style: const TextStyle(fontWeight: FontWeight.w500),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                decoration: BoxDecoration(
                  color: const Color(0xFFEAF3DE),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text(
                  '$percent%',
                  style: const TextStyle(
                    fontSize: 12, fontWeight: FontWeight.w500, color: Color(0xFF27500A),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0.0, end: ratio),
            duration: const Duration(milliseconds: 1200),
            curve: Curves.easeOut,
            builder: (context, value, _) => LinearProgressIndicator(
              value: value,
              backgroundColor: Colors.grey.shade200,
              color: const Color(0xFF1D9E75),
              minHeight: 6,
              borderRadius: BorderRadius.circular(3),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSubjectCard(
    String title, String subtitle, IconData icon, Color color,
    double progress, VoidCallback onTap,
  ) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey.shade200),
        ),
        child: Row(
          children: [
            Container(
              width: 44, height: 44,
              decoration: BoxDecoration(
                color: color.withOpacity(0.12),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(icon, color: color, size: 22),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 15)),
                  Text(subtitle, style: const TextStyle(color: Colors.grey, fontSize: 12)),
                  const SizedBox(height: 6),
                  TweenAnimationBuilder<double>(
                    tween: Tween(begin: 0.0, end: progress),
                    duration: const Duration(milliseconds: 1000),
                    curve: Curves.easeOut,
                    builder: (context, value, _) => LinearProgressIndicator(
                      value: value,
                      backgroundColor: Colors.grey.shade200,
                      color: color,
                      minHeight: 4,
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Text(
                '${(progress * 100).toInt()}%',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500, color: color),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAiButton() {
    return GestureDetector(
      onTap: () => Navigator.push(context, _route(const AiChatScreen())),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          color: const Color(0xFF534AB7),
          borderRadius: BorderRadius.circular(16),
        ),
        child: const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.smart_toy, color: Colors.white, size: 20),
            SizedBox(width: 8),
            Text('Chat with AI tutor',
                style: TextStyle(color: Colors.white, fontSize: 15, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }

  PageRouteBuilder _route(Widget page) => PageRouteBuilder(
    pageBuilder: (_, __, ___) => page,
    transitionsBuilder: (_, anim, __, child) => FadeTransition(opacity: anim, child: child),
    transitionDuration: const Duration(milliseconds: 250),
  );
}