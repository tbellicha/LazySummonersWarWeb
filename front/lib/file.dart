import 'dart:convert';

import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as path;

class MyFile {
  static Future<Map<String, dynamic>> selectFile() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['json'],
    );
    if (result != null) {
      String fileName = path.basename(result.files.single.name);
      String fileContent = String.fromCharCodes(result.files.single.bytes!);
      return {'fileName': fileName, 'fileContent': fileContent};
    } else {
      return {'fileName': '', 'fileContent': ''};
    }
  }

  static Map<String, dynamic> _prepareDataForUpload(String fileContent) {
    // Convert the file content string to a map
    Map<String, dynamic> data = jsonDecode(fileContent);

    // Remove the unwanted keys from the map
    data.remove("defense_unit_list");
    data.remove("server_arena_defense_unit_list");
    data.remove("quest_active");
    data.remove("quest_rewarded");
    data.remove("event_id_list");
    data.remove("building_list");
    data.remove("deco_list");
    data.remove("obstacle_list");
    data.remove("mob_costume_equip_list");
    data.remove("mob_costume_part_list");
    data.remove("object_storage_list");
    data.remove("object_state");
    data.remove("homunculus_skill_list");
    data.remove("unit_collection");
    data.remove("summon_special_info");
    data.remove("island_info");
    data.remove("inventory_info");
    data.remove("inventory_open_info");
    data.remove("inventory_mail_info");
    data.remove("emoticon_favorites");
    data.remove("wish_list");
    data.remove("markers");
    data.remove("shop_info");
    data.remove("period_item_list");
    data.remove("notice_info");
    data.remove("guild");

    return data;
  }

  static Future<Map<String, dynamic>> loadFileContent(String selectedFileName,
      String fileContent, Map<String, dynamic> selectedSet) async {
    try {
      final response = await http.post(
        Uri.parse('http://localhost:5000/api/load_json'),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'file_name': selectedFileName,
          'file_content': _prepareDataForUpload(fileContent),
          'set': selectedSet,
        }),
      );
      if (response.statusCode == 200) {
        // If the server returns a success response, update the counter with the received data
        final responseData = jsonDecode(response.body);
        final monsters = responseData["monsters"];
        var monstersData = <Map<String, dynamic>>[];
        final artifacts = responseData["artifacts"];
        var artifactsData = <Map<String, dynamic>>[];
        final runes = responseData["runes"];
        var runesData = <Map<String, dynamic>>[];

        for (var element in monsters) {
          monstersData.add(jsonDecode(element));
        }
        for (var element in artifacts) {
          artifactsData.add(jsonDecode(element));
        }
        for (var element in runes) {
          runesData.add(jsonDecode(element));
        }
        return {
          'score': responseData["score"],
          'runes': runesData,
          'table': responseData["table"],
          'monsters': monstersData,
          'artifacts': artifactsData,
        };
      } else {
        print('Request failed with status: ${response.statusCode}.');
        return {
          'score': 0,
          'runes': [],
          'table': [],
          'monsters': [],
          'artifacts': [],
        };
      }
    } catch (e, stacktrace) {
      print('loadFileContent: ${e.toString()}');
      print(stacktrace);
      return {
        'score': 0,
        'runes': [],
        'table': [],
        'monsters': [],
        'artifacts': [],
      };
    }
  }
}
