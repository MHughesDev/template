import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Secure token storage using platform Keychain (iOS) and Keystore (Android).
/// 
/// This is the **only** sanctioned storage for auth tokens.
/// Never use SharedPreferences, hive, or plain files for tokens.
/// 
/// See docs/architecture/mobile.md §7 for the auth and token storage specification.
class SecureStorage {
  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(
      encryptedSharedPreferences: true,
    ),
    iOptions: IOSOptions(
      accessibility: KeychainAccessibility.first_unlock,
    ),
  );

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';
  static const _tokenExpiresAtKey = 'token_expires_at';

  /// Save access token.
  Future<void> saveAccessToken(String token) async {
    await _storage.write(key: _accessTokenKey, value: token);
  }

  /// Save refresh token.
  Future<void> saveRefreshToken(String token) async {
    await _storage.write(key: _refreshTokenKey, value: token);
  }

  /// Save both tokens with expiration.
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
    required DateTime expiresAt,
  }) async {
    await Future.wait([
      _storage.write(key: _accessTokenKey, value: accessToken),
      _storage.write(key: _refreshTokenKey, value: refreshToken),
      _storage.write(
        key: _tokenExpiresAtKey,
        value: expiresAt.toIso8601String(),
      ),
    ]);
  }

  /// Get access token.
  Future<String?> getAccessToken() async {
    return _storage.read(key: _accessTokenKey);
  }

  /// Get refresh token.
  Future<String?> getRefreshToken() async {
    return _storage.read(key: _refreshTokenKey);
  }

  /// Get token expiration.
  Future<DateTime?> getTokenExpiration() async {
    final value = await _storage.read(key: _tokenExpiresAtKey);
    if (value == null) return null;
    return DateTime.tryParse(value);
  }

  /// Check if token is expired (with 60-second buffer).
  Future<bool> isTokenExpired() async {
    final expiration = await getTokenExpiration();
    if (expiration == null) return true;
    return DateTime.now().isAfter(expiration.subtract(const Duration(seconds: 60)));
  }

  /// Clear all tokens (logout).
  Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _refreshTokenKey),
      _storage.delete(key: _tokenExpiresAtKey),
    ]);
  }

  /// Check if tokens exist.
  Future<bool> hasTokens() async {
    final access = await getAccessToken();
    return access != null && access.isNotEmpty;
  }

  // Private constructor for singleton pattern
  SecureStorage._();
  
  static final SecureStorage _instance = SecureStorage._();
  
  /// Singleton instance.
  factory SecureStorage() => _instance;
}
