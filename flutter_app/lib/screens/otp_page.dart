// lib/screens/otp_page.dart
import 'package:flutter/material.dart';
import '../utils/shared_prefs.dart';

class OtpPage extends StatelessWidget {
  const OtpPage({super.key});
  @override
  Widget build(BuildContext context) {
    // Mock OTP flow: pressing Verify goes to dashboard
    return Scaffold(
      appBar: AppBar(title: const Text('Verify OTP')),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            // In real app: verify OTP via API
            Navigator.pushReplacementNamed(context, '/dashboard');
          },
          child: const Text('Verify (mock)'),
        ),
      ),
    );
  }
}
