// lib/screens/dashboard_page.dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../services/api_service.dart';
import '../models/alert.dart';
import '../services/location_service.dart';
import '../utils/shared_prefs.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});
  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  final ApiService _api = ApiService();
  List<AlertModel> _alerts = [];
  LatLng _center = LatLng(28.6139, 77.2090);
  LatLng? _current;
  Timer? _poller;

  @override
  void initState() {
    super.initState();
    _loadAlerts();
    _startPolling();
    _ensureLocation();
  }

  void _startPolling() {
    _poller = Timer.periodic(const Duration(seconds: 10), (_) => _loadAlerts());
  }

  Future<void> _ensureLocation() async {
    final ok = await LocationService.ensurePermission();
    if (!ok) return;
    final pos = await LocationService.getCurrentPosition();
    setState(() {
      _current = LatLng(pos.latitude, pos.longitude);
      _center = _current!;
    });
  }

  Future<void> _loadAlerts() async {
    try {
      final list = await _api.fetchAlerts();
      setState(() => _alerts = list);
    } catch (e) {
      // ignore or show small message
    }
  }

  @override
  void dispose() {
    _poller?.cancel();
    super.dispose();
  }

  Future<void> _triggerPanic() async {
    final id = await Prefs.getTouristId();
    if (id == null) {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Not registered')));
      return;
    }
    if (_current == null) {
      ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Location not available')));
      return;
    }
    try {
      await _api.triggerPanic(id, _current!.latitude, _current!.longitude);
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('Panic sent')));
      await _loadAlerts();
    } catch (e) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Panic failed: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    final markers = <Marker>[];
    if (_current != null) {
      markers.add(Marker(
          point: _current!,
          width: 40,
          height: 40,
          builder: (ctx) => const Icon(Icons.person_pin_circle,
              size: 36, color: Colors.blue)));
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard')),
      body: Column(
        children: [
          Expanded(
            flex: 3,
            child: FlutterMap(
              options: MapOptions(center: _center, zoom: 13),
              children: [
                TileLayer(
                    urlTemplate:
                        'https://tile.openstreetmap.org/{z}/{x}/{y}.png'),
                MarkerLayer(markers: markers),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: _alerts.isEmpty
                ? const Center(child: Text('No alerts'))
                : ListView.builder(
                    itemCount: _alerts.length,
                    itemBuilder: (ctx, i) {
                      final a = _alerts[i];
                      return ListTile(
                        leading: Icon(
                            a.resolved ? Icons.check_circle : Icons.warning,
                            color: a.resolved ? Colors.green : Colors.red),
                        title: Text(a.message),
                        subtitle: Text(a.timestamp),
                      );
                    },
                  ),
          )
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _triggerPanic,
        label: const Text('PANIC'),
        icon: const Icon(Icons.report_problem),
        backgroundColor: Colors.red,
      ),
      drawer: Drawer(
        child: ListView(children: [
          ListTile(
              title: const Text('Profile'),
              onTap: () => Navigator.pushNamed(context, '/profile')),
          ListTile(
              title: const Text('Report'),
              onTap: () => Navigator.pushNamed(context, '/report')),
          ListTile(
              title: const Text('Reports'),
              onTap: () => Navigator.pushNamed(context, '/reports')),
        ]),
      ),
    );
  }
}
