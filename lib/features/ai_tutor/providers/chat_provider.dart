import 'package:flutter_riverpod/flutter_riverpod.dart';

class ChatMessage {
  final String text;
  final bool isUser;
  ChatMessage(this.text, this.isUser);
}

class ChatNotifier extends StateNotifier<List<ChatMessage>> {
  ChatNotifier() : super([ChatMessage("Hi Nayaka! I'm your AI Tutor. Need a hint for this math problem?", false)]);

  void sendMessage(String text) async {
    state = [...state, ChatMessage(text, true)];
    
    // TODO: Connect to your Python backend (http://localhost:5000/ask)
    // For now, let's mock a response
    await Future.delayed(const Duration(seconds: 1));
    state = [...state, ChatMessage("That's a great question! Remember to add the numbers in the units place first.", false)];
  }
}

final chatProvider = StateNotifierProvider<ChatNotifier, List<ChatMessage>>((ref) => ChatNotifier());