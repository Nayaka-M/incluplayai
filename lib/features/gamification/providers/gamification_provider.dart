import 'package:flutter_riverpod/flutter_riverpod.dart';

class GamificationState {
  final int points;
  final int streak;
  final int quizzesCompleted;
  final Map<String, double> subjectProgress;

  GamificationState({
    this.points = 0,
    this.streak = 0,
    this.quizzesCompleted = 0,
    this.subjectProgress = const {
      'Mathematics': 0.0,
      'Science': 0.0,
      'Tamil': 0.0,
      'EVS': 0.0,
    },
  });

  GamificationState copyWith({
    int? points,
    int? streak,
    int? quizzesCompleted,
    Map<String, double>? subjectProgress,
  }) {
    return GamificationState(
      points: points ?? this.points,
      streak: streak ?? this.streak,
      quizzesCompleted: quizzesCompleted ?? this.quizzesCompleted,
      subjectProgress: subjectProgress ?? this.subjectProgress,
    );
  }
}

class GamificationNotifier extends Notifier<GamificationState> {
  @override
  GamificationState build() => GamificationState();

  void addPoints(int amount) =>
      state = state.copyWith(points: state.points + amount);

  void completeQuiz() =>
      state = state.copyWith(quizzesCompleted: state.quizzesCompleted + 1);

  void updateSubjectProgress(String subject, int correct, int total) {
    final updated = Map<String, double>.from(state.subjectProgress);
    updated[subject] = total == 0 ? 0.0 : correct / total;
    state = state.copyWith(subjectProgress: updated);
  }
}

final gamificationProvider =
    NotifierProvider<GamificationNotifier, GamificationState>(
        GamificationNotifier.new);