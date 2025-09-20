// lib/screens/register_page.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../utils/shared_prefs.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({super.key});
  @override
  State<RegisterPage> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameCtl = TextEditingController();
  final _phoneCtl = TextEditingController();
  final api = ApiService();
  bool _loading = false;

  Future<void> _onSubmit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      final payload = {
        'name': _nameCtl.text.trim(),
        'phone': _phoneCtl.text.trim(),
      };
      final tourist = await api.registerTourist(payload);
      await Prefs.saveProfile(
        touristId: tourist.id,
        name: tourist.name,
        phone: tourist.phone,
        email: tourist.email,
      );
      Navigator.pushReplacementNamed(context, '/otp');
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Register failed: $e')));
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _nameCtl.dispose();
    _phoneCtl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Register')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                  controller: _nameCtl,
                  decoration: const InputDecoration(labelText: 'Full name'),
                  validator: (v) =>
                      (v == null || v.trim().length < 2) ? 'Enter name' : null),
              const SizedBox(height: 10),
              TextFormField(
                  controller: _phoneCtl,
                  decoration: const InputDecoration(labelText: 'Phone'),
                  keyboardType: TextInputType.phone,
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Enter phone' : null),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _loading ? null : _onSubmit,
                child: _loading
                    ? const CircularProgressIndicator()
                    : const Text('Register'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
