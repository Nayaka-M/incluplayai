(
echo import 'package:flutter_vibrate/flutter_vibrate.dart';
echo.
echo class HapticHelper {
echo   static void success() => Vibrate.feedback(FeedbackType.success);
echo   static void error() => Vibrate.feedback(FeedbackType.error);
echo   static void click() => Vibrate.feedback(FeedbackType.light);
echo } 
) > lib\core\utils\haptic_helper.dart