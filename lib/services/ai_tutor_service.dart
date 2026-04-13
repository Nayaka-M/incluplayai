import 'dart:convert';
import 'package:http/http.dart' as http;

class AiTutorService {
  static const String baseUrl = "http://127.0.0.1:8000";

  static Future<String> askQuestion(String question) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({"question": question}),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['answer'] ?? "Sorry, I couldn't generate a response.";
      } else {
        return "Backend is running but returned an error.";
      }
    } catch (e) {
      return "Cannot connect to AI Backend.\nMake sure backend is running on port 8000.";
    }
  }
}