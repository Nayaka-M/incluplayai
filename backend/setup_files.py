import os

files = {
    "backend/requirements.txt": """fastapi
uvicorn
langchain
langchain-community
langchain-huggingface
langchain-text-splitters
chromadb
sentence-transformers
""",

    "backend/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

app = FastAPI(title="IncluPlayAI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./data", embedding_function=embeddings)

class Query(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "IncluPlayAI Backend Running!"}

@app.post("/ask")
async def ask_question(query: Query):
    try:
        docs = vectorstore.similarity_search(query.question, k=3)
        context = "\\n".join([doc.page_content for doc in docs])
        return {"answer": f"Based on NCERT content:\\n\\n{context}"}
    except Exception as e:
        return {"answer": "Sorry, could not find answer."}
""",

    "backend/data_sample.py": """from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("Creating Vector Database...")

documents = [
    "Photosynthesis is the process by which green plants make their own food using sunlight, carbon dioxide, and water.",
    "Newton's First Law: An object at rest stays at rest unless acted upon by an external force.",
    "Jupiter is the largest planet in our solar system.",
    "Water boils at 100 degree Celsius at sea level.",
    "Matter has three states: Solid, Liquid, and Gas.",
    "Force equals mass times acceleration. This is Newton's Second Law.",
    "The human body has 206 bones in an adult.",
    "Chlorophyll is the green pigment in plants that absorbs sunlight for photosynthesis.",
]

text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
texts = text_splitter.create_documents(documents)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory="./data")

print("Vector Database Created Successfully!")
print(f"Total chunks stored: {len(texts)}")
""",

    "lib/app.dart": """import 'package:flutter/material.dart';
import 'features/dashboard/presentation/dashboard_screen.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IncluPlayAI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green),
      home: const DashboardScreen(),
    );
  }
}
""",

    "lib/main.dart": """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}
""",

    "lib/core/api/ai_tutor_service.dart": """import 'dart:convert';
import 'package:http/http.dart' as http;

class AiTutorService {
  static const String baseUrl = "http://127.0.0.1:8000";

  Future<String> askQuestion(String question) async {
    try {
      final response = await http.post(
        Uri.parse('\$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({"question": question}),
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['answer'] ?? "No answer found.";
      } else {
        return "Server error: \${response.statusCode}";
      }
    } catch (e) {
      return "Cannot connect to backend. Make sure uvicorn is running on port 8000.";
    }
  }
}
""",

    "lib/features/gamification/providers/gamification_provider.dart": """import 'package:flutter_riverpod/flutter_riverpod.dart';

class GamificationState {
  final int points;
  final int streak;
  GamificationState({this.points = 245, this.streak = 7});
  GamificationState copyWith({int? points, int? streak}) {
    return GamificationState(points: points ?? this.points, streak: streak ?? this.streak);
  }
}

class GamificationNotifier extends Notifier<GamificationState> {
  @override
  GamificationState build() => GamificationState();
  void addPoints(int amount) => state = state.copyWith(points: state.points + amount);
}

final gamificationProvider = NotifierProvider<GamificationNotifier, GamificationState>(GamificationNotifier.new);
""",

    "lib/features/subjects/math/presentation/math_quest_screen.dart": """import 'package:flutter/material.dart';
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
          content: Text("Score: \$_score / \${_questions.length}\\n+\${_score * 10} points earned!"),
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
""",

    "lib/features/subjects/science/presentation/science_quest_screen.dart": """import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../gamification/providers/gamification_provider.dart';

class ScienceQuestScreen extends ConsumerStatefulWidget {
  const ScienceQuestScreen({super.key});
  @override
  ConsumerState<ScienceQuestScreen> createState() => _ScienceQuestScreenState();
}

class _ScienceQuestScreenState extends ConsumerState<ScienceQuestScreen> {
  int _score = 0;
  int _current = 0;

  final List<Map<String, dynamic>> _questions = [
    {"q": "What gas do plants absorb during photosynthesis?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"q": "Which is the largest planet?", "options": ["Earth", "Saturn", "Jupiter", "Mars"], "answer": "Jupiter"},
    {"q": "What is the boiling point of water?", "options": ["50°C", "75°C", "100°C", "120°C"], "answer": "100°C"},
    {"q": "How many states of matter are there?", "options": ["2", "3", "4", "5"], "answer": "3"},
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
          content: Text("Score: \$_score / \${_questions.length}\\n+\${_score * 10} points earned!"),
          actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text("OK"))],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final q = _questions[_current];
    return Scaffold(
      appBar: AppBar(title: const Text("Science Quest"), backgroundColor: Colors.purple),
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
""",

    "lib/features/dashboard/presentation/dashboard_screen.dart": """import 'package:flutter/material.dart';
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
""",
}

print("Creating all project files...")
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Created: {path}")

print("\nAll files created successfully!")
print("\nNext steps:")
print("1. Run: flutter pub add flutter_riverpod http")
print("2. Run: cd backend && python data_sample.py")
print("3. Run: cd backend && uvicorn main:app --reload")
print("4. In new terminal: flutter run -d chrome")