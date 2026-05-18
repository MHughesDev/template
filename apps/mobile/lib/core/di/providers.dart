import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';
import '../network/dio_client.dart';
import '../routing/app_router.dart';
import '../theme/app_theme.dart';

/// App configuration provider.
/// 
/// Overridden at startup with loaded config in main.dart.
final appConfigProvider = Provider<AppConfig>((ref) {
  throw UnimplementedError('AppConfig must be overridden at startup');
});

/// Theme mode provider.
/// 
/// Controls light/dark/system theme selection.
final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.system);

/// API client provider.
/// 
/// Provides a configured Dio instance with auth interceptors.
final apiClientProvider = Provider<DioClient>((ref) {
  final config = ref.watch(appConfigProvider);
  return DioClient(config: config);
});

/// App router provider.
/// 
/// Provides the go_router configuration.
final appRouterProvider = Provider<AppRouter>((ref) {
  return AppRouter();
});

/// Logger provider (placeholder - replace with concrete implementation).
/// 
/// Provide logging based on config.logLevel.
final loggerProvider = Provider<Logger>((ref) {
  return Logger();
});

/// Placeholder logger class.
/// 
/// Replace with actual logger implementation (e.g., Logger package or analytics service).
class Logger {
  void debug(String message) => print('[DEBUG] $message');
  void info(String message) => print('[INFO] $message');
  void warning(String message) => print('[WARN] $message');
  void error(String message, [Object? error, StackTrace? stackTrace]) =>
      print('[ERROR] $message ${error ?? ''} ${stackTrace ?? ''}');
}
