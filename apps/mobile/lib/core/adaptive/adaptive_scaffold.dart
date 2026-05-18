import 'package:flutter/material.dart';

import 'breakpoints.dart';

/// Adaptive scaffold that switches navigation based on screen size.
/// 
/// - compact (phone): Bottom NavigationBar
/// - medium (small tablet): Side NavigationRail
/// - expanded/large (tablet): NavigationDrawer or dual-pane
/// 
/// All screens use this scaffold to maintain consistent navigation patterns.
class AdaptiveScaffold extends StatelessWidget {
  final Widget body;
  final int selectedIndex;
  final List<NavigationDestination> destinations;
  final ValueChanged<int> onDestinationSelected;
  final Widget? floatingActionButton;
  final List<Widget>? actions;
  final Widget? title;
  final bool showBackButton;

  const AdaptiveScaffold({
    super.key,
    required this.body,
    required this.selectedIndex,
    required this.destinations,
    required this.onDestinationSelected,
    this.floatingActionButton,
    this.actions,
    this.title,
    this.showBackButton = false,
  });

  @override
  Widget build(BuildContext context) {
    return Breakpoints.builder(
      context: context,
      compact: _buildCompactScaffold(context),
      medium: _buildMediumScaffold(context),
      expanded: _buildExpandedScaffold(context),
      large: _buildExpandedScaffold(context),
    );
  }

  Widget _buildCompactScaffold(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: title,
        actions: actions,
        automaticallyImplyLeading: showBackButton,
      ),
      body: body,
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: onDestinationSelected,
        destinations: destinations,
      ),
      floatingActionButton: floatingActionButton,
    );
  }

  Widget _buildMediumScaffold(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: title,
        actions: actions,
        automaticallyImplyLeading: showBackButton,
      ),
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: selectedIndex,
            onDestinationSelected: onDestinationSelected,
            destinations: destinations
                .map((d) => NavigationRailDestination(
                      icon: d.icon,
                      selectedIcon: d.selectedIcon,
                      label: Text(d.label),
                    ))
                .toList(),
          ),
          const VerticalDivider(thickness: 1, width: 1),
          Expanded(child: body),
        ],
      ),
      floatingActionButton: floatingActionButton,
    );
  }

  Widget _buildExpandedScaffold(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationDrawer(
            selectedIndex: selectedIndex,
            onDestinationSelected: onDestinationSelected,
            children: [
              if (title != null) ...[
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: DefaultTextStyle(
                    style: Theme.of(context).textTheme.titleLarge!,
                    child: title!,
                  ),
                ),
                const Divider(),
              ],
              ...destinations.map((d) => NavigationDrawerDestination(
                    icon: d.icon,
                    selectedIcon: d.selectedIcon,
                    label: Text(d.label),
                  )),
            ],
          ),
          const VerticalDivider(thickness: 1, width: 1),
          Expanded(
            child: Scaffold(
              appBar: actions != null
                  ? AppBar(
                      actions: actions,
                      automaticallyImplyLeading: showBackButton,
                    )
                  : null,
              body: body,
              floatingActionButton: floatingActionButton,
            ),
          ),
        ],
      ),
    );
  }
}

/// A simpler adaptive scaffold for screens without persistent navigation
/// (e.g., login, onboarding, detail screens).
class SimpleAdaptiveScaffold extends StatelessWidget {
  final Widget body;
  final PreferredSizeWidget? appBar;
  final Widget? floatingActionButton;

  const SimpleAdaptiveScaffold({
    super.key,
    required this.body,
    this.appBar,
    this.floatingActionButton,
  });

  @override
  Widget build(BuildContext context) {
    // On large screens, center the content with padding
    if (context.isLarge || context.isExpanded) {
      return Scaffold(
        appBar: appBar,
        body: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 840),
            child: body,
          ),
        ),
        floatingActionButton: floatingActionButton,
      );
    }

    // On smaller screens, full-width
    return Scaffold(
      appBar: appBar,
      body: body,
      floatingActionButton: floatingActionButton,
    );
  }
}
