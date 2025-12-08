export enum GameStatus {
  IDLE = 'IDLE',
  PLAYING = 'PLAYING',
  GAME_OVER = 'GAME_OVER',
}

export interface Entity {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Garbage extends Entity {
  id: number;
  type: 'bottle' | 'bag' | 'can';
  rotation: number;
}

export interface GameState {
  status: GameStatus;
  distance: number; // in meters
  health: number; // 0 to 1
  highScore: number;
}

export interface PhysicsState {
  orcaY: number;
  orcaVelocity: number;
  isJumping: boolean;
  garbage: Garbage[];
  lastGarbageTime: number;
  gameSpeed: number;
  distanceOffset: number;
  invulnerabilityTimer: number;
}