/// Base failure class for domain errors.
/// 
/// All failures are pure Dart objects with no Flutter dependencies.
/// This lives in the domain layer and is known to all layers.
abstract class Failure {
  final String message;
  final String? code;
  final StackTrace? stackTrace;

  const Failure({
    required this.message,
    this.code,
    this.stackTrace,
  });

  @override
  String toString() => 'Failure(message: $message, code: $code)';
}

/// Network connectivity failure.
class NetworkFailure extends Failure {
  const NetworkFailure({
    super.message = 'No internet connection',
    super.code = 'NETWORK_ERROR',
  });
}

/// Authentication/authorization failure.
class AuthFailure extends Failure {
  final bool shouldLogout;

  const AuthFailure({
    super.message = 'Authentication failed',
    super.code = 'AUTH_ERROR',
    this.shouldLogout = false,
  });
}

/// Server-side validation failure.
class ValidationFailure extends Failure {
  final Map<String, List<String>>? fieldErrors;

  const ValidationFailure({
    super.message = 'Validation failed',
    super.code = 'VALIDATION_ERROR',
    this.fieldErrors,
  });
}

/// Server error (5xx).
class ServerFailure extends Failure {
  final int? statusCode;

  const ServerFailure({
    super.message = 'Server error',
    super.code = 'SERVER_ERROR',
    this.statusCode,
  });
}

/// Not found (404).
class NotFoundFailure extends Failure {
  const NotFoundFailure({
    super.message = 'Resource not found',
    super.code = 'NOT_FOUND',
  });
}

/// Timeout failure.
class TimeoutFailure extends Failure {
  const TimeoutFailure({
    super.message = 'Request timed out',
    super.code = 'TIMEOUT_ERROR',
  });
}

/// Unknown/unexpected failure.
class UnknownFailure extends Failure {
  const UnknownFailure({
    required super.message,
    super.code = 'UNKNOWN_ERROR',
  });
}

/// Cache/local storage failure.
class CacheFailure extends Failure {
  const CacheFailure({
    super.message = 'Cache error',
    super.code = 'CACHE_ERROR',
  });
}
