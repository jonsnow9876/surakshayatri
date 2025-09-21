// lib/screens/splash_screen.dart
import 'package:flutter/material.dart';
import '../utils/shared_prefs.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});
  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    Future.delayed(const Duration(milliseconds: 800), _goNext);
  }

  Future<void> _goNext() async {
    final id = await Prefs.getTouristId();
    if (id == null || id.isEmpty) {
      Navigator.pushReplacementNamed(context, '/register');
    } else {
      Navigator.pushReplacementNamed(context, '/dashboard');
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Suraksha Yatri', style: TextStyle(fontSize: 24))),
    );
  }
}
