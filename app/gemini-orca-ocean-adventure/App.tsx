import React, { useState, useEffect, useCallback } from 'react';
import GameLoop from './components/GameLoop';
import { GameStatus, GameState } from './types';
import { MAX_HEALTH, SEA_LEVEL_PERCENT } from './constants';
import { generateGameOverMessage } from './services/geminiService';

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>({
    status: GameStatus.IDLE,
    distance: 0,
    health: MAX_HEALTH,
    highScore: 0,
  });
  
  const [gameOverMsg, setGameOverMsg] = useState<string>('');
  const [isLoadingMsg, setIsLoadingMsg] = useState<boolean>(false);

  const startGame = () => {
    setGameState(prev => ({
      ...prev,
      status: GameStatus.PLAYING,
      distance: 0,
      health: MAX_HEALTH,
    }));
    setGameOverMsg('');
  };

  const handleDistanceUpdate = useCallback((addedDistance: number) => {
    setGameState(prev => ({
      ...prev,
      distance: addedDistance
    }));
  }, []);

  const handleHealthUpdate = useCallback((change: number) => {
    setGameState(prev => {
      const newHealth = Math.max(0, prev.health + change);
      
      if (newHealth <= 0 && prev.status === GameStatus.PLAYING) {
        // Trigger Game Over immediately
        return {
          ...prev,
          health: 0,
          status: GameStatus.GAME_OVER
        };
      }
      return {
        ...prev,
        health: newHealth
      };
    });
  }, []);

  // Handle Game Over Side Effects
  useEffect(() => {
    if (gameState.status === GameStatus.GAME_OVER && !gameOverMsg && !isLoadingMsg) {
      const fetchMessage = async () => {
        setIsLoadingMsg(true);
        const msg = await generateGameOverMessage(gameState.distance);
        setGameOverMsg(msg);
        setIsLoadingMsg(false);
        
        // Update high score
        setGameState(prev => ({
            ...prev,
            highScore: Math.max(prev.highScore, prev.distance)
        }));
      };
      fetchMessage();
    }
  }, [gameState.status, gameState.distance, gameOverMsg, isLoadingMsg]);


  return (
    <div className="relative w-full h-screen overflow-hidden bg-slate-900 font-sans">
      
      {/* --- BACKGROUND LAYERS --- */}
      
      {/* Sky */}
      <div className="absolute top-0 left-0 w-full h-[65%] bg-gradient-to-b from-sky-300 to-sky-100 overflow-hidden">
        {/* Sun */}
        <div className="absolute top-10 right-10 w-20 h-20 bg-yellow-300 rounded-full blur-md opacity-80 animate-pulse"></div>
        {/* Clouds - Animation via pure CSS or simple styles */}
        <div className="absolute top-20 left-0 animate-[moveRight_60s_linear_infinite] opacity-60">
           <Cloud />
        </div>
        <div className="absolute top-40 left-[50%] animate-[moveRight_45s_linear_infinite] opacity-40">
           <Cloud />
        </div>
      </div>

      {/* Sea - Starts at 65% height */}
      <div 
        className="absolute bottom-0 left-0 w-full h-[35%] bg-gradient-to-b from-blue-600 to-blue-900 z-10"
        style={{ borderTop: '4px solid #60a5fa' }} // Light blue surface line
      >
        {/* Wave effect overlay */}
        <div className="absolute top-0 left-0 w-full h-4 bg-white/20 blur-sm"></div>
      </div>

      {/* --- GAME LAYER --- */}
      <GameLoop 
        status={gameState.status}
        onGameOver={() => {}} // Handled via health update
        onDistanceUpdate={handleDistanceUpdate}
        onHealthUpdate={handleHealthUpdate}
      />

      {/* --- UI OVERLAY --- */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none z-30">
        
        {/* HUD */}
        <div className="absolute top-4 left-4 flex gap-4 text-slate-800 game-font">
          <div className="bg-white/80 backdrop-blur px-4 py-2 rounded-xl shadow-lg border border-sky-200">
            <span className="text-sm font-bold uppercase text-slate-500 mr-2">Health</span>
            <div className="flex gap-1 inline-block align-middle">
              {/* Render Hearts based on health steps of 0.5 */}
              {[...Array(2)].map((_, i) => (
                <Heart key={i} fill={gameState.health > i * 0.5} />
              ))}
            </div>
          </div>
          
          <div className="bg-white/80 backdrop-blur px-4 py-2 rounded-xl shadow-lg border border-sky-200">
            <span className="text-sm font-bold uppercase text-slate-500 mr-2">Distance</span>
            <span className="text-xl font-black text-sky-600">{gameState.distance.toFixed(1)}m</span>
          </div>
        </div>

        {/* START SCREEN */}
        {gameState.status === GameStatus.IDLE && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm pointer-events-auto">
            <div className="bg-white p-8 rounded-3xl shadow-2xl text-center max-w-md border-4 border-sky-300">
              <h1 className="text-4xl font-extrabold text-sky-600 mb-2 game-font">Orca's Adventure</h1>
              <p className="text-slate-600 mb-6">Tap or Click to Jump. Avoid the trash!</p>
              <button 
                onClick={startGame}
                className="bg-sky-500 hover:bg-sky-400 text-white text-xl font-bold py-3 px-8 rounded-full shadow-lg transition-transform transform hover:scale-105 active:scale-95"
              >
                Start Swimming
              </button>
            </div>
          </div>
        )}

        {/* GAME OVER SCREEN */}
        {gameState.status === GameStatus.GAME_OVER && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-sm pointer-events-auto">
            <div className="bg-white p-8 rounded-3xl shadow-2xl text-center max-w-md border-4 border-red-300 animate-in fade-in zoom-in duration-300">
              <h2 className="text-3xl font-black text-slate-800 mb-2 game-font">Oh no!</h2>
              <div className="text-5xl mb-4">😢</div>
              <p className="text-slate-500 font-semibold mb-2">You swam</p>
              <p className="text-4xl font-black text-sky-600 mb-6">{gameState.distance.toFixed(1)}m</p>
              
              <div className="bg-sky-50 p-4 rounded-xl mb-6 border border-sky-100">
                 {isLoadingMsg ? (
                   <span className="text-sky-400 animate-pulse">Consulting the ocean spirits...</span>
                 ) : (
                   <p className="text-slate-700 italic text-sm">"{gameOverMsg}"</p>
                 )}
              </div>

              <div className="flex justify-center gap-4">
                 <button 
                  onClick={startGame}
                  className="bg-sky-500 hover:bg-sky-400 text-white text-lg font-bold py-3 px-8 rounded-full shadow-lg transition-transform transform hover:scale-105"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Global CSS for Animations that Tailwind doesn't have natively for infinite loops */}
      <style>{`
        @keyframes moveRight {
          from { transform: translateX(-100px); }
          to { transform: translateX(100vw); }
        }
      `}</style>
    </div>
  );
};

// Simple UI Components for the overlay
const Heart: React.FC<{ fill: boolean }> = ({ fill }) => (
  <svg width="24" height="24" viewBox="0 0 24 24" className={fill ? "text-red-500" : "text-gray-300"}>
    <path fill="currentColor" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
  </svg>
);

const Cloud = () => (
  <svg width="100" height="60" viewBox="0 0 24 24" fill="white">
     <path d="M18.42 9.22A5.5 5.5 0 0 0 13.5 6a5.5 5.5 0 0 0-5.18 3.56A4.5 4.5 0 0 0 4.5 18h14.5a4 4 0 0 0-.58-8.78Z"/>
  </svg>
)

export default App;