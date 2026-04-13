import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../gamification/providers/gamification_provider.dart';
import '../history/score_history_screen.dart';
import '../auth/login_screen.dart';
import '../profile/profile_provider.dart';

class ProfileScreen extends ConsumerWidget {
  final String studentName;
  final String grade;
  const ProfileScreen({super.key, required this.studentName, required this.grade});

  static const Map<String, Map<String, String>> _translations = {
    "English": {
      "account": "Account",
      "settings": "Settings",
      "progress": "Progress",
      "about": "About",
      "name": "Name",
      "grade": "Grade",
      "location": "Location",
      "language": "Language",
      "points": "Total points",
      "streak": "Current streak",
      "days": "days",
      "quizzes": "Quizzes completed",
      "history": "Score history",
      "version": "App version",
      "built": "Built with",
      "syllabus": "Syllabus",
      "logout": "Log out",
      "student": "NCERT Student",
      "weekly": "Weekly progress",
      "of": "of",
      "subjects_done": "subjects done",
      "no_quizzes": "No quizzes completed yet",
    },
    "Tamil": {
      "account": "கணக்கு",
      "settings": "அமைப்புகள்",
      "progress": "முன்னேற்றம்",
      "about": "பற்றி",
      "name": "பெயர்",
      "grade": "வகுப்பு",
      "location": "இடம்",
      "language": "மொழி",
      "points": "மொத்த புள்ளிகள்",
      "streak": "தொடர்",
      "days": "நாட்கள்",
      "quizzes": "முடிந்த வினாடி வினா",
      "history": "மதிப்பெண் வரலாறு",
      "version": "பதிப்பு",
      "built": "உருவாக்கியது",
      "syllabus": "பாடத்திட்டம்",
      "logout": "வெளியேறு",
      "student": "NCERT மாணவர்",
      "weekly": "வாராந்திர முன்னேற்றம்",
      "of": "/",
      "subjects_done": "பாடங்கள் முடிந்தன",
      "no_quizzes": "இன்னும் வினாடி வினா இல்லை",
    },
    "Hindi": {
      "account": "खाता",
      "settings": "सेटिंग्स",
      "progress": "प्रगति",
      "about": "के बारे में",
      "name": "नाम",
      "grade": "कक्षा",
      "location": "स्थान",
      "language": "भाषा",
      "points": "कुल अंक",
      "streak": "स्ट्रीक",
      "days": "दिन",
      "quizzes": "पूर्ण क्विज़",
      "history": "स्कोर इतिहास",
      "version": "संस्करण",
      "built": "बनाया गया",
      "syllabus": "पाठ्यक्रम",
      "logout": "लॉग आउट",
      "student": "NCERT छात्र",
      "weekly": "साप्ताहिक प्रगति",
      "of": "/",
      "subjects_done": "विषय पूर्ण",
      "no_quizzes": "अभी तक कोई क्विज़ नहीं",
    },
  };

  String t(String key, String language) =>
      _translations[language]?[key] ?? key;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final progress = ref.watch(gamificationProvider);
    final profile = ref.watch(profileProvider);
    final lang = profile.language;

