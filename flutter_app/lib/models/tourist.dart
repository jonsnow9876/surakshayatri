// lib/models/tourist.dart
class Tourist {
  final String id;
  final String name;
  final String? phone;
  final String? email;

  Tourist({
    required this.id,
    required this.name,
    this.phone,
    this.email,
  });

  factory Tourist.fromJson(Map<String, dynamic> json) {
    return Tourist(
      id: json['id']?.toString() ?? json['permanent_id']?.toString() ?? '',
      name: json['name'] ?? json['profile_name'] ?? '',
      phone: json['phone'] ?? json['profile_phone'],
      email: json['email'] ?? json['profile_email'],
    );
  }
}
