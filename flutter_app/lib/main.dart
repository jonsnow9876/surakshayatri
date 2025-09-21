// lib/main.dart
import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';
import 'screens/register_page.dart';
import 'screens/otp_page.dart';
import 'screens/dashboard_page.dart';
import 'screens/profile_page.dart';
import 'screens/report_issue_page.dart';
import 'screens/reports_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Suraksha Yatri',
      theme: ThemeData(primarySwatch: Colors.indigo),
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      routes: {
        '/': (context) => const SplashScreen(),
        '/register': (context) => const RegisterPage(),
        '/otp': (context) => const OtpPage(),
        '/dashboard': (context) => const DashboardPage(),
        '/profile': (context) => const ProfilePage(),
        '/report': (context) => const ReportIssuePage(),
        '/reports': (context) => const ReportsPage(),
      },
    );
  }
}
