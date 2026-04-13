import 'package:flutter_riverpod/flutter_riverpod.dart';

class ProfileState {
  final String location;
  final String language;

  const ProfileState({
    this.location = 'Tiruchirappalli',
    this.language = 'English',
  });

  ProfileState copyWith({String? location, String? language}) {
    return ProfileState(
      location: location ?? this.location,
      language: language ?? this.language,
    );
  }
}

class ProfileNotifier extends Notifier<ProfileState> {
  @override
  ProfileState build() => const ProfileState();

  void setLocation(String location) {
    if (location.trim().isNotEmpty) {
      state = state.copyWith(location: location.trim());
    }
  }

  void setLanguage(String language) {
    state = state.copyWith(language: language);
  }
}

final profileProvider = NotifierProvider<ProfileNotifier, ProfileState>(() {
  return ProfileNotifier();
});