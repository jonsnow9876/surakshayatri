class Tourist {
  final String permanentId;
  final String tempId;
  final String name;
  final String phone;
  final String email;

  Tourist({
    required this.permanentId,
    required this.tempId,
    required this.name,
    required this.phone,
    required this.email,
  });

  factory Tourist.fromJson(Map<String, dynamic> json) {
    return Tourist(
      permanentId: json['permanent_id'],
      tempId: json['temp_id'],
      name: json['name'],
      phone: json['phone'],
      email: json['email'],
    );
  }
}
