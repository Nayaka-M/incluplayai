import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ChatWidget extends StatefulWidget {
  const ChatWidget({super.key});
  @override
  State<ChatWidget> createState() => _ChatWidgetState();
}

class _ChatWidgetState extends State<ChatWidget> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;

  Future<void> _sendMessage() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add({"role": "user", "text": text});
      _isLoading = true;
    });
    _controller.clear();

    try {
      // 127.0.0.1:5000 is the correct local address for your Python server
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'query': text}),
      );

      final Map<String, dynamic> data = jsonDecode(response.body);
      
      setState(() {
        // This 'response' key matches the Python code exactly
        _messages.add({
          "role": "ai", 
          "text": data['response']?.toString() ?? "Error: Empty response"
        });
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _messages.add({"role": "ai", "text": "Connection failed. Is Python running?"});
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            itemCount: _messages.length,
            itemBuilder: (context, i) => ListTile(
              title: Text(_messages[i]["text"] ?? ""),
              tileColor: _messages[i]["role"] == "user" ? Colors.blue[50] : Colors.grey[100],
            ),
          ),
        ),
        if (_isLoading) LinearProgressIndicator(),
        TextField(
          controller: _controller,
          onSubmitted: (_) => _sendMessage(),
          decoration: InputDecoration(
            hintText: "Ask a math question...",
            suffixIcon: IconButton(icon: Icon(Icons.send), onPressed: _sendMessage),
          ),
        ),
      ],
    );
  }
}