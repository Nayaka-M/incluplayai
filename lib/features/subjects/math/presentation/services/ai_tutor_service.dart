import 'dart:convert';
import 'package:http/http.dart' as http;

class AiTutorService {
  // Matches the Uvicorn port 8000
  final String _baseUrl = 'http://127.0.0.1:8000/ask';

  Future<String> askQuestion(String message) async {
    try {
      final response = await http.post(
        Uri.parse(_baseUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'query': message}),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = jsonDecode(response.body);
        return data['response']?.toString() ?? "Empty response from AI.";
      } else {
        return "Server error: ${response.statusCode}";
      }
    } catch (e) {
      return "Connection failed. Make sure Python is running on port 8000.";
    }
  }
}