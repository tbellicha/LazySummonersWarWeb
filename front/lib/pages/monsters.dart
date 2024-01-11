import 'package:flutter/cupertino.dart';

import '../loading.dart';

Widget displayMonsters(Map<String, dynamic> fileData, bool loadingJSON) {
  if (loadingJSON) {
    return loadingInProgress();
  }
  if (fileData['monsters'] == null) {
    return const Text('No monsters found');
  }
  return GridView.builder(
    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
      crossAxisCount: 16,
    ),
    itemBuilder: (context, index) {
      return Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage(
              'monsters/${fileData['monsters'][index]["image_filename"]}',
            ),
          ),
        ),
      );
    },
    itemCount: fileData['monsters'].length,
  );
}
