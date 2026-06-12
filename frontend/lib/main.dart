import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/liveness_provider.dart';
import 'screens/camera_screen.dart';
import 'screens/challenge_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => LivenessProvider()),
      ],
      child: const ShieldApp(),
    ),
  );
}

class ShieldApp extends StatelessWidget {
  const ShieldApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SHIELD - Liveness Detection',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
        useMaterial3: true,
        scaffoldBackgroundColor: Colors.black,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _urlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _urlController.text = 'ws://192.168.1.100:8000/ws/verify'; // Example local IP
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<LivenessProvider>(context);

    return Scaffold(
      body: Container(
        padding: const EdgeInsets.all(24),
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Colors.black, Color(0xFF121212)],
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Icon(Icons.shield_rounded, size: 100, color: Colors.blue),
            const SizedBox(height: 24),
            const Text(
              'SHIELD',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 48,
                fontWeight: FontWeight.bold,
                letterSpacing: 4,
                color: Colors.white,
              ),
            ),
            const Text(
              'Secure Human Identity & Liveness Evaluation Detection',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white70, fontSize: 14),
            ),
            const SizedBox(height: 60),
            TextField(
              controller: _urlController,
              decoration: InputDecoration(
                labelText: 'Server WebSocket URL',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                prefixIcon: const Icon(Icons.link),
              ),
              onChanged: (value) => provider.setServerUrl(value),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: provider.isConnected 
                  ? () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const CameraScreen())
                    )
                  : () async {
                      await provider.connect(isChallenge: false);
                      if (provider.isConnected) {
                        if (mounted) {
                          Navigator.of(context).push(
                            MaterialPageRoute(builder: (_) => const CameraScreen())
                          );
                        }
                      } else {
                        if (mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Failed to connect to backend'))
                          );
                        }
                      }
                    },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                backgroundColor: provider.isConnected ? Colors.blue : Colors.blueGrey,
              ),
              child: Text(
                provider.isConnected ? 'Passive Liveness Check' : 'Connect (Passive)',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: provider.isConnected 
                  ? () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (_) => const ChallengeScreen())
                    )
                  : () async {
                      await provider.connect(isChallenge: true);
                      if (provider.isConnected) {
                        if (mounted) {
                          Navigator.of(context).push(
                            MaterialPageRoute(builder: (_) => const ChallengeScreen())
                          );
                        }
                      } else {
                        if (mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('Failed to connect to backend'))
                          );
                        }
                      }
                    },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                backgroundColor: provider.isConnected ? Colors.green : Colors.blueGrey,
              ),
              child: Text(
                provider.isConnected ? 'Active Challenge Verification' : 'Connect (Active Challenge)',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
