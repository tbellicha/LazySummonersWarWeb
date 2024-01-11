import 'package:flutter/material.dart';

class NavItem extends StatelessWidget {
  final IconData? icon;
  final Widget child;
  final VoidCallback? onTap;

  const NavItem({
    super.key,
    this.icon,
    required this.child,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              if (icon != null)
                Icon(
                  icon,
                  color: Colors.white,
                ),
              const SizedBox(width: 8),
              child,
            ],
          ),
          const Divider(
            color: Colors.white,
            thickness: 0.4,
          ),
        ],
      ),
    );
  }
}
