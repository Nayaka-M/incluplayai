import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Use 10.0.2.2 for Android Emulator, or 127.0.0.1 for Chrome/iOS
  static const String baseUrl = 'http://127.0.0.1:5000';

  static Future<String> askTutor(String query) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'query': query}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['answer'] ?? "The tutor is thinking...";
      } else {
        return "Error: ${response.statusCode}. Make sure the backend is running!";
      }
    } catch (e) {
      return "Connection failed. Did you start the Python server?";
    }
  }
}