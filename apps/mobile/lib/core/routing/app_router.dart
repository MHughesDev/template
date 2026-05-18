import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Application router configuration.
/// 
/// All routes are defined here. Deep links must match the backend's URL
/// structure where features overlap with the web client.
/// 
/// Example: /items/:id in mobile calls the same backend endpoint
/// that the web React client calls.
class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      debugLogDiagnostics: true,
      initialLocation: '/',
      redirect: _handleRedirect,
      routes: [
        // Splash / loading screen
        GoRoute(
          path: '/',
          builder: (context, state) => const Placeholder(
            child: Center(child: Text('Home Screen - TODO')),
          ),
        ),

        // Auth routes
        GoRoute(
          path: '/login',
          builder: (context, state) => const Placeholder(
            child: Center(child: Text('Login Screen - TODO')),
          ),
        ),
        GoRoute(
          path: '/register',
          builder: (context, state) => const Placeholder(
            child: Center(child: Text('Register Screen - TODO')),
          ),
        ),

        // Main app routes with bottom/side navigation
        ShellRoute(
          builder: (context, state, child) {
            // This will be replaced with the actual adaptive scaffold
            // that manages navigation state
            return child;
          },
          routes: [
            GoRoute(
              path: '/dashboard',
              builder: (context, state) => const Placeholder(
                child: Center(child: Text('Dashboard - TODO')),
              ),
            ),
            GoRoute(
              path: '/items',
              builder: (context, state) => const Placeholder(
                child: Center(child: Text('Items List - TODO')),
              ),
              routes: [
                GoRoute(
                  path: ':id',
                  builder: (context, state) {
                    final id = state.pathParameters['id']!;
                    return Placeholder(
                      child: Center(child: Text('Item Detail: $id - TODO')),
                    );
                  },
                ),
              ],
            ),
            GoRoute(
              path: '/settings',
              builder: (context, state) => const Placeholder(
                child: Center(child: Text('Settings - TODO')),
              ),
            ),
          ],
        ),

        // 404
        GoRoute(
          path: '/404',
          builder: (context, state) => const Placeholder(
            child: Center(child: Text('Not Found')),
          ),
        ),
      ],
      errorBuilder: (context, state) => const Placeholder(
        child: Center(child: Text('Error: Route not found')),
      ),
    );
  }

  String? _handleRedirect(BuildContext context, GoRouterState state) {
    // TODO: Implement auth guard
    // - Check if user is authenticated
    // - If not and route requires auth, redirect to /login
    // - Include return URL as query parameter
    
    final isAuthRoute = state.matchedLocation == '/login' || 
                        state.matchedLocation == '/register';
    
    // Allow auth routes
    if (isAuthRoute) return null;
    
    // TODO: Check auth state and redirect if needed
    // final isAuthenticated = ref.read(authStateProvider);
    // if (!isAuthenticated) return '/login?from=${state.uri}';
    
    return null;
  }
}

/// Route names for type-safe navigation.
/// 
/// Use these instead of string literals.
abstract class Routes {
  Routes._();
  
  static const String home = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String dashboard = '/dashboard';
  static const String items = '/items';
  static String itemDetail(String id) => '/items/$id';
  static const String settings = '/settings';
  static const String notFound = '/404';
}

/// Extension for convenient navigation.
extension GoRouterX on BuildContext {
  /// Navigate to a named route with optional query parameters.
  void goTo(String path, {Map<String, String>? queryParams}) {
    if (queryParams != null && queryParams.isNotEmpty) {
      final queryString = queryParams.entries
          .map((e) => '${Uri.encodeComponent(e.key)}=${Uri.encodeComponent(e.value)}')
          .join('&');
      GoRouter.of(this).go('$path?$queryString');
    } else {
      GoRouter.of(this).go(path);
    }
  }

  /// Push a route onto the navigation stack.
  void pushTo(String path) => GoRouter.of(this).push(path);

  /// Pop the current route.
  void pop() => GoRouter.of(this).pop();

  /// Pop with a result.
  void popWithResult<T extends Object?>(T result) => GoRouter.of(this).pop(result);

  /// Replace current route.
  void replaceWith(String path) => GoRouter.of(this).replace(path);
}
