import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Token manager with refresh race-condition protection.
/// 
/// This is used by the AuthInterceptor to safely refresh tokens
/// when multiple concurrent requests hit 401.
/// 
/// See docs/architecture/mobile.md §7 for the pattern specification.
class TokenManager {
  final FlutterSecureStorage _storage;
  
  TokenManager({FlutterSecureStorage? storage})
      : _storage = storage ?? const FlutterSecureStorage(
          aOptions: AndroidOptions(encryptedSharedPreferences: true),
          iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
        );

  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';

  /// Get the current access token.
  Future<String?> getAccessToken() async {
    return _storage.read(key: _accessTokenKey);
  }

  /// Get the current refresh token.
  Future<String?> getRefreshToken() async {
    return _storage.read(key: _refreshTokenKey);
  }

  /// Save new tokens after refresh.
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await Future.wait([
      _storage.write(key: _accessTokenKey, value: accessToken),
      _storage.write(key: _refreshTokenKey, value: refreshToken),
    ]);
  }

  /// Clear all tokens on logout.
  Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _refreshTokenKey),
    ]);
  }

  /// Refresh the access token using the refresh token.
  /// 
  /// This method is called by the AuthInterceptor and must be
  /// protected against concurrent calls (Completer pattern).
  /// 
  /// Returns the new access token or null if refresh failed.
  Future<String?> refreshAccessToken() async {
    // TODO: Implement token refresh
    // 1. Get refresh token from storage
    // 2. Call backend /auth/refresh endpoint
    // 3. Save new tokens
    // 4. Return new access token
    // 5. If refresh fails, clear tokens and return null
    
    final refreshToken = await getRefreshToken();
    if (refreshToken == null) return null;
    
    // Placeholder - implement actual refresh logic
    throw UnimplementedError(
      'Token refresh must be implemented with your backend endpoint. '
      'See docs/architecture/mobile.md §7 for the pattern.',
    );
  }
}
