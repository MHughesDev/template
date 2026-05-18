import 'package:dio/dio.dart';

import '../config/app_config.dart';

/// Dio HTTP client with interceptors for auth, retry, logging, and error handling.
/// 
/// This client is the only sanctioned way to call the FastAPI backend.
/// Never use raw http calls or separate Dio instances in features.
class DioClient {
  final Dio _dio;

  DioClient({required AppConfig config}) : _dio = _createDio(config);

  Dio get dio => _dio;

  static Dio _createDio(AppConfig config) {
    final dio = Dio(
      BaseOptions(
        baseUrl: config.apiUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      ),
    );

    // Add interceptors in order
    dio.interceptors.addAll([
      _LoggingInterceptor(logLevel: config.logLevel),
      // AuthInterceptor will be added via provider that has access to secure storage
    ]);

    return dio;
  }
}

/// Logging interceptor that respects the configured log level.
class _LoggingInterceptor extends Interceptor {
  final String logLevel;

  _LoggingInterceptor({required this.logLevel});

  bool get _shouldLog => logLevel == 'debug' || logLevel == 'info';

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (_shouldLog) {
      print('[HTTP REQUEST] ${options.method} ${options.uri}');
      if (logLevel == 'debug') {
        print('Headers: ${options.headers}');
        print('Body: ${options.data}');
      }
    }
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    if (_shouldLog) {
      print('[HTTP RESPONSE] ${response.statusCode} ${response.requestOptions.uri}');
      if (logLevel == 'debug') {
        print('Body: ${response.data}');
      }
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    print('[HTTP ERROR] ${err.response?.statusCode ?? 'NO_STATUS'} ${err.requestOptions.uri}');
    print('Error: ${err.message}');
    handler.next(err);
  }
}

/// Placeholder for the auth interceptor with token refresh.
/// 
/// This will be implemented with flutter_secure_storage for token management
/// and proper race-condition protection using Completer pattern.
/// 
/// The full implementation should:
/// 1. Read access token from secure storage and add to Authorization header
/// 2. On 401, queue requests while refreshing token
/// 3. Use refresh token to get new access token
/// 4. If refresh fails, clear tokens and force logout
/// 5. Retry queued requests with new token
class AuthInterceptor extends QueuedInterceptor {
  // Implementation deferred to feature-specific work
  // See docs/architecture/mobile.md §7 for the pattern specification
}
