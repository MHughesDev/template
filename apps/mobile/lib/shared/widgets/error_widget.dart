import 'package:flutter/material.dart';

import '../../core/error/failures.dart';

/// Standardized error widget used across the app.
/// 
/// Provides consistent error UI with retry action.
class AppErrorWidget extends StatelessWidget {
  final Failure failure;
  final VoidCallback? onRetry;
  final String? customMessage;

  const AppErrorWidget({
    super.key,
    required this.failure,
    this.onRetry,
    this.customMessage,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final message = customMessage ?? _getDisplayMessage();

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              _getIcon(),
              size: 64,
              color: theme.colorScheme.error,
            ),
            const SizedBox(height: 16),
            Text(
              _getTitle(),
              style: theme.textTheme.titleMedium?.copyWith(
                color: theme.colorScheme.onSurface,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            Text(
              message,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh),
                label: const Text('Try Again'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  String _getTitle() {
    if (failure is NetworkFailure) return 'No Connection';
    if (failure is AuthFailure) return 'Authentication Error';
    if (failure is NotFoundFailure) return 'Not Found';
    if (failure is ServerFailure) return 'Server Error';
    if (failure is ValidationFailure) return 'Validation Error';
    return 'Something Went Wrong';
  }

  String _getDisplayMessage() {
    return failure.message;
  }

  IconData _getIcon() {
    if (failure is NetworkFailure) return Icons.wifi_off;
    if (failure is AuthFailure) return Icons.lock_outline;
    if (failure is NotFoundFailure) return Icons.search_off;
    if (failure is ServerFailure) return Icons.cloud_off;
    if (failure is ValidationFailure) return Icons.error_outline;
    return Icons.error_outline;
  }
}

/// A simpler inline error widget for use within forms or cards.
class InlineError extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const InlineError({
    super.key,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: theme.colorScheme.errorContainer,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        children: [
          Icon(
            Icons.error_outline,
            color: theme.colorScheme.onErrorContainer,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message,
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onErrorContainer,
              ),
            ),
          ),
          if (onRetry != null)
            IconButton(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              color: theme.colorScheme.onErrorContainer,
            ),
        ],
      ),
    );
  }
}
