import 'package:flutter/material.dart';

/// Common Dart/Flutter extensions used across the app.

/// String extensions.
extension StringX on String {
  /// Capitalize first letter.
  String get capitalize {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }

  /// Truncate with ellipsis.
  String truncate(int maxLength, {String ellipsis = '...'}) {
    if (length <= maxLength) return this;
    return '${substring(0, maxLength - ellipsis.length)}$ellipsis';
  }

  /// Check if valid email (basic regex).
  bool get isValidEmail {
    final regex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return regex.hasMatch(this);
  }

  /// Convert to snake_case.
  String get snakeCase {
    return replaceAllMapped(
      RegExp(r'[A-Z]'),
      (match) => '_${match.group(0)!.toLowerCase()}',
    ).replaceAll(RegExp(r'^_'), '');
  }

  /// Convert to camelCase.
  String get camelCase {
    final words = split(RegExp(r'[_-\s]+'));
    if (words.isEmpty) return this;
    return words.first.toLowerCase() +
        words.skip(1).map((w) => w.capitalize).join();
  }
}

/// DateTime extensions.
extension DateTimeX on DateTime {
  /// Format as relative time (e.g., "2 hours ago").
  String toRelativeTime() {
    final now = DateTime.now();
    final diff = now.difference(this);

    if (diff.inDays > 365) {
      final years = (diff.inDays / 365).floor();
      return '$years year${years > 1 ? 's' : ''} ago';
    }
    if (diff.inDays > 30) {
      final months = (diff.inDays / 30).floor();
      return '$months month${months > 1 ? 's' : ''} ago';
    }
    if (diff.inDays > 0) {
      return '${diff.inDays} day${diff.inDays > 1 ? 's' : ''} ago';
    }
    if (diff.inHours > 0) {
      return '${diff.inHours} hour${diff.inHours > 1 ? 's' : ''} ago';
    }
    if (diff.inMinutes > 0) {
      return '${diff.inMinutes} minute${diff.inMinutes > 1 ? 's' : ''} ago';
    }
    return 'just now';
  }

  /// Check if same day as another DateTime.
  bool isSameDay(DateTime other) {
    return year == other.year && month == other.month && day == other.day;
  }

  /// Start of day (00:00:00).
  DateTime get startOfDay {
    return DateTime(year, month, day);
  }

  /// End of day (23:59:59.999).
  DateTime get endOfDay {
    return DateTime(year, month, day, 23, 59, 59, 999);
  }
}

/// BuildContext extensions for common operations.
extension BuildContextX on BuildContext {
  /// Show a snackbar.
  void showSnackBar(String message, {bool isError = false}) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: isError
            ? Theme.of(this).colorScheme.error
            : Theme.of(this).colorScheme.primary,
      ),
    );
  }

  /// Show a modal bottom sheet.
  Future<T?> showBottomSheet<T>(Widget child, {bool isScrollControlled = true}) {
    return showModalBottomSheet<T>(
      context: this,
      isScrollControlled: isScrollControlled,
      builder: (_) => child,
    );
  }

  /// Show an alert dialog.
  Future<bool?> showConfirmDialog({
    required String title,
    required String message,
    String? confirmText,
    String? cancelText,
    bool isDestructive = false,
  }) {
    return showDialog<bool>(
      context: this,
      builder: (_) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(this).pop(false),
            child: Text(cancelText ?? 'Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.of(this).pop(true),
            child: Text(
              confirmText ?? 'Confirm',
              style: isDestructive
                  ? TextStyle(color: Theme.of(this).colorScheme.error)
                  : null,
            ),
          ),
        ],
      ),
    );
  }

  /// Hide keyboard.
  void hideKeyboard() {
    FocusScope.of(this).unfocus();
  }

  /// True if keyboard is visible.
  bool get isKeyboardVisible {
    return MediaQuery.viewInsetsOf(this).bottom > 0;
  }
}

/// AsyncValue extensions for Riverpod.
extension AsyncValueX<T> on AsyncValue<T> {
  /// Execute action only when data is present.
  void whenData(void Function(T data) action) {
    if (hasValue && value != null) {
      action(value as T);
    }
  }

  /// Get error message or null.
  String? get errorMessage {
    return error?.toString();
  }
}
