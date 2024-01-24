import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:lazy_summoners_war_web/artifact.dart';

class ArtifactDisplay extends StatefulWidget {
  bool loadingJson;

  ArtifactDisplay({
    super.key,
    this.loadingJson = false,
  });

  @override
  _ArtifactDisplayState createState() => _ArtifactDisplayState();
}

class _ArtifactDisplayState extends State<ArtifactDisplay> {
  int selectedMainStat = 0;
  Map<int, List<dynamic>> artifacts = {};
  Map<dynamic, Map<int, List<dynamic>>> savedArtifacts = {};
  int size = 4;

  @override
  void initState() {
    super.initState();
    getBestArtifacts(
      [
        305,
        306,
        307,
        308,
        309,
      ],
      type:
          Artifact.artifactTypeStrings.values.toList().indexOf("Attribute") + 1,
      mainStat: selectedMainStat,
    );
  }

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
                  SingleChildScrollView(
                    child: displayAttributeArtifacts(),
                  ),
                  displayUnitStyleArtifacts(),
                ],
              ),
            ),
        ],
      ),
    );
  }

  void getBestArtifacts(List<double> subStats, {type = 0, mainStat = 0}) async {
    widget.loadingJson = true;
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
        // For each artifact, add it to the list of artifacts of the corresponding attribute
        setState(() {
          artifacts = {};
          for (var attribute in Artifact.attributeStrings.keys) {
            artifacts[attribute] = [];
          }
        });
        var attributeIndex = 0;
        for (var attribute in Artifact.attributeStrings.keys) {
          for (var i = 0; i < size; i++) {
            setState(() {
              artifacts[attribute]!.add(responseData[attributeIndex][i]);
            });
          }
          attributeIndex++;
        }
        setState(() {
          savedArtifacts[mainStat] = artifacts;
        });
        widget.loadingJson = false;
      } else {
        // Handle the error case if needed
        print('Request failed with status: ${response.statusCode}.');
      }
    } catch (e, stacktrace) {
      print('getBestArtifacts: ${e.toString()}');
      print(stacktrace);
    }
  }

  Widget displayAttributeArtifacts() {
    List<DropdownMenuItem> mainStatsItem = [];
    mainStatsItem.add(
      const DropdownMenuItem(
        value: 0,
        child: Text("ALL"),
      ),
    );
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
                      if (savedArtifacts[selectedMainStat] != null) {
                        artifacts = savedArtifacts[selectedMainStat]!;
                      } else {
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
                        );
                      }
                    });
                  },
                ),
              ],
            ),
          ],
        ),
        createArtifactTables(),
      ],
    );
  }

  Widget displayUnitStyleArtifacts() {
    return const Text('Type Artifacts');
  }

  Widget? displayAttributeIcon(int attribute, double size) {
    try {
      Image image = Image.asset(
        'artifacts/attributes/${Artifact.attributeStrings[attribute].toString().toLowerCase()}.png',
        width: size,
        height: size,
      );
      return image;
    } catch (e, stacktrace) {
      print('displayArtifactIcon: ${e.toString()}');
      print(stacktrace);
    }
    return null;
  }

  Widget displayMainStatIcon(int mainStat, double size) {
    try {
      Image image = Image.asset(
        'artifacts/main_stats/${Artifact.mainStatStrings[mainStat].toString().toLowerCase()}.png',
        width: size,
        height: size,
      );
      return image;
    } catch (e, stacktrace) {
      print('displayArtifactIcon: ${e.toString()}');
      print(stacktrace);
      return const SizedBox();
    }
  }

  Widget createArtifactTable(int attribute) {
    final ArtifactsInfo artifactsInfo = ArtifactsInfo(
      attributes: Artifact.attributeStrings.keys.toList(),
      unitStyles: Artifact.unitStyleStrings.keys.toList(),
      mainStats: Artifact.mainStatStrings.keys.toList(),
    );
    artifactsInfo.attributes.removeAt(artifactsInfo.attributes.length - 1);
    var temp = artifactsInfo.attributes[0];
    artifactsInfo.attributes[0] = artifactsInfo.attributes[1];
    artifactsInfo.attributes[1] = temp;
    List<DataColumn> columns = [];
    try {
      for (var attribute in artifactsInfo.attributes) {
        columns.add(
          DataColumn(
            label: Expanded(
              child: Center(
                child: displayAttributeIcon(attribute, 16) ?? const Text('NA'),
              ),
            ),
          ),
        );
      }
      if (artifacts[attribute] == null || artifacts[attribute]!.isEmpty) {
        return DataTable(
          headingRowColor:
              MaterialStateColor.resolveWith((states) => Colors.grey.shade400),
          columns: columns,
          rows: const [],
        );
      }
      return DataTable(
        headingRowColor:
            MaterialStateColor.resolveWith((states) => Colors.grey.shade400),
        showBottomBorder: true,
        border: const TableBorder(
          verticalInside: BorderSide(
            color: Colors.grey,
            width: 1,
          ),
        ),
        columns: columns,
        rows: List.generate(
          artifacts[attribute]!.length,
          (index) {
            List<DataCell> cells = [];
            for (var attributeIndex = 0;
                attributeIndex < artifactsInfo.attributes.length;
                attributeIndex++) {
              var value = artifacts[attribute]![index][attributeIndex]["value"];
              if (value == 0) {
                cells.add(
                  const DataCell(
                    Center(
                      child: Padding(
                        padding: EdgeInsets.symmetric(horizontal: 12),
                        child: Text('   '),
                      ),
                    ),
                  ),
                );
                continue;
              }
              var backgroundColor = Colors.transparent;
              if (value < 22 && index == 0) {
                backgroundColor = Colors.red;
              }
              cells.add(
                DataCell(
                  SizedBox.expand(
                    child: Container(
                      color: backgroundColor,
                      child: Row(
                        children: [
                          displayMainStatIcon(
                              jsonDecode(artifacts[attribute]![index]
                                      [attributeIndex]
                                  ["artifact"])["pri_effects"][0],
                              20),
                          const SizedBox(width: 4),
                          Text(
                            artifacts[attribute]![index][attributeIndex]
                                    ["value"]
                                .toString(),
                            style: const TextStyle(
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              );
            }
            return DataRow(cells: cells);
          },
        ),
      );
    } catch (e, stacktrace) {
      print('createArtifactTable: ${e.toString()}');
      print(stacktrace);
      return DataTable(
        columns: columns,
        rows: const [],
        headingRowColor:
            MaterialStateColor.resolveWith((states) => Colors.grey.shade400),
      );
    }
  }

  Widget createArtifactTables() {
    try {
      final ArtifactsInfo artifactsInfo = ArtifactsInfo(
        attributes: Artifact.attributeStrings.keys.toList(),
        unitStyles: Artifact.unitStyleStrings.keys.toList(),
        mainStats: Artifact.mainStatStrings.keys.toList(),
      );

      return SizedBox(
        height: 1000,
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisExtent: 400,
          ),
          itemCount: artifactsInfo.attributes.length,
          itemBuilder: (BuildContext context, int index) {
            var attribute = artifactsInfo.attributes[index];
            return Column(
              children: [
                displayAttributeIcon(attribute, 32) ?? const SizedBox(),
                const SizedBox(height: 8),
                createArtifactTable(attribute),
                const SizedBox(height: 32),
              ],
            );
          },
        ),
      );
    } catch (e, stacktrace) {
      print('createArtifactTables: ${e.toString()}');
      print(stacktrace);
      return const SizedBox();
    }
  }
}
