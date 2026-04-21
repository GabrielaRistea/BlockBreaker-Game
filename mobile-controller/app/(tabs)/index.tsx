import * as Haptics from 'expo-haptics';
import { useRef, useState } from 'react';
import { Alert, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { io, Socket } from 'socket.io-client';

export default function App() {
  const [ipAddress, setIpAddress] = useState<string>('192.168.1.104');
  const [isConnected, setIsConnected] = useState<boolean>(false);
  
  const socket = useRef<Socket | null>(null);

  const connectToServer = () => {
    if (!ipAddress) return;

    if (socket.current) {
      socket.current.disconnect();
    }
    
    socket.current = io(`http://${ipAddress}:8765`);

    socket.current.on('connect', () => {
      Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      setIsConnected(true);
    });

    socket.current.on('connect_error', () => {
      Alert.alert('Eroare', 'Nu m-am putut conecta. Verifică IP-ul și serverul de pe PC.');
      if (socket.current) socket.current.disconnect();
    });

    socket.current.on('disconnect', () => {
      setIsConnected(false);
    });
  };

  const sendCommand = (direction: 'left' | 'right' | 'none') => {
    if (socket.current && isConnected) {
      if (direction !== 'none') {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      }
      socket.current.emit('command', direction);
    }
  };

  const sendAction = () => {
    if (socket.current && isConnected) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
      socket.current.emit('action', true);
      
      setTimeout(() => {
        if (socket.current) socket.current.emit('action', false);
      }, 100);
    }
  };

  if (!isConnected) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>BlockBreaker Controller</Text>
        <Text style={styles.subtitle}>Introdu IP-ul PC-ului tău:</Text>
        <TextInput 
          style={styles.input}
          value={ipAddress}
          onChangeText={setIpAddress}
          keyboardType="numeric"
        />
        <TouchableOpacity style={styles.connectButton} onPress={connectToServer}>
          <Text style={styles.buttonText}>CONECTARE</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.gameContainer}>
      <Text style={styles.statusText}>🟢 Conectat la joc</Text>
      
      <TouchableOpacity style={styles.actionButton} onPress={sendAction}>
        <Text style={styles.buttonText}>LANSĂ MINGEA (↑)</Text>
      </TouchableOpacity>

      <View style={styles.controlsRow}>
        <TouchableOpacity 
          style={styles.directionButton}
          onPressIn={() => sendCommand('left')}
          onPressOut={() => sendCommand('none')}
        >
          <Text style={styles.arrowText}>←</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.directionButton}
          onPressIn={() => sendCommand('right')}
          onPressOut={() => sendCommand('none')}
        >
          <Text style={styles.arrowText}>→</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1e1e1e', alignItems: 'center', justifyContent: 'center', padding: 20 },
  gameContainer: { flex: 1, backgroundColor: '#121212', alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 28, color: '#fff', fontWeight: 'bold', marginBottom: 20 },
  subtitle: { fontSize: 16, color: '#aaa', marginBottom: 10 },
  input: { width: '80%', height: 50, backgroundColor: '#333', color: '#fff', fontSize: 20, textAlign: 'center', borderRadius: 10, marginBottom: 20 },
  connectButton: { backgroundColor: '#4CAF50', paddingVertical: 15, paddingHorizontal: 40, borderRadius: 10 },
  buttonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  statusText: { color: '#4CAF50', fontSize: 16, position: 'absolute', top: 50 },
  actionButton: { backgroundColor: '#FF9800', width: '80%', paddingVertical: 20, borderRadius: 15, alignItems: 'center', marginBottom: 40 },
  controlsRow: { flexDirection: 'row', width: '90%', justifyContent: 'space-between' },
  directionButton: { backgroundColor: '#2196F3', width: '45%', height: 120, borderRadius: 20, alignItems: 'center', justifyContent: 'center' },
  arrowText: { fontSize: 50, color: '#fff', fontWeight: 'bold' }
});