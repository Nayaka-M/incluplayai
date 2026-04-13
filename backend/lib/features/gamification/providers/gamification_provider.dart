import 'package:flutter_riverpod/flutter_riverpod.dart';

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
