import 'dart:convert';
import 'package:http/http.dart' as http;

class AiTutorService {
  static const String baseUrl = "http://127.0.0.1:8000";

  Future<String> askQuestion(String question) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl + "/ask"),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({"question": question}),
      ).timeout(const Duration(seconds: 20));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['answer'] ?? "No answer found.";
      }
      return "Server error: " + response.statusCode.toString();
    } catch (e) {
      return "Error: " + e.toString();
    }
  }

  Future<List<Map<String, dynamic>>> generateQuiz(String subject, String grade) async {
    try {
      final response = await http.post(
        Uri.parse(baseUrl + "/quiz"),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({"subject": subject, "grade": grade}),
      ).timeout(const Duration(seconds: 30));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final questions = data['questions'] as List;
        return questions.map((q) => Map<String, dynamic>.from(q)).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }
}