// lib/models/alert.dart
class AlertModel {
  final String id;
  final String message;
  final String timestamp;
  final bool resolved;

  AlertModel({
    required this.id,
    required this.message,
    required this.timestamp,
    required this.resolved,
  });

  factory AlertModel.fromJson(Map<String, dynamic> json) {
    return AlertModel(
      id: json['id']?.toString() ?? json['uuid']?.toString() ?? '',
      message: json['message'] ?? json['msg'] ?? '',
      timestamp: json['time'] ?? json['timestamp'] ?? '',
      resolved: json['resolved'] ?? false,
    );
  }
}
