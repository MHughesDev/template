import 'package:fpdart/fpdart.dart';

import '../error/failures.dart';

/// API result type using Either from fpdart.
/// 
/// Left = Failure, Right = Success data.
/// 
/// Usage:
/// ```dart
/// Future<ApiResult<User>> getUser(String id) async {
///   try {
///     final response = await dio.get('/users/$id');
///     return Right(User.fromJson(response.data));
///   } on DioException catch (e) {
///     return Left(_mapDioError(e));
///   }
/// }
/// ```
typedef ApiResult<T> = Either<Failure, T>;

/// Extension helpers for ApiResult.
extension ApiResultX<T> on ApiResult<T> {
  /// Get success value or null.
  T? getOrNull() => fold((l) => null, (r) => r);

  /// Get failure or null.
  Failure? failureOrNull() => fold((l) => l, (r) => null);

  /// Execute side effect on success.
  ApiResult<T> onSuccess(void Function(T data) action) {
    return map((r) {
      action(r);
      return r;
    });
  }

  /// Execute side effect on failure.
  ApiResult<T> onFailure(void Function(Failure failure) action) {
    return mapLeft((l) {
      action(l);
      return l;
    });
  }
}

/// Map DioException to domain Failure.
/// 
/// This should be extended as the app grows to handle specific error codes
/// from the backend's error taxonomy.
Failure mapDioError(dynamic error) {
  // Placeholder implementation
  // Full implementation deferred to feature work
  return UnknownFailure(message: error.toString());
}
