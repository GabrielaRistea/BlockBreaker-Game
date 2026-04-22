import * as Haptics from 'expo-haptics';
import { useEffect, useRef, useState } from 'react';
import { ActivityIndicator, Alert, Animated, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';

export default function App() {
  const [ipAddress, setIpAddress] = useState<string>('10.2.13.140');
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  const [score, setScore] = useState<number>(0);
  const [lives, setLives] = useState<number>(3);
  const [gameState, setGameState] = useState<string>('MENU');

  const ws = useRef<WebSocket | null>(null);

  const scaleAnim = useRef(new Animated.Value(1)).current; 
  const shakeAnim = useRef(new Animated.Value(0)).current; 
  const prevScore = useRef(score);
  const prevLives = useRef(lives);

  useEffect(() => {
    if (score > prevScore.current) {
      Animated.sequence([
        Animated.timing(scaleAnim, { toValue: 1.5, duration: 100, useNativeDriver: true }),
        Animated.timing(scaleAnim, { toValue: 1, duration: 200, useNativeDriver: true })
      ]).start();
    }
    prevScore.current = score;
  }, [score]);

  useEffect(() => {
    if (lives < prevLives.current) {
      Animated.sequence([
        Animated.timing(shakeAnim, { toValue: 15, duration: 50, useNativeDriver: true }),
        Animated.timing(shakeAnim, { toValue: -15, duration: 50, useNativeDriver: true }),
        Animated.timing(shakeAnim, { toValue: 15, duration: 50, useNativeDriver: true }),
        Animated.timing(shakeAnim, { toValue: 0, duration: 50, useNativeDriver: true })
      ]).start();
    }
    prevLives.current = lives;
  }, [lives]);

  const connectToServer = () => {
    if (!ipAddress || isLoading) return;
    setIsLoading(true);

    if (ws.current) ws.current.close();
    
    ws.current = new WebSocket(`ws://${ipAddress}:8765`);

    const connectionTimeout = setTimeout(() => {
      if (ws.current && ws.current.readyState !== WebSocket.OPEN) {
        ws.current.close();
        setIsLoading(false);
        Alert.alert('Eroare', 'Timpul a expirat. Verifică IP-ul!');
      }
    }, 4000);

    ws.current.onopen = () => {
      clearTimeout(connectionTimeout);
      try { Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success); } catch(e){}
      setIsConnected(true);
      setIsLoading(false);
    };

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'update_data') {
          setScore(data.score);
          setLives(data.lives);
          if (data.state) setGameState(data.state);
        } else if (data.type === 'vibrate') {
          const type = data.value;
          try {
            if (type === 'light') Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            else if (type === 'medium') Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
            else if (type === 'heavy') Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
            else if (type === 'success') Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
          } catch(e) {}
        }
      } catch (e) {
        console.log("Eroare parsare:", e);
      }
    };

    ws.current.onerror = () => {
      clearTimeout(connectionTimeout);
      setIsLoading(false);
      setIsConnected(false);
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      setIsLoading(false);
    };
  };

  const sendCommand = (direction: 'left' | 'right' | 'none') => {
    if (ws.current && isConnected) {
      if (direction !== 'none') {
        try { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light); } catch(e){}
      }
      ws.current.send(JSON.stringify({ type: 'command', value: direction }));
    }
  };

  const sendAction = () => {
    if (ws.current && isConnected) {
      try { Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy); } catch(e){}
      ws.current.send(JSON.stringify({ type: 'action', value: true }));
      setTimeout(() => {
        if (ws.current) ws.current.send(JSON.stringify({ type: 'action', value: false }));
      }, 100);
    }
  };

  const requestExtraLife = () => {
    if (ws.current && isConnected) {
      try { Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success); } catch(e){}
      ws.current.send(JSON.stringify({ type: 'add_life' }));
    }
  };

  const sendStartGame = () => {
    if (ws.current && isConnected) {
      try { Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success); } catch(e){}
      ws.current.send(JSON.stringify({ type: 'start_game' }));
    }
  };

  if (!isConnected) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>BlockBreaker Controller</Text>
        <Text style={styles.subtitle}>Enter PC IP address:</Text>
        <TextInput style={styles.input} value={ipAddress} onChangeText={setIpAddress} keyboardType="numeric" />
        <TouchableOpacity style={[styles.connectButton, isLoading && { backgroundColor: '#888' }]} onPress={connectToServer} disabled={isLoading}>
          {isLoading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>CONNECT</Text>}
        </TouchableOpacity>
      </View>
    );
  }

  const renderHeader = () => (
    <View style={styles.header}>
      <Text style={styles.statusText}>🟢 Connected</Text>
      <View style={styles.statsRow}>
        {}
        <Animated.Text style={[styles.statText, { transform: [{ scale: scaleAnim }] }]}>
          🏆 {score}
        </Animated.Text>
        <Text style={styles.statText}>❤️ {lives}</Text>
      </View>
    </View>
  );

  if (gameState === 'GAME' || gameState === 'PAUSE') {
    return (
      <Animated.View style={[styles.gameContainer, { transform: [{ translateX: shakeAnim }] }]}>
        {renderHeader()}
        
        <View style={styles.centerGroup}>
          <TouchableOpacity style={styles.actionButton} onPress={sendAction}>
            <Text style={styles.buttonText}>THROW BALL (↑)</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.controlsRow}>
          <TouchableOpacity style={styles.directionButton} onPressIn={() => sendCommand('left')} onPressOut={() => sendCommand('none')}>
            <Text style={styles.arrowText}>←</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.directionButton} onPressIn={() => sendCommand('right')} onPressOut={() => sendCommand('none')}>
            <Text style={styles.arrowText}>→</Text>
          </TouchableOpacity>
        </View>
      </Animated.View>
    );
  }

  return (
    <Animated.View style={[styles.gameContainer, { transform: [{ translateX: shakeAnim }] }]}>
      {renderHeader()}
      
      <View style={[styles.centerGroup, { flex: 1, justifyContent: 'center', marginBottom: 100 }]}>
        {gameState === 'MENU' && (
          <Text style={styles.waitingText}>Waiting for game...</Text>
        )}

        {(gameState === 'GAMEOVER' || gameState === 'INPUT_NAME') && (
          <TouchableOpacity style={[styles.lifeButton, { marginBottom: 30, width: '70%', paddingVertical: 20 }]} onPress={requestExtraLife}>
            <Text style={styles.buttonText}>+1 LIFE ❤️</Text>
          </TouchableOpacity>
        )}

        <TouchableOpacity style={[styles.actionButton, {backgroundColor: '#4CAF50'}]} onPress={sendStartGame}>
          <Text style={styles.buttonText}>▶️ START GAME</Text>
        </TouchableOpacity>
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1e1e1e', alignItems: 'center', justifyContent: 'center', padding: 20 },
  gameContainer: { flex: 1, backgroundColor: '#121212', alignItems: 'center', justifyContent: 'flex-start' },
  title: { fontSize: 28, color: '#fff', fontWeight: 'bold', marginBottom: 20 },
  subtitle: { fontSize: 16, color: '#aaa', marginBottom: 10 },
  input: { width: '80%', height: 50, backgroundColor: '#333', color: '#fff', fontSize: 20, textAlign: 'center', borderRadius: 10, marginBottom: 20 },
  connectButton: { backgroundColor: '#4CAF50', paddingVertical: 15, paddingHorizontal: 40, borderRadius: 10 },
  buttonText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  waitingText: { color: '#aaa', fontSize: 20, fontStyle: 'italic', marginBottom: 30 },
  header: { width: '100%', alignItems: 'center', marginTop: 50 },
  statusText: { color: '#4CAF50', fontSize: 16, position: 'absolute', top: -30 },
  statsRow: { flexDirection: 'row', justifyContent: 'space-around', width: '80%', backgroundColor: '#222', padding: 15, borderRadius: 15, marginTop: 20 },
  statText: { color: '#fff', fontSize: 22, fontWeight: 'bold' },
  centerGroup: { width: '100%', alignItems: 'center', marginVertical: 40 },
  lifeButton: { backgroundColor: '#E91E63', width: '50%', paddingVertical: 12, borderRadius: 12, alignItems: 'center' },
  actionButton: { backgroundColor: '#FF9800', width: '80%', paddingVertical: 20, borderRadius: 15, alignItems: 'center' },
  controlsRow: { flexDirection: 'row', width: '90%', justifyContent: 'space-between', marginTop: 'auto', marginBottom: 40 },
  directionButton: { backgroundColor: '#2196F3', width: '45%', height: 120, borderRadius: 20, alignItems: 'center', justifyContent: 'center' },
  arrowText: { fontSize: 50, color: '#fff', fontWeight: 'bold' }
});