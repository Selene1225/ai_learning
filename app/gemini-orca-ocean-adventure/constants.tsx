import React from 'react';

// Physics & Game Config
export const GRAVITY = 0.6;
export const JUMP_STRENGTH = 12;
export const BASE_GAME_SPEED = 5;
export const SEA_LEVEL_PERCENT = 0.65; // Water starts at 65% down the screen
export const MAX_HEALTH = 1.0;
export const DAMAGE_PER_HIT = 0.5;
export const METERS_PER_FRAME = 0.05;

// Asset Sizes (relative or pixels depending on usage, here we assume pixels for calculation logic)
export const ORCA_WIDTH = 80;
export const ORCA_HEIGHT = 40;
export const GARBAGE_SIZE = 40;

// SVGs
export const OrcaSvg = ({ rotation, isHit }: { rotation: number; isHit: boolean }) => (
  <svg
    width="80"
    height="40"
    viewBox="0 0 100 50"
    className={`transition-transform duration-75 ${isHit ? 'opacity-50 animate-pulse' : ''}`}
    style={{ transform: `rotate(${rotation}deg)` }}
  >
    <path
      d="M10,25 Q30,5 60,15 T95,25 Q80,45 50,35 T10,25 Z"
      fill="#1e293b" // slate-800
      stroke="white"
      strokeWidth="2"
    />
    <circle cx="25" cy="20" r="3" fill="white" />
    <path d="M60,15 Q65,5 55,0 Q50,10 60,15" fill="#1e293b" />
    <path d="M30,30 Q40,40 20,40 Z" fill="white" />
  </svg>
);

export const BottleSvg = () => (
  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-green-600">
    <path d="M9 3h6v4l-2 2v10a2 2 0 01-2 2H9a2 2 0 01-2-2V9L5 7V3z" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const BagSvg = () => (
  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gray-400">
    <path d="M6 9l2-5h8l2 5v11a2 2 0 01-2 2H8a2 2 0 01-2-2V9z" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M10 14h4" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

export const CanSvg = () => (
  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-red-500">
    <path d="M7 6h10v13a2 2 0 01-2 2H9a2 2 0 01-2-2V6z" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M7 6a2 2 0 012-2h6a2 2 0 012 2" strokeLinecap="round" strokeLinejoin="round"/>
    <line x1="10" y1="10" x2="10" y2="16" />
    <line x1="14" y1="10" x2="14" y2="16" />
  </svg>
);