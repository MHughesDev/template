import 'dart:convert';

import 'package:flutter/services.dart';

/// Application configuration loaded at startup.
/// 
/// Configuration is compile-time injected via --dart-define-from-file.
/// Never use runtime environment variable lookups in Flutter.
class AppConfig {
  final String apiBaseUrl;
  final String logLevel;
  final bool analyticsEnabled;
  final bool biometricUnlock;
  final String apiVersion;

  const AppConfig({
    required this.apiBaseUrl,
    required this.logLevel,
    required this.analyticsEnabled,
    required this.biometricUnlock,
    required this.apiVersion,
  });

  /// Load configuration from compile-time defines.
  /// 
  /// In development, this reads from config/dev.json.
  /// In production, values are injected via --dart-define-from-file.
  static Future<AppConfig> load() async {
    const baseUrl = String.fromEnvironment(
      'API_BASE_URL',
      defaultValue: 'http://localhost:8000',
    );
    const logLevel = String.fromEnvironment(
      'LOG_LEVEL',
      defaultValue: 'info',
    );
    const analyticsEnabled = bool.fromEnvironment(
      'ANALYTICS_ENABLED',
      defaultValue: false,
    );
    const biometricUnlock = bool.fromEnvironment(
      'BIOMETRIC_UNLOCK',
      defaultValue: false,
    );
    const apiVersion = String.fromEnvironment(
      'API_VERSION',
      defaultValue: 'v1',
    );

    return AppConfig(
      apiBaseUrl: baseUrl,
      logLevel: logLevel,
      analyticsEnabled: analyticsEnabled,
      biometricUnlock: biometricUnlock,
      apiVersion: apiVersion,
    );
  }

  /// Full API base URL with version.
  String get apiUrl => '$apiBaseUrl/api/$apiVersion';

  Map<String, dynamic> toJson() => {
    'apiBaseUrl': apiBaseUrl,
    'logLevel': logLevel,
    'analyticsEnabled': analyticsEnabled,
    'biometricUnlock': biometricUnlock,
    'apiVersion': apiVersion,
  };

  @override
  String toString() => 'AppConfig(${jsonEncode(toJson())})';
}
