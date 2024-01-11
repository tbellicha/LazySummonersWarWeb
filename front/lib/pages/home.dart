import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:lazy_summoners_war_web/file.dart';
import 'package:lazy_summoners_war_web/nav_item.dart';
import 'package:lazy_summoners_war_web/pages/artifacts.dart';
import 'package:lazy_summoners_war_web/pages/monsters.dart';
import 'package:lazy_summoners_war_web/pages/runes.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  Map<String, dynamic> fileInformation = {};
  Map<String, dynamic> fileData = {};
  bool loadingJson = false;
  int _selectedTab = 2;
  final Map<String, dynamic> _selectedSet = {'ALL': 1};

  @override
  void initState() {
    super.initState();
    _updateSets();
  }

  void _updateSets() async {
    try {
      final response = await http.get(
        Uri.parse('http://localhost:5000/api/get_sets'),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
      );
      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        List<RuneSet> sets = responseData.map<RuneSet>((data) {
          return RuneSet(nbRunes: data['nbRunes'], set: data['set']);
        }).toList();
      } else {
        // Handle the error case if needed
        print('Request failed with status: ${response.statusCode}.');
      }
    } catch (e) {
      print('_updateSets: ${e.toString()}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          Container(
            width: 240,
            color: Colors.indigoAccent,
            child: Column(
              children: [
                NavItem(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Padding(
                        padding:
                            const EdgeInsetsDirectional.fromSTEB(0, 6, 0, 0),
                        child: ElevatedButton(
                          onPressed: () async => {
                            fileInformation = await MyFile.selectFile(),
                            setState(() {
                              loadingJson = true;
                            }),
                            fileData = await MyFile.loadFileContent(
                              fileInformation['fileName'],
                              fileInformation['fileContent'],
                              _selectedSet,
                            ),
                            setState(() {
                              loadingJson = false;
                            }),
                          },
                          child: const Text(
                            'Select File',
                            style: TextStyle(fontSize: 16),
                          ),
                        ),
                      ),
                      if (fileInformation['fileName'] != null) ...[
                        const SizedBox(width: 8),
                        Text(
                          fileInformation['fileName'].split('-').first,
                          style: const TextStyle(
                              fontSize: 16, color: Colors.white),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ],
                    ],
                  ),
                ),
                NavItem(
                  child: const Text('Monsters'),
                  onTap: () {
                    setState(() {
                      _selectedTab = 0;
                    });
                  },
                ),
                NavItem(
                  child: const Text('Runes'),
                  onTap: () {
                    setState(() {
                      _selectedTab = 1;
                    });
                  },
                ),
                NavItem(
                  child: const Text('Artifacts'),
                  onTap: () {
                    setState(() {
                      _selectedTab = 2;
                    });
                  },
                )
              ],
            ),
          ),
          Expanded(
            child: IndexedStack(
              alignment: Alignment.center,
              index: _selectedTab,
              children: [
                displayMonsters(fileData, loadingJson),
                displayRunes(fileData, loadingJson),
                ArtifactDisplay(loadingJson: loadingJson),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
