import React, { useEffect, useRef, useState, useCallback } from 'react';
import { GameStatus, PhysicsState, Garbage } from '../types';
import { 
  GRAVITY, 
  JUMP_STRENGTH, 
  BASE_GAME_SPEED, 
  SEA_LEVEL_PERCENT, 
  ORCA_WIDTH, 
  ORCA_HEIGHT, 
  GARBAGE_SIZE,
  OrcaSvg,
  BottleSvg,
  BagSvg,
  CanSvg,
  DAMAGE_PER_HIT,
  METERS_PER_FRAME
} from '../constants';

interface GameLoopProps {
  status: GameStatus;
  onGameOver: (finalDistance: number) => void;
  onDistanceUpdate: (dist: number) => void;
  onHealthUpdate: (health: number) => void;
}

const GameLoop: React.FC<GameLoopProps> = ({ status, onGameOver, onDistanceUpdate, onHealthUpdate }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const requestRef = useRef<number>();
  
  // We use refs for high-frequency physics updates to avoid React render lag
  const physics = useRef<PhysicsState>({
    orcaY: 0,
    orcaVelocity: 0,
    isJumping: false,
    garbage: [],
    lastGarbageTime: 0,
    gameSpeed: BASE_GAME_SPEED,
    distanceOffset: 0,
    invulnerabilityTimer: 0,
  });

  // State for rendering positions (synced from physics ref via RAF)
  const [renderState, setRenderState] = useState<{
    orcaY: number;
    orcaRotation: number;
    garbage: Garbage[];
    isHit: boolean;
  }>({
    orcaY: 0,
    orcaRotation: 0,
    garbage: [],
    isHit: false,
  });

  // Initialize Physics on Mount/Restart
  useEffect(() => {
    if (status === GameStatus.PLAYING && containerRef.current) {
      const containerHeight = containerRef.current.clientHeight;
      const seaLevelY = containerHeight * SEA_LEVEL_PERCENT;
      
      physics.current = {
        orcaY: seaLevelY,
        orcaVelocity: 0,
        isJumping: false,
        garbage: [],
        lastGarbageTime: performance.now(),
        gameSpeed: BASE_GAME_SPEED,
        distanceOffset: 0,
        invulnerabilityTimer: 0,
      };
    }
  }, [status]);

  // The Main Loop
  const update = useCallback((time: number) => {
    if (status !== GameStatus.PLAYING || !containerRef.current) return;

    const p = physics.current;
    const containerHeight = containerRef.current.clientHeight;
    const containerWidth = containerRef.current.clientWidth;
    const seaLevelY = containerHeight * SEA_LEVEL_PERCENT;

    // 1. Update Distance
    p.distanceOffset += METERS_PER_FRAME * (p.gameSpeed / BASE_GAME_SPEED);
    onDistanceUpdate(p.distanceOffset);

    // 2. Physics (Orca)
    // Apply Gravity
    p.orcaVelocity += GRAVITY;
    p.orcaY += p.orcaVelocity;

    // Floor/Water Surface Collision
    if (p.orcaY >= seaLevelY) {
      p.orcaY = seaLevelY;
      p.isJumping = false;
      // If we are just swimming, dampen velocity
      if (p.orcaVelocity > 0) {
        p.orcaVelocity = 0; 
      }
    } else {
      p.isJumping = true;
    }

    // 3. Garbage Spawning
    // Spawn roughly every 1.5 - 3 seconds based on speed
    if (time - p.lastGarbageTime > 2000 - (p.gameSpeed * 50)) {
      if (Math.random() > 0.3) { // 70% chance to spawn
        p.garbage.push({
          id: time,
          x: containerWidth + 50, // Start off-screen right
          y: seaLevelY + 10, // Float ON the water
          width: GARBAGE_SIZE,
          height: GARBAGE_SIZE,
          type: Math.random() < 0.33 ? 'bottle' : Math.random() < 0.5 ? 'bag' : 'can',
          rotation: Math.random() * 360
        });
      }
      p.lastGarbageTime = time;
    }

    // 4. Garbage Movement & Cleanup
    p.garbage.forEach(g => {
      g.x -= p.gameSpeed;
      g.rotation += 1; // Spin slowly
    });
    // Remove off-screen garbage
    p.garbage = p.garbage.filter(g => g.x > -100);

    // 5. Collision Detection
    // Simple AABB (Axis-Aligned Bounding Box) but slightly forgiving
    if (p.invulnerabilityTimer <= 0) {
      const orcaBox = {
        x: 100 + 10, // Orca is fixed at x=100, +10 padding
        y: p.orcaY + 10,
        w: ORCA_WIDTH - 20,
        h: ORCA_HEIGHT - 10
      };

      for (const g of p.garbage) {
        const garbageBox = {
          x: g.x + 5,
          y: g.y + 5,
          w: g.width - 10,
          h: g.height - 10
        };

        if (
          orcaBox.x < garbageBox.x + garbageBox.w &&
          orcaBox.x + orcaBox.w > garbageBox.x &&
          orcaBox.y < garbageBox.y + garbageBox.h &&
          orcaBox.y + orcaBox.h > garbageBox.y
        ) {
          // HIT!
          onHealthUpdate(-DAMAGE_PER_HIT);
          p.invulnerabilityTimer = 60; // 60 frames (~1 sec)
          break; // Only one hit per frame
        }
      }
    } else {
      p.invulnerabilityTimer--;
    }

    // 6. Acceleration (Game gets harder)
    if (p.distanceOffset % 50 < 0.1) {
       p.gameSpeed = Math.min(p.gameSpeed + 0.005, 12);
    }

    // 7. Render State Sync
    // Calculate rotation based on velocity
    let rotation = 0;
    if (p.isJumping) {
      rotation = Math.min(Math.max(p.orcaVelocity * 2, -45), 45);
    }

    setRenderState({
      orcaY: p.orcaY,
      orcaRotation: rotation,
      garbage: [...p.garbage], // Create copy for React render
      isHit: p.invulnerabilityTimer > 0 && Math.floor(time / 100) % 2 === 0
    });

    requestRef.current = requestAnimationFrame(update);
  }, [status, onDistanceUpdate, onHealthUpdate]);

  // Start Loop
  useEffect(() => {
    requestRef.current = requestAnimationFrame(update);
    return () => {
      if (requestRef.current) cancelAnimationFrame(requestRef.current);
    };
  }, [update]);

  // Input Handler
  const handleJump = useCallback(() => {
    if (status === GameStatus.PLAYING && !physics.current.isJumping) {
      physics.current.orcaVelocity = -JUMP_STRENGTH;
      physics.current.isJumping = true;
    }
  }, [status]);

  // Mouse/Touch Listeners
  useEffect(() => {
    const handleInput = (e: Event) => {
      // Prevent default to stop double-firing on some touch devices or zooming
      // e.preventDefault(); 
      handleJump();
    };

    window.addEventListener('mousedown', handleInput);
    window.addEventListener('touchstart', handleInput);
    window.addEventListener('keydown', (e) => {
      if (e.code === 'Space' || e.code === 'ArrowUp') handleJump();
    });

    return () => {
      window.removeEventListener('mousedown', handleInput);
      window.removeEventListener('touchstart', handleInput);
      window.removeEventListener('keydown', () => {});
    };
  }, [handleJump]);


  return (
    <div 
      ref={containerRef}
      className="absolute inset-0 w-full h-full overflow-hidden select-none"
    >
      {/* Dynamic Renderings */}
      
      {/* Garbage */}
      {renderState.garbage.map(g => (
        <div
          key={g.id}
          className="absolute transform -translate-y-1/2"
          style={{
            left: `${g.x}px`,
            top: `${g.y}px`,
            width: `${g.width}px`,
            height: `${g.height}px`,
            transform: `translate(0, -50%) rotate(${g.rotation}deg)`
          }}
        >
          {g.type === 'bottle' && <BottleSvg />}
          {g.type === 'bag' && <BagSvg />}
          {g.type === 'can' && <CanSvg />}
        </div>
      ))}

      {/* Orca */}
      <div 
        className="absolute z-20 transition-transform will-change-transform"
        style={{
          left: '100px', // Fixed X position
          top: `${renderState.orcaY}px`,
          transform: `translate(0, -50%)`, // Center anchor
        }}
      >
        <OrcaSvg rotation={renderState.orcaRotation} isHit={renderState.isHit} />
      </div>

    </div>
  );
};

export default GameLoop;