import 'dart:convert';
import 'package:http/http.dart' as http;

class AiTutorService {
  static const String baseUrl = "https://incluplayai-backend.onrender.com";

  Future<String> askQuestion(String question) async {
    try {
      final url = baseUrl + "/ask";
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({"question": question}),
      ).timeout(const Duration(seconds: 20));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['answer'] ?? "No answer found.";
      } else {
        return "Server error: " + response.statusCode.toString();
      }
    } catch (e) {
      return "Error: " + e.toString();
    }
  }
}