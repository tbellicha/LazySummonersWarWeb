import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../artifact.dart';

class ArtifactDisplay extends StatefulWidget {
  final bool loadingJson;

  const ArtifactDisplay({super.key, this.loadingJson = false});
  @override
  _ArtifactDisplayState createState() => _ArtifactDisplayState();
}

class _ArtifactDisplayState extends State<ArtifactDisplay> {
  int selectedMainStat = 0;
  List<List> artifacts = List.generate(
    Artifact.attributeStrings.length,
    (index) => [],
  );
  int size = 2;

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Column(
        children: [
          const TabBar(
            tabs: [
              Tab(text: 'Attribute'),
              Tab(text: 'Unit Style'),
            ],
          ),
          if (widget.loadingJson)
            const Expanded(
              child: Center(
                child: CircularProgressIndicator(),
              ),
            )
          else
            Expanded(
              child: TabBarView(
                children: [
                  displayAttributeArtifacts(),
                  displayUnitStyleArtifacts(),
                ],
              ),
            ),
        ],
      ),
    );
  }

  void getBestArtifacts(List<int> subStats, {type = 0, mainStat = 0}) async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:5000/api/get_bests_artifacts').replace(
          queryParameters: {
            'type': type.toString(),
            'main_stat': mainStat.toString(),
            'size': size.toString(),
            'sub_stats': jsonEncode(subStats),
          },
        ),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        print(responseData);
        // For each artifact, add it to the list of artifacts of the corresponding attribute
        for (var obj in responseData) {
          if (obj.containsKey("value") && obj.containsKey("artifact")) {
            var value = obj["value"];
            var artifact = Artifact.fromJson(obj["artifact"]);
            artifacts[artifact.attribute].add(artifact);
          } else {
            print("Unexpected response format.");
          }
        }
      } else {
        // Handle the error case if needed
        print('Request failed with status: ${response.statusCode}.');
      }
    } catch (e) {
      print('getBestArtifacts: ${e.toString()}');
    }
  }

  Widget displayAttributeArtifacts() {
    List<DropdownMenuItem> mainStatsItem = [];
    mainStatsItem.add(const DropdownMenuItem(
      value: 0,
      child: Text("ALL"),
    ));
    for (var mainStat in Artifact.mainStatStrings.keys) {
      mainStatsItem.add(DropdownMenuItem(
        value: mainStat,
        child: Text(Artifact.mainStatStrings[mainStat]!),
      ));
    }

    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Column(
              children: [
                const Text(
                  'Main Stat',
                  style: TextStyle(
                    fontSize: 16,
                  ),
                ),
                DropdownButton(
                  items: mainStatsItem,
                  value: selectedMainStat,
                  alignment: Alignment.center,
                  onChanged: (value) {
                    setState(() {
                      selectedMainStat = value;
                    });
                  },
                ),
              ],
            ),
          ],
        ),
        ElevatedButton(
          onPressed: () async => {
            // with the type of value artifact
            getBestArtifacts(
              [
                305,
                306,
                307,
                308,
                309,
              ],
              type: Artifact.artifactTypeStrings.values
                      .toList()
                      .indexOf("Attribute") +
                  1,
              mainStat: selectedMainStat,
            ),
          },
          child: const Text('Get best artifacts'),
        ),
        createArtifactTables(),
      ],
    );
  }

  Widget displayUnitStyleArtifacts() {
    return const Text('Type Artifacts');
  }

  Widget? displayArtifactIcon(int attribute, double size) {
    try {
      Image image = Image.asset(
        'attributes/${Artifact.attributeStrings[attribute].toString().toLowerCase()}.png',
        width: size,
        height: size,
      );
      return image;
    } catch (e) {
      print('displayArtifactIcon: ${e.toString()}');
    }
    return null;
  }

  Widget createArtifactTable(int attribute) {
    final ArtifactsInfo artifactsInfo = ArtifactsInfo(
      attributes: Artifact.attributeStrings.keys.toList(),
      unitStyles: Artifact.unitStyleStrings.keys.toList(),
      mainStats: Artifact.mainStatStrings.keys.toList(),
    );
    artifactsInfo.attributes.removeAt(artifactsInfo.attributes.length - 1);
    List<DataColumn> columns = [];
    try {
      for (var attribute in artifactsInfo.attributes) {
        columns.add(DataColumn(
            label: displayArtifactIcon(attribute, 16) ?? const Text('NA')));
      }
      // File the rows with the artifacts
      return DataTable(
        columns: columns,
        rows: List.generate(
          artifacts[attribute].length,
          (index) => DataRow(
            cells: List.generate(
              artifactsInfo.attributes.length,
              (index2) => DataCell(
                Text(
                  artifacts[attribute][index][artifactsInfo.attributes[index2]]
                      .toString(),
                ),
              ),
            ),
          ),
        ),
        headingRowColor:
            MaterialStateColor.resolveWith((states) => Colors.grey.shade400),
      );
    } catch (e) {
      print('createArtifactTable: ${e.toString()}');
      return DataTable(
        columns: columns,
        rows: const [],
        headingRowColor:
            MaterialStateColor.resolveWith((states) => Colors.grey.shade400),
      );
    }
  }

  Widget createArtifactTables() {
    final ArtifactsInfo artifactsInfo = ArtifactsInfo(
      attributes: Artifact.attributeStrings.keys.toList(),
      unitStyles: Artifact.unitStyleStrings.keys.toList(),
      mainStats: Artifact.mainStatStrings.keys.toList(),
    );
    List<Widget> tables = [];
    // Show the tables in a response way
    for (var attribute in artifactsInfo.attributes) {
      tables.add(displayArtifactIcon(attribute, 32) ?? const SizedBox());
      tables.add(const SizedBox(height: 8));
      tables.add(createArtifactTable(attribute));
      tables.add(const SizedBox(height: 32));
    }
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: tables,
    );
  }
}
