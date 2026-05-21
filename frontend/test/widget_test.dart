import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:shield_app/main.dart';
import 'package:shield_app/providers/liveness_provider.dart';

void main() {
  testWidgets('SHIELD App Smoke Test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => LivenessProvider()),
        ],
        child: const ShieldApp(),
      ),
    );

    // Verify that SHIELD title is present
    expect(find.text('SHIELD'), findsOneWidget);
    
    // Verify that the start button is present
    expect(find.text('Connect & Start'), findsOneWidget);
  });
}
