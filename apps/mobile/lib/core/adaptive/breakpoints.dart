import 'package:flutter/material.dart';

/// Breakpoint definitions for responsive/adaptive layouts.
/// 
/// Mirrors Material 3's adaptive breakpoint system:
/// - compact: phones in portrait
/// - medium: phones in landscape, small tablets
/// - expanded: tablets in landscape, foldables unfolded
/// - large: very large tablets
/// 
/// See docs/architecture/mobile.md §4 for the breakpoint system.
class Breakpoints {
  Breakpoints._();

  static const double compactMax = 600;
  static const double mediumMax = 840;
  static const double expandedMax = 1200;

  /// Check if current width is compact.
  static bool isCompact(BuildContext context) {
    return MediaQuery.sizeOf(context).width < compactMax;
  }

  /// Check if current width is medium.
  static bool isMedium(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    return width >= compactMax && width < mediumMax;
  }

  /// Check if current width is expanded.
  static bool isExpanded(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    return width >= mediumMax && width < expandedMax;
  }

  /// Check if current width is large.
  static bool isLarge(BuildContext context) {
    return MediaQuery.sizeOf(context).width >= expandedMax;
  }

  /// Get current breakpoint name.
  static String current(BuildContext context) {
    if (isCompact(context)) return 'compact';
    if (isMedium(context)) return 'medium';
    if (isExpanded(context)) return 'expanded';
    return 'large';
  }

  /// Build different widgets based on breakpoint.
  static Widget builder({
    required BuildContext context,
    required Widget compact,
    Widget? medium,
    Widget? expanded,
    Widget? large,
  }) {
    if (isCompact(context)) return compact;
    if (isMedium(context)) return medium ?? compact;
    if (isExpanded(context)) return expanded ?? medium ?? compact;
    return large ?? expanded ?? medium ?? compact;
  }
}

/// Extension for convenient breakpoint checks on BuildContext.
extension BreakpointContext on BuildContext {
  /// True if compact (phone portrait).
  bool get isCompact => Breakpoints.isCompact(this);

  /// True if medium (phone landscape, small tablet).
  bool get isMedium => Breakpoints.isMedium(this);

  /// True if expanded (tablet landscape, foldable).
  bool get isExpanded => Breakpoints.isExpanded(this);

  /// True if large (very large tablet).
  bool get isLarge => Breakpoints.isLarge(this);

  /// Minimum tap target size for current platform.
  /// iOS: 44pt, Material: 48dp
  double get minTapTargetSize {
    final platform = Theme.of(this).platform;
    if (platform == TargetPlatform.iOS || platform == TargetPlatform.macOS) {
      return 44.0;
    }
    return 48.0;
  }
}