    final subjectsDone = progress.quizzesCompleted.clamp(0, 4);
    final progressRatio = subjectsDone / 4.0;

    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F5),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1D9E75),
        foregroundColor: Colors.white,
        elevation: 0,
        title: Text(t("account", lang),
            style: const TextStyle(color: Colors.white)),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            _buildHeader(profile, lang),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  _buildStatsRow(progress, lang),
                  const SizedBox(height: 20),
                  _buildProgressCard(subjectsDone, progressRatio, lang),
                  const SizedBox(height: 20),
                  _buildSection(t("account", lang), [
                    _buildTile(Icons.person, t("name", lang), studentName, Colors.blue),
                    _buildTile(Icons.school, t("grade", lang), grade, Colors.purple),
                    _buildEditableTile(
                      Icons.location_on,
                      t("location", lang),
                      profile.location,
                      Colors.orange,
                      () => _editLocation(context, ref, profile.location, lang),
                    ),
                  ]),
                  const SizedBox(height: 16),
                  _buildSection(t("settings", lang), [
                    _buildDropdownTile(
                        Icons.language, t("language", lang), Colors.teal, lang, ref),
                  ]),
                  const SizedBox(height: 16),
                  _buildSection(t("progress", lang), [
                    _buildTile(Icons.star, t("points", lang),
                        progress.points.toString(), Colors.amber),
                    _buildTile(Icons.local_fire_department, t("streak", lang),
                        "${progress.streak} ${t('days', lang)}", Colors.orange),
                    _buildTile(Icons.quiz, t("quizzes", lang),
                        progress.quizzesCompleted.toString(), Colors.blue),
                    _buildNavTile(Icons.history, t("history", lang), Colors.purple,
                        () => Navigator.push(context,
                            MaterialPageRoute(builder: (_) => const ScoreHistoryScreen()))),
                  ]),
                  const SizedBox(height: 16),
                  _buildSection(t("about", lang), [
                    _buildTile(Icons.info, t("version", lang), "1.0.0", Colors.grey),
                    _buildTile(Icons.code, t("built", lang), "Flutter + Groq AI", Colors.teal),
                    _buildTile(Icons.book, t("syllabus", lang), "NCERT Grades 6-10", Colors.green),
                  ]),
                  const SizedBox(height: 16),
                  _buildLogoutButton(context, lang),
                  const SizedBox(height: 24),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _editLocation(BuildContext context, WidgetRef ref, String current, String lang) {
    final controller = TextEditingController(text: current);
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text(t("location", lang)),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: InputDecoration(
            hintText: "Enter your city",
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF1D9E75)),
            onPressed: () {
              ref.read(profileProvider.notifier).setLocation(controller.text);
              Navigator.pop(context);
            },
            child: const Text("Save", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader(ProfileState profile, String lang) {
    return Container(
      decoration: const BoxDecoration(
        color: Color(0xFF1D9E75),
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(24),
          bottomRight: Radius.circular(24),
        ),
      ),
      padding: const EdgeInsets.fromLTRB(20, 24, 20, 28),
      child: Column(
        children: [
          CircleAvatar(
            radius: 40,
            backgroundColor: Colors.white,
            child: Text(
              studentName[0].toUpperCase(),
              style: const TextStyle(
                  fontSize: 36, fontWeight: FontWeight.bold, color: Color(0xFF1D9E75)),
            ),
          ),
          const SizedBox(height: 12),
          Text(studentName,
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
          Text(grade, style: const TextStyle(fontSize: 14, color: Colors.white70)),
          const SizedBox(height: 4),
          Text(profile.location, style: const TextStyle(fontSize: 12, color: Colors.white60)),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(20)),
            child: Text(t("student", lang), style: const TextStyle(color: Colors.white, fontSize: 13)),
          ),
        ],
      ),
    );
  }

  Widget _buildStatsRow(GamificationState progress, String lang) {
    return Row(
      children: [
        _statBox(progress.points.toString(), t("points", lang), const Color(0xFF1D9E75)),
        const SizedBox(width: 10),
        _statBox("${progress.streak}", t("streak", lang), const Color(0xFFBA7517)),
        const SizedBox(width: 10),
        _statBox(progress.quizzesCompleted.toString(), t("quizzes", lang), const Color(0xFF185FA5)),
      ],
    );
  }

  Widget _statBox(String value, String label, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.grey.shade200),
        ),
        child: Column(
          children: [
            Text(value, style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: color)),
            const SizedBox(height: 2),
            Text(label, textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 10, color: Colors.grey)),
          ],
        ),
      ),
    );
  }

  Widget _buildProgressCard(int subjectsDone, double progressRatio, String lang) {
    final percent = (progressRatio * 100).toInt();
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
          Text(t("weekly", lang), style: const TextStyle(color: Colors.grey, fontSize: 13)),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                subjectsDone == 0
                    ? t("no_quizzes", lang)
                    : "$subjectsDone ${t('of', lang)} 4 ${t('subjects_done', lang)}",
                style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 13),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                decoration: BoxDecoration(
                  color: const Color(0xFFEAF3DE),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Text("$percent%",
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500,
                        color: Color(0xFF27500A))),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ClipRRect(
            borderRadius: BorderRadius.circular(3),
            child: LinearProgressIndicator(
              value: progressRatio,
              backgroundColor: Colors.grey.shade200,
              color: const Color(0xFF1D9E75),
              minHeight: 6,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSection(String title, List<Widget> children) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 4, bottom: 8),
          child: Text(title,
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.grey)),
        ),
        Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.grey.shade200),
          ),
          child: Column(children: children),
        ),
      ],
    );
  }

  Widget _buildTile(IconData icon, String label, String value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
                color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
            child: Icon(icon, color: color, size: 18),
          ),
          const SizedBox(width: 12),
          Text(label, style: const TextStyle(fontSize: 15)),
          const Spacer(),
          Text(value, style: const TextStyle(fontSize: 14, color: Colors.grey)),
        ],
      ),
    );
  }

  Widget _buildEditableTile(IconData icon, String label, String value,
      Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                  color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
              child: Icon(icon, color: color, size: 18),
            ),
            const SizedBox(width: 12),
            Text(label, style: const TextStyle(fontSize: 15)),
            const Spacer(),
            Text(value, style: const TextStyle(fontSize: 14, color: Colors.grey)),
            const SizedBox(width: 6),
            const Icon(Icons.edit, size: 14, color: Colors.grey),
          ],
        ),
      ),
    );
  }

  Widget _buildNavTile(IconData icon, String label, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                  color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
              child: Icon(icon, color: color, size: 18),
            ),
            const SizedBox(width: 12),
            Text(label, style: const TextStyle(fontSize: 15)),
            const Spacer(),
            const Icon(Icons.arrow_forward_ios, size: 14, color: Colors.grey),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdownTile(IconData icon, String label, Color color,
      String currentLang, WidgetRef ref) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
                color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
            child: Icon(icon, color: color, size: 18),
          ),
          const SizedBox(width: 12),
          Text(label, style: const TextStyle(fontSize: 15)),
          const Spacer(),
          DropdownButton<String>(
            value: currentLang,
            underline: const SizedBox(),
            style: const TextStyle(fontSize: 14, color: Colors.grey),
            items: ["English", "Tamil", "Hindi"]
                .map((l) => DropdownMenuItem(value: l, child: Text(l)))
                .toList(),
            onChanged: (v) {
              if (v != null) ref.read(profileProvider.notifier).setLanguage(v);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildLogoutButton(BuildContext context, String lang) {
    return GestureDetector(
      onTap: () => Navigator.pushAndRemoveUntil(
        context,
        MaterialPageRoute(builder: (_) => const LoginScreen()),
        (route) => false,
      ),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          color: Colors.red.shade50,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.red.shade200),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.logout, color: Colors.red, size: 20),
            const SizedBox(width: 8),
            Text(t("logout", lang),
                style: const TextStyle(
                    color: Colors.red, fontSize: 15, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }
}