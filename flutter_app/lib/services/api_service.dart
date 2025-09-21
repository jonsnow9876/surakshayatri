// lib/services/api_service.dart
import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/tourist.dart';
import '../models/report.dart';
import '../models/alert.dart';
import '../utils/constants.dart';

class ApiService {
  final String base = apiBaseUrl;

  // Register tourist (POST /register/)
  Future<Tourist> registerTourist(Map<String, dynamic> payload) async {
    final url = Uri.parse('$base/register/');
    final res = await http.post(url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload));
    if (res.statusCode == 200 || res.statusCode == 201) {
      return Tourist.fromJson(jsonDecode(res.body));
    } else {
      throw Exception('Register failed: ${res.statusCode} ${res.body}');
    }
  }

  // Fetch alerts (GET /alerts/)
  Future<List<AlertModel>> fetchAlerts() async {
    final url = Uri.parse('$base/alerts/');
    final res = await http.get(url);
    if (res.statusCode == 200) {
      final list = jsonDecode(res.body) as List<dynamic>;
      return list.map((e) => AlertModel.fromJson(e)).toList();
    } else {
      throw Exception('Fetch alerts failed: ${res.statusCode}');
    }
  }

  // Trigger panic alert (POST /panic/)
  Future<void> triggerPanic(String touristId, double lat, double lon) async {
    final url = Uri.parse('$base/panic/');
    final payload = {
      'tourist_id': touristId,
      'latitude': lat,
      'longitude': lon
    };
    final res = await http.post(url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload));
    if (res.statusCode == 200 || res.statusCode == 201) {
      return;
    } else {
      throw Exception('Panic failed: ${res.statusCode} ${res.body}');
    }
  }

  // Submit report (POST /reports/)
  Future<void> submitReport(String touristId, Report report) async {
    final url = Uri.parse('$base/reports/');
    try {
      final res = await http.post(url,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'tourist_id': touristId,
            ...report.toJson(),
          }));
      if (res.statusCode == 200 || res.statusCode == 201) {
        return;
      } else {
        throw Exception('Report submission failed: ${res.statusCode}');
      }
    } on SocketException {
      throw Exception('Network error while submitting report.');
    } catch (e) {
      rethrow;
    }
  }

  // ===============================================================
  // ## NEW METHOD ADDED BELOW ##
  // ===============================================================

  // Fetch reports for a specific tourist (GET /reports/{id})
  Future<List<Report>> fetchReports(String touristId) async {
    final url = Uri.parse('$base/reports/$touristId');
    final response = await http.get(
      url,
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      // Transform the list of json maps into a list of Report objects
      return data.map((json) => Report.fromJson(json)).toList();
    } else {
      // If the server did not return a 200 OK response, throw an exception.
      throw Exception('Failed to load reports. Status code: ${response.statusCode}');
    }
  }
}