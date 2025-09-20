// lib/utils/shared_prefs.dart
import 'package:shared_preferences/shared_preferences.dart';

class Prefs {
  static Future<void> saveProfile({
    required String touristId,
    required String name,
    String? phone,
    String? email,
  }) async {
    final p = await SharedPreferences.getInstance();
    await p.setString('tourist_id', touristId);
    await p.setString('profile_name', name);
    if (phone != null) await p.setString('profile_phone', phone);
    if (email != null) await p.setString('profile_email', email);
  }

  static Future<String?> getTouristId() async {
    final p = await SharedPreferences.getInstance();
    return p.getString('tourist_id');
  }

  static Future<Map<String, String?>> loadProfile() async {
    final p = await SharedPreferences.getInstance();
    return {
      'id': p.getString('tourist_id'),
      'name': p.getString('profile_name'),
      'phone': p.getString('profile_phone'),
      'email': p.getString('profile_email'),
    };
  }

  static Future<void> clearAll() async {
    final p = await SharedPreferences.getInstance();
    await p.clear();
  }
}
