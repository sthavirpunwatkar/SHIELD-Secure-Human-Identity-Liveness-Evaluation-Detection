import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:shield_app/main.dart';
import 'package:shield_app/providers/liveness_provider.dart';
import 'package:shield_app/services/camera_capture_service.dart';
import 'package:shield_app/services/frame_transport_service.dart';
import 'package:shield_app/services/webcodecs_service.dart';
import 'package:shield_app/transport/current_websocket_transport.dart';

void main() {
  testWidgets('SHIELD App Smoke Test', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider<CameraCaptureService>(
            create: (_) => CameraCaptureService(),
          ),
          ChangeNotifierProxyProvider<CameraCaptureService, LivenessProvider>(
            create: (context) {
              final cameraService = Provider.of<CameraCaptureService>(context, listen: false);
              final encoder = WebCodecsService();
              final transport = CurrentWebSocketTransport(encoder);
              final transportService = FrameTransportService(cameraService, transport);
              return LivenessProvider(transportService);
            },
            update: (_, cameraService, previous) => previous ?? LivenessProvider(FrameTransportService(cameraService, CurrentWebSocketTransport(WebCodecsService()))),
          ),
        ],
        child: const ShieldApp(),
      ),
    );

    // Verify that SHIELD title is present
    expect(find.text('SHIELD'), findsOneWidget);
    
    // Verify that the connect buttons are present
    expect(find.text('Connect (Passive)'), findsOneWidget);
    expect(find.text('Connect (Active Challenge)'), findsOneWidget);
  });
}
