const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const healthDisplay = document.getElementById("healthDisplay");
const scoreDisplay = document.getElementById("scoreDisplay");
const timeDisplay = document.getElementById("timeDisplay");
const levelDisplay = document.getElementById("levelDisplay");

const gameOverlay = document.getElementById("gameOverlay");
const startBtn = document.getElementById("startBtn");

const keys = {};

let gameRunning = false;
let animationId = null;
let lastTime = 0;
let enemySpawnTimer = 0;
let attackTimer = 0;
let gameTime = 0;

const player = {
  x: canvas.width / 2,
  y: canvas.height / 2,
  radius: 16,
  speed: 230,
  health: 100
};

let enemies = [];
let projectiles = [];
let score = 0;
let level = 1;

function resetGame() {
  player.x = canvas.width / 2;
  player.y = canvas.height / 2;
  player.health = 100;

  enemies = [];
  projectiles = [];
  score = 0;
  level = 1;
  gameTime = 0;
  enemySpawnTimer = 0;
  attackTimer = 0;
  lastTime = performance.now();

  updateUI();
}

function updateUI() {
  healthDisplay.textContent = Math.max(0, Math.round(player.health));
  scoreDisplay.textContent = score;
  timeDisplay.textContent = `${Math.floor(gameTime)}s`;
  levelDisplay.textContent = level;
}

function startGame() {
  resetGame();
  gameRunning = true;
  gameOverlay.classList.add("hidden");
  animationId = requestAnimationFrame(gameLoop);
}

function endGame() {
  gameRunning = false;
  cancelAnimationFrame(animationId);

  gameOverlay.classList.remove("hidden");
  gameOverlay.innerHTML = `
    <div>
      <h2>Game Over</h2>
      <p>You survived ${Math.floor(gameTime)} seconds and scored ${score} points.</p>
      <button id="restartBtn">Restart Game</button>
    </div>
  `;

  document.getElementById("restartBtn").addEventListener("click", startGame);
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function distance(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;

  return Math.sqrt(dx * dx + dy * dy);
}

function spawnEnemy() {
  const side = Math.floor(Math.random() * 4);
  let x;
  let y;

  if (side === 0) {
    x = Math.random() * canvas.width;
    y = -20;
  } else if (side === 1) {
    x = canvas.width + 20;
    y = Math.random() * canvas.height;
  } else if (side === 2) {
    x = Math.random() * canvas.width;
    y = canvas.height + 20;
  } else {
    x = -20;
    y = Math.random() * canvas.height;
  }

  enemies.push({
    x,
    y,
    radius: 14,
    speed: 70 + level * 8,
    health: 2 + Math.floor(level / 2)
  });
}

function autoAttack() {
  if (enemies.length === 0) return;

  const nearestEnemy = enemies.reduce((nearest, enemy) => {
    if (!nearest) return enemy;

    return distance(player, enemy) < distance(player, nearest) ? enemy : nearest;
  }, null);

  const dx = nearestEnemy.x - player.x;
  const dy = nearestEnemy.y - player.y;
  const length = Math.sqrt(dx * dx + dy * dy) || 1;

  projectiles.push({
    x: player.x,
    y: player.y,
    radius: 6,
    speed: 420,
    damage: 1,
    vx: dx / length,
    vy: dy / length,
    life: 1.6
  });
}

function updatePlayer(deltaTime) {
  let moveX = 0;
  let moveY = 0;

  if (keys.ArrowUp || keys.w) moveY -= 1;
  if (keys.ArrowDown || keys.s) moveY += 1;
  if (keys.ArrowLeft || keys.a) moveX -= 1;
  if (keys.ArrowRight || keys.d) moveX += 1;

  const length = Math.sqrt(moveX * moveX + moveY * moveY) || 1;

  player.x += (moveX / length) * player.speed * deltaTime;
  player.y += (moveY / length) * player.speed * deltaTime;

  player.x = clamp(player.x, player.radius, canvas.width - player.radius);
  player.y = clamp(player.y, player.radius, canvas.height - player.radius);
}

function updateEnemies(deltaTime) {
  enemies.forEach((enemy) => {
    const dx = player.x - enemy.x;
    const dy = player.y - enemy.y;
    const length = Math.sqrt(dx * dx + dy * dy) || 1;

    enemy.x += (dx / length) * enemy.speed * deltaTime;
    enemy.y += (dy / length) * enemy.speed * deltaTime;

    if (distance(player, enemy) < player.radius + enemy.radius) {
      player.health -= 22 * deltaTime;
    }
  });
}

function updateProjectiles(deltaTime) {
  projectiles.forEach((projectile) => {
    projectile.x += projectile.vx * projectile.speed * deltaTime;
    projectile.y += projectile.vy * projectile.speed * deltaTime;
    projectile.life -= deltaTime;
  });

  projectiles = projectiles.filter((projectile) => {
    return (
      projectile.life > 0 &&
      projectile.x > -50 &&
      projectile.x < canvas.width + 50 &&
      projectile.y > -50 &&
      projectile.y < canvas.height + 50
    );
  });
}

function handleCollisions() {
  projectiles.forEach((projectile) => {
    enemies.forEach((enemy) => {
      if (distance(projectile, enemy) < projectile.radius + enemy.radius) {
        enemy.health -= projectile.damage;
        projectile.life = 0;
      }
    });
  });

  const enemiesBefore = enemies.length;

  enemies = enemies.filter((enemy) => enemy.health > 0);

  const defeatedEnemies = enemiesBefore - enemies.length;

  if (defeatedEnemies > 0) {
    score += defeatedEnemies * 10;
  }

  projectiles = projectiles.filter((projectile) => projectile.life > 0);
}

function updateLevel() {
  level = 1 + Math.floor(gameTime / 20);
}

function drawBackground() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function drawPlayer() {
  ctx.beginPath();
  ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
  ctx.fillStyle = "#10b981";
  ctx.fill();

  ctx.beginPath();
  ctx.arc(player.x, player.y, player.radius + 5, 0, Math.PI * 2);
  ctx.strokeStyle = "rgba(16, 185, 129, 0.35)";
  ctx.lineWidth = 3;
  ctx.stroke();
}

function drawEnemies() {
  enemies.forEach((enemy) => {
    ctx.beginPath();
    ctx.arc(enemy.x, enemy.y, enemy.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#fb7185";
    ctx.fill();

    ctx.beginPath();
    ctx.arc(enemy.x - 4, enemy.y - 4, 3, 0, Math.PI * 2);
    ctx.fillStyle = "#0f1117";
    ctx.fill();
  });
}

function drawProjectiles() {
  projectiles.forEach((projectile) => {
    ctx.beginPath();
    ctx.arc(projectile.x, projectile.y, projectile.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.fill();
  });
}

function draw() {
  drawBackground();
  drawProjectiles();
  drawEnemies();
  drawPlayer();
}

function gameLoop(currentTime) {
  if (!gameRunning) return;

  const deltaTime = (currentTime - lastTime) / 1000;
  lastTime = currentTime;

  gameTime += deltaTime;
  enemySpawnTimer += deltaTime;
  attackTimer += deltaTime;

  updateLevel();

  const spawnRate = Math.max(0.35, 1.25 - level * 0.08);

  if (enemySpawnTimer >= spawnRate) {
    spawnEnemy();
    enemySpawnTimer = 0;
  }

  if (attackTimer >= 0.85) {
    autoAttack();
    attackTimer = 0;
  }

  updatePlayer(deltaTime);
  updateEnemies(deltaTime);
  updateProjectiles(deltaTime);
  handleCollisions();
  updateUI();
  draw();

  if (player.health <= 0) {
    endGame();
    return;
  }

  animationId = requestAnimationFrame(gameLoop);
}

window.addEventListener("keydown", (event) => {
  keys[event.key] = true;
});

window.addEventListener("keyup", (event) => {
  keys[event.key] = false;
});

startBtn.addEventListener("click", startGame);

draw();