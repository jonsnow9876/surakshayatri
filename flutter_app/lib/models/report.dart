// lib/models/report.dart
class Report {
  final String title;
  final String description;
  final String? imageBase64; // optional base64 if we upload

  Report({required this.title, required this.description, this.imageBase64});

  factory Report.fromJson(Map<String, dynamic> json) {
    return Report(
      title: json['title'],
      description: json['description'],
      imageBase64: json['image'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'description': description,
      if (imageBase64 != null) 'image': imageBase64,
    };
  }
}
