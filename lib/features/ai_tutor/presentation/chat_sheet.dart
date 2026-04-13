import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatSheet extends StatefulWidget {
  const ChatSheet({super.key});

  @override
  State<ChatSheet> createState() => _ChatSheetState();
}

class _ChatSheetState extends State<ChatSheet> {
  final List<Map<String, dynamic>> _messages = [];
  final TextEditingController _controller = TextEditingController();
  bool _isTyping = false;

  Future<void> _sendMessage(String text) async {
    setState(() {
      _messages.add({"text": text, "isUser": true, "subject": "USER"});
      _isTyping = true;
    });

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': text}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _messages.add({
            "text": data['reply'],
            "isUser": false,
            "subject": data['subject']
          });
        });
      }
    } catch (e) {
      setState(() {
        _messages.add({
          "text": "Check if Python backend is running!",
          "isUser": false,
          "subject": "ERROR"
        });
      });
    } finally {
      setState(() => _isTyping = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.8,
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          Text("IncluPlay AI Tutor", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, i) {
                final m = _messages[i];
                return ListTile(
                  title: Align(
                    alignment: m['isUser'] ? Alignment.centerRight : Alignment.centerLeft,
                    child: Column(
                      crossAxisAlignment: m['isUser'] ? CrossAxisAlignment.end : CrossAxisAlignment.start,
                      children: [
                        Text(m['subject'], style: TextStyle(fontSize: 10, color: Colors.grey)),
                        Container(
                          padding: EdgeInsets.all(10),
                          decoration: BoxDecoration(
                            color: m['isUser'] ? Colors.blue[100] : Colors.green[100],
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Text(m['text']),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isTyping) LinearProgressIndicator(),
          TextField(
            controller: _controller,
            onSubmitted: (val) {
              _sendMessage(val);
              _controller.clear();
            },
            decoration: InputDecoration(hintText: "Ask a question..."),
          ),
        ],
      ),
    );
  }
}