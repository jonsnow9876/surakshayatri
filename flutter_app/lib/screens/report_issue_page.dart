// lib/screens/report_issue_page.dart
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../models/report.dart';
import '../services/api_service.dart';
import '../utils/shared_prefs.dart';
import 'package:path_provider/path_provider.dart';

class ReportIssuePage extends StatefulWidget {
  const ReportIssuePage({super.key});
  @override
  State<ReportIssuePage> createState() => _ReportIssuePageState();
}

class _ReportIssuePageState extends State<ReportIssuePage> {
  final _formKey = GlobalKey<FormState>();
  final _titleCtl = TextEditingController();
  final _descCtl = TextEditingController();
  File? _image;
  final ApiService _api = ApiService();
  bool _loading = false;

  Future<void> _pickImage() async {
    try {
      final p = ImagePicker();
      final x = await p.pickImage(source: ImageSource.gallery, maxWidth: 1200);
      if (x == null) return;
      final tmp = File(x.path);
      setState(() => _image = tmp);
    } catch (e) {
      // image_picker may not work on web/desktop; ignore
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Image pick not available')));
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    final touristId = await Prefs.getTouristId();
    if (touristId == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Not registered')));
      setState(() => _loading = false);
      return;
    }
    String? base64img;
    if (_image != null) {
      final bytes = await _image!.readAsBytes();
      base64img = base64Encode(bytes);
    }
    final report = Report(
        title: _titleCtl.text.trim(),
        description: _descCtl.text.trim(),
        imageBase64: base64img);

    try {
      await _api.submitReport(touristId, report);
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Report submitted')));
      Navigator.pop(context);
    } catch (e) {
      // fallback - save locally
      final dir = await getApplicationDocumentsDirectory();
      final file = File('${dir.path}/local_reports.json');
      List existing = [];
      if (await file.exists()) {
        try {
          existing = jsonDecode(await file.readAsString()) as List;
        } catch (_) {}
      }
      existing.insert(0, report.toJson());
      await file.writeAsString(jsonEncode(existing));
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Saved locally (backend unavailable)')));
      Navigator.pop(context);
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _titleCtl.dispose();
    _descCtl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Report Issue')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                  controller: _titleCtl,
                  decoration: const InputDecoration(labelText: 'Title'),
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Enter title' : null),
              const SizedBox(height: 8),
              TextFormField(
                  controller: _descCtl,
                  decoration: const InputDecoration(labelText: 'Description'),
                  maxLines: 4,
                  validator: (v) => (v == null || v.trim().isEmpty)
                      ? 'Enter description'
                      : null),
              const SizedBox(height: 12),
              if (_image != null) Image.file(_image!, height: 160),
              Row(children: [
                ElevatedButton.icon(
                    onPressed: _pickImage,
                    icon: const Icon(Icons.photo),
                    label: const Text('Pick Image')),
                const SizedBox(width: 12),
                ElevatedButton(
                    onPressed: _submit,
                    child: _loading
                        ? const CircularProgressIndicator()
                        : const Text('Submit')),
              ]),
            ],
          ),
        ),
      ),
    );
  }
}
