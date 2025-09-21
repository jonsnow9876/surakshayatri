// lib/screens/dashboard_page.dart

// 1. IMPORT the correct package
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'dart:async';
import 'package:flutter/material.dart';
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
  LatLng _center = const LatLng(28.6139, 77.2090); // Default center
  LatLng? _current;
  Timer? _poller;

  // 2. ADD a controller for the map
  final Completer<GoogleMapController> _controller = Completer();

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

    // Animate camera to new position
    final GoogleMapController controller = await _controller.future;
    controller.animateCamera(CameraUpdate.newCameraPosition(
      CameraPosition(target: LatLng(pos.latitude, pos.longitude), zoom: 14.0),
    ));

    setState(() {
      _current = LatLng(pos.latitude, pos.longitude);
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
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Not registered')));
      return;
    }
    if (_current == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Location not available')));
      return;
    }
    try {
      await _api.triggerPanic(id, _current!.latitude, _current!.longitude);
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Panic sent')));
      await _loadAlerts();
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Panic failed: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    // 3. CREATE markers for Google Maps
    final Set<Marker> markers = {};
    if (_current != null) {
      markers.add(
        Marker(
          markerId: const MarkerId('currentUser'),
          position: _current!,
          icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueAzure), // Different icon for user
        ),
      );
    }
    // Note: You would also add markers for your alerts here

    return Scaffold(
      appBar: AppBar(title: const Text('Dashboard')),
      body: Column(
        children: [
          Expanded(
            flex: 3,
            // 4. USE the GoogleMap widget
            child: GoogleMap(
              initialCameraPosition: CameraPosition(target: _center, zoom: 13),
              markers: markers,
              onMapCreated: (GoogleMapController controller) {
                _controller.complete(controller);
              },
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
                        leading: Icon(a.resolved ? Icons.check_circle : Icons.warning, color: a.resolved ? Colors.green : Colors.red),
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
          ListTile(title: const Text('Profile'), onTap: () => Navigator.pushNamed(context, '/profile')),
          ListTile(title: const Text('Report'), onTap: () => Navigator.pushNamed(context, '/report')),
          ListTile(title: const Text('Reports'), onTap: () => Navigator.pushNamed(context, '/reports')),
        ]),
      ),
    );
  }
}