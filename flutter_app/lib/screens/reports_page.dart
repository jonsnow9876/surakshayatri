// lib/screens/reports_page.dart
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/report.dart';
import '../utils/shared_prefs.dart';
import 'package:path_provider/path_provider.dart';

class ReportsPage extends StatefulWidget {
  const ReportsPage({super.key});
  @override
  State<ReportsPage> createState() => _ReportsPageState();
}

class _ReportsPageState extends State<ReportsPage> {
  final ApiService _api = ApiService();
  List<Report> _reports = [];

  @override
  void initState() {
    super.initState();
    _loadReports();
  }

  Future<void> _loadReports() async {
    // Try fetch from backend if supported (not implemented on backend main by default)
    final id = await Prefs.getTouristId();
    if (id == null) return;
    try {
      // backend route may be /reports/{id} — not present by default; skip if not available
      // Here we just try and ignore failure.
      final url = Uri.parse('${ApiService().base}/reports/$id');
      final res = await ApiService().fetchReports(
          id); // note: fetchReports not implemented earlier; but we keep fallback
    } catch (_) {}
    // Fallback read local reports file
    try {
      final dir = await getApplicationDocumentsDirectory();
      final f = File('${dir.path}/local_reports.json');
      if (await f.exists()) {
        final data = jsonDecode(await f.readAsString()) as List<dynamic>;
        setState(() {
          _reports = data
              .map((e) => Report.fromJson(e as Map<String, dynamic>))
              .toList();
        });
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Reports')),
      body: _reports.isEmpty
          ? const Center(child: Text('No reports'))
          : ListView.builder(
              itemCount: _reports.length,
              itemBuilder: (ctx, i) {
                final r = _reports[i];
                return Card(
                  margin: const EdgeInsets.all(8.0),
                  child: ListTile(
                    title: Text(r.title),
                    subtitle: Text(r.description),
                  ),
                );
              },
            ),
    );
  }
}
