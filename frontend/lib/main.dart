import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:shield_app/l10n/app_localizations.dart';
import 'providers/liveness_provider.dart';
import 'screens/camera_screen.dart';
import 'screens/challenge_screen.dart';
import 'screens/pre_verification_screen.dart';

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
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en'),
        Locale('es'),
        Locale('fr'),
      ],
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
    _urlController.text = 'ws://localhost:8000/ws/verify'; // Example local IP
  }

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<LivenessProvider>(context);
    final l10n = AppLocalizations.of(context)!;

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
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.shield_rounded, size: 100, color: Colors.blue),
              const SizedBox(height: 24),
              Text(
                l10n.shieldTitle,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 48,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 4,
                  color: Colors.white,
                ),
              ),
              Text(
                l10n.shieldSubtitle,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white70, fontSize: 14),
              ),
              const SizedBox(height: 60),
              TextField(
                controller: _urlController,
                decoration: InputDecoration(
                  labelText: l10n.serverUrlLabel,
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
                              SnackBar(content: Text(l10n.failedConnect))
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
                  provider.isConnected ? l10n.passiveCheck : l10n.connectPassive,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: provider.isConnected 
                    ? () => Navigator.of(context).push(
                        MaterialPageRoute(builder: (_) => const PreVerificationScreen())
                      )
                    : () async {
                        await provider.connect(isChallenge: true);
                        if (provider.isConnected) {
                          if (mounted) {
                            Navigator.of(context).push(
                              MaterialPageRoute(builder: (_) => const PreVerificationScreen())
                            );
                          }
                        } else {
                          if (mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text(l10n.failedConnect))
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
                  provider.isConnected ? l10n.activeCheck : l10n.connectActive,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
