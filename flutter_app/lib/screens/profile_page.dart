// lib/screens/profile_page.dart
import 'package:flutter/material.dart';
import '../utils/shared_prefs.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});
  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  String? id, name, phone, email;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final map = await Prefs.loadProfile();
    setState(() {
      id = map['id'];
      name = map['name'];
      phone = map['phone'];
      email = map['email'];
    });
  }

  Future<void> _logout() async {
    await Prefs.clearAll();
    Navigator.pushNamedAndRemoveUntil(context, '/register', (r) => false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Name: ${name ?? ""}'),
            const SizedBox(height: 8),
            Text('Phone: ${phone ?? ""}'),
            const SizedBox(height: 8),
            Text('Email: ${email ?? ""}'),
            const SizedBox(height: 20),
            ElevatedButton(onPressed: _logout, child: const Text('Logout')),
          ],
        ),
      ),
    );
  }
}
