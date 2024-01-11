import 'package:flutter/material.dart';
import 'package:lazy_summoners_war_web/loading.dart';

class RuneSet {
  final int nbRunes;
  final String set;

  RuneSet({
    required this.nbRunes,
    required this.set,
  });
}

Widget buildDataTableWidget(Map<String, dynamic> fileData) {
  List<DataColumn> columns = [];
  List<DataRow> rows = [];

  List<dynamic> uniqueEffectLevels =
      fileData['table'].map((element) => element[1]).toSet().toList();
  columns.add(const DataColumn(label: Text('')));
  for (var effectLevel in uniqueEffectLevels) {
    columns.add(DataColumn(label: Text(effectLevel.toString())));
  }
  List<dynamic> uniqueEffects =
      fileData['table'].map((element) => element[0]).toSet().toList();
  for (var effect in uniqueEffects) {
    List<DataCell> cells = [DataCell(Text(effect.toString()))];
    for (var effectLevel in uniqueEffectLevels) {
      var matchingRow = fileData['table'].firstWhere(
        (element) => element[0] == effect && element[1] == effectLevel,
        orElse: () => [effect, effectLevel, 0],
      );
      cells.add(DataCell(Text(matchingRow[2].toString())));
    }
    rows.add(DataRow(cells: cells));
  }
  return DataTable(
    columns: columns,
    rows: rows,
    headingRowColor:
        MaterialStateColor.resolveWith((states) => Colors.grey.shade400),
  );
}

Widget displayRunes(Map<String, dynamic> fileData, bool loadingJSON) {
  if (loadingJSON) {
    return loadingInProgress();
  }
  if (fileData['score'] == null) {
    return const Text('No runes found');
  }
  return Column(
    mainAxisAlignment: MainAxisAlignment.center,
    children: <Widget>[
      Text(
        'Score: ${fileData['score']}',
        style: const TextStyle(fontSize: 20),
      ),
      buildDataTableWidget(fileData),
    ],
  );
}
