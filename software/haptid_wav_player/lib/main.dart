import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HapTID WAV Player',
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2E45ED),
          background: const Color(0xFF04071B),
        ),
        textTheme: const TextTheme(
          titleLarge: TextStyle(
            fontSize: 56,
          ),
          titleMedium: TextStyle(
            fontSize: 36,
            fontWeight: FontWeight.bold,
          ),
          titleSmall: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
          bodyMedium: TextStyle(
            fontSize: 18,
          ),
          bodySmall: TextStyle(
            fontSize: 14,
          ),
          displayLarge: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
          displayMedium: TextStyle(
            fontSize: 14,
          ),
        ).apply(
          bodyColor: const Color(0xFFF4EFDC),
          displayColor: const Color(0xFFF4EFDC),
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(
            borderSide: BorderSide(color: Color(0xFF2E45ED), width: 2),
          ),
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Color(0xFF2E45ED), width: 2),
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Color(0xFF2E45ED), width: 2),
          ),
        ),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.max,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text('HapTID',
                style: TextStyle(
                  fontSize: 56,
                  fontWeight: FontWeight.w900,
                  fontStyle: FontStyle.italic,
                  color: Theme.of(context).colorScheme.primary,
                )),
            Center(
              child: SizedBox(
                width: MediaQuery.of(context).size.width * 0.3,
                child: Column(
                  children: <Widget>[
                    Text(
                      'WAV Player',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const Row(
                      children: [
                        Flexible(
                          flex: 1,
                          child: Padding(
                            padding: EdgeInsets.all(5),
                            child: TextField(
                              decoration: InputDecoration(
                                labelText: 'COM Port',
                                hintText: 'COM Port',
                              ),
                            ),
                          ),
                        ),
                        Flexible(
                          flex: 2,
                          child: Padding(
                            padding: EdgeInsets.all(5),
                            child: TextField(
                              decoration: InputDecoration(
                                labelText: 'Baud Rate',
                                hintText: 'Baud Rate',
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {},
                      child: const Text('Connect'),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
