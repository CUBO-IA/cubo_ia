"""Estado de juego: coordina nivel, jugador, enemigos, objetos, cámara y HUD.

Las reglas de movimiento viven en systems/ y en cada entidad;
aquí solo se decide QUÉ pasa cuando las cosas interactúan.
"""

import pygame

from src.settings import (
    WIDTH,
    HEIGHT,
    TILE,
    DEATH_Y,
    LEVEL_TIME,
    FPS,
    COINS_FOR_LIFE,
    SCORE_COIN,
    SCORE_STOMP,
    SCORE_BRICK,
    SCORE_CRYSTAL,
    SCORE_TIME_BONUS,
    STOMP_BOUNCE,
    STOMP_BOUNCE_HELD,
    ENEMY_ACTIVATE_MARGIN,
    THEMES,
    OVERLAY_COLOR,
    HIGHLIGHT_COLOR,
)
from src.states.base import State, font
from src.entities.player import Player, Controls, JUMP_KEYS
from src.entities.item import Crystal, CoinPop, Debris, ScorePopup
from src.entities.platform import Tile
from src.systems.camera import Camera
from src.systems.hud import HUD
from src.systems.background import Background
from src.levels import LEVELS
from src.levels.loader import Level


class PlayState(State):
    def __init__(self, game):
        super().__init__(game)

        self.session = game.session
        self.audio = game.audio

        self.level = Level(LEVELS[self.session.level_index]())
        self.player = Player(*self.level.start, big=self.session.player_big)
        self.player.transform_timer = 0

        self.camera = Camera(self.level.width)
        self.background = Background(self.level.theme)
        self.hud = HUD()
        self.controls = Controls()

        self.crystals = []
        self.effects = []
        self.bumping = []

        self.frame = 0
        self.time_left = LEVEL_TIME
        self.time_frames = 0

        self.phase = "playing"          # playing | dying | clear
        self.phase_timer = 0
        self.paused = False
        self.stomp_combo = 0
        self._jump_pressed = False
        self.clear_done_at = None

        self.big_font = font(64)
        self.small_font = font(32)

        self.audio.play_music(THEMES[self.level.theme]["music"])

    # -----------------------------------------------------------
    # Eventos
    # -----------------------------------------------------------
    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key in JUMP_KEYS:
            self._jump_pressed = True

        elif event.key in (pygame.K_p, pygame.K_RETURN) and self.phase == "playing":
            self.paused = not self.paused
            self.audio.play("pause")
            self.audio.pause_music(self.paused)

        elif event.key == pygame.K_ESCAPE:
            self.audio.stop_music()
            self.next_state = "menu"

    # -----------------------------------------------------------
    # Actualización
    # -----------------------------------------------------------
    def update(self):
        if self.paused:
            self._jump_pressed = False
            return

        self.frame += 1

        if self.phase == "clear":
            self._update_clear()
            return

        # Crecer/encoger congela el mundo unos instantes
        if self.player.transform_timer > 0:
            self.player.transform_timer -= 1
            self._jump_pressed = False
            return

        self.controls.read_keyboard()
        self.controls.jump_pressed = self._jump_pressed
        self._jump_pressed = False

        for platform in self.level.moving_platforms:
            platform.update()

        for tile in self.bumping[:]:
            tile.update()
            if tile.bump_timer == 0:
                self.bumping.remove(tile)

        prev_bottom = self.player.rect.bottom
        result = self.player.update(self.controls, self.level)

        if self.phase == "playing":
            self._keep_player_in_bounds()

            if result is not None:
                if self.player.on_ground:
                    self.stomp_combo = 0

                block = self._pick_head_block(result.head_hits)
                if block is not None:
                    self._hit_block(block)

            self._update_coins()
            self._update_crystals()
            self._update_enemies(prev_bottom)
            self._check_door()
            self._update_timer()

            if self.player.rect.top > DEATH_Y and not self.player.dead:
                self.player.die()
                self.player.velocity_y = 0

            if self.player.dead:
                self.phase = "dying"
                self.phase_timer = 0
                self.audio.stop_music()

        elif self.phase == "dying":
            self._update_enemies(prev_bottom, interact=False)
            self.phase_timer += 1

            if self.phase_timer > 170:
                self._lose_life()

        for effect in self.effects[:]:
            effect.update()
            if effect.done:
                self.effects.remove(effect)

        if not self.player.dead:
            self.camera.update(self.player)

        self._play_player_sounds()

    # -----------------------------------------------------------
    def _keep_player_in_bounds(self):
        rect = self.player.rect
        left_limit = self.camera.left
        right_limit = self.level.width

        if rect.left < left_limit:
            rect.left = left_limit
            self.player.velocity_x = max(0, self.player.velocity_x)
            self.player.pos_x = float(rect.x)

        elif rect.right > right_limit:
            rect.right = right_limit
            self.player.velocity_x = min(0, self.player.velocity_x)
            self.player.pos_x = float(rect.x)

    def _play_player_sounds(self):
        for name in self.player.events:
            self.audio.play(name)
        self.player.events.clear()

    # -----------------------------------------------------------
    # Bloques
    # -----------------------------------------------------------
    def _pick_head_block(self, hits):
        """Si la cabeza toca dos bloques, se golpea el más centrado."""
        best, best_overlap = None, 0

        for solid in hits:
            if not isinstance(solid, Tile):
                continue

            overlap = min(self.player.rect.right, solid.rect.right) - max(
                self.player.rect.left, solid.rect.left
            )

            if overlap > best_overlap:
                best, best_overlap = solid, overlap

        return best

    def _hit_block(self, tile):
        if tile.kind == "bonus":
            self._bump(tile)

            if tile.content == "crystal":
                self.crystals.append(Crystal(tile.rect))
                self.audio.play("powerup_appear")
                tile.kind = "used"

            else:
                self.effects.append(CoinPop(tile.rect))
                self._add_coin(tile.rect.centerx, tile.rect.top - 20)

                if tile.content == "multi":
                    tile.multi_left -= 1
                    if tile.multi_left <= 0:
                        tile.kind = "used"
                else:
                    tile.kind = "used"

        elif tile.kind == "brick":
            if self.player.big:
                self._break_brick(tile)
            else:
                self._bump(tile)
                self.audio.play("bump")

        else:
            self.audio.play("bump")

    def _bump(self, tile):
        tile.bump()
        if tile not in self.bumping:
            self.bumping.append(tile)

        # Los enemigos y monedas encima del bloque reciben el golpe
        above = pygame.Rect(tile.rect.x, tile.rect.y - 4, TILE, 6)

        for enemy in self.level.enemies:
            if enemy.harmful and enemy.rect.colliderect(above):
                direction = 1 if enemy.rect.centerx >= tile.rect.centerx else -1
                enemy.knock(direction)
                self._add_score(SCORE_STOMP, enemy.rect.centerx, enemy.rect.top)
                self.audio.play("stomp")

        for coin in self.level.coins:
            if not coin.collected and coin.rect.colliderect(above.inflate(0, TILE)):
                coin.collected = True
                self.effects.append(CoinPop(tile.rect.move(0, -TILE)))
                self._add_coin(coin.rect.centerx, coin.rect.top)

    def _break_brick(self, tile):
        self.level.remove_tile(tile)
        self.audio.play("break")
        self._add_score(SCORE_BRICK)

        cx, cy = tile.rect.center
        for vx, vy in ((-2.5, -9), (2.5, -9), (-2, -6), (2, -6)):
            self.effects.append(Debris(cx - 6, cy - 6, vx, vy))

        self._bump(tile)   # golpea lo que hubiera encima
        if tile in self.bumping:
            self.bumping.remove(tile)

    # -----------------------------------------------------------
    # Monedas, cristales, enemigos, meta
    # -----------------------------------------------------------
    def _add_score(self, points, x=None, y=None):
        self.session.score += points

        if x is not None:
            self.effects.append(ScorePopup(x, y, str(points)))

    def _add_coin(self, x=None, y=None):
        self.session.coins += 1
        self._add_score(SCORE_COIN)
        self.audio.play("coin")

        if self.session.coins >= COINS_FOR_LIFE:
            self.session.coins -= COINS_FOR_LIFE
            self.session.lives += 1
            self.audio.play("one_up")
            if x is not None:
                self.effects.append(ScorePopup(x, y - 20, "1UP"))

    def _update_coins(self):
        for coin in self.level.coins:
            if not coin.collected and coin.rect.colliderect(self.player.rect):
                coin.collected = True
                self._add_coin()

    def _update_crystals(self):
        for crystal in self.crystals[:]:
            crystal.update(self.level)

            if crystal.removed:
                self.crystals.remove(crystal)
                continue

            if not crystal.emerging and crystal.rect.colliderect(self.player.rect):
                self.crystals.remove(crystal)
                self._add_score(SCORE_CRYSTAL, crystal.rect.centerx, crystal.rect.top)
                self.audio.play("powerup")

                if not self.player.big:
                    self.player.set_big(True)

    def _update_enemies(self, prev_bottom, interact=True):
        for enemy in self.level.enemies:
            if not enemy.active and self.camera.is_visible(enemy.rect, ENEMY_ACTIVATE_MARGIN):
                enemy.active = True

            enemy.update(self.level)

        self.level.enemies = [e for e in self.level.enemies if not e.removed]

        if not interact or self.player.dead:
            return

        for enemy in self.level.enemies:
            if not enemy.harmful or not enemy.rect.colliderect(self.player.rect):
                continue

            from_above = prev_bottom <= enemy.rect.top + 8 and self.player.velocity_y >= 0

            if from_above and enemy.stompable:
                enemy.stomp()
                self.stomp_combo += 1
                points = SCORE_STOMP * (2 ** min(self.stomp_combo - 1, 4))
                self._add_score(points, enemy.rect.centerx, enemy.rect.top)
                self.audio.play("stomp")

                bounce = STOMP_BOUNCE_HELD if self.controls.jump_held else STOMP_BOUNCE
                self.player.bounce(bounce)
            else:
                self.player.hurt()

    def _check_door(self):
        door = self.level.door
        if door is not None and self.player.rect.colliderect(door.trigger):
            self.phase = "clear"
            self.phase_timer = 0
            self.audio.stop_music()
            self.audio.play("level_clear")

    def _update_timer(self):
        self.time_frames += 1

        if self.time_frames >= FPS:
            self.time_frames = 0
            self.time_left -= 1

            if self.time_left <= 0:
                self.time_left = 0
                self.player.die()

    # -----------------------------------------------------------
    # Fin de nivel / muerte
    # -----------------------------------------------------------
    def _update_clear(self):
        self.phase_timer += 1

        # Primero una pausa, luego el tiempo restante se convierte en puntos
        if self.phase_timer > 60 and self.time_left > 0:
            step = min(self.time_left, 2)
            self.time_left -= step
            self.session.score += step * SCORE_TIME_BONUS
            if self.phase_timer % 4 == 0:
                self.audio.play("coin")
            return

        if self.phase_timer > 60 and self.time_left == 0:
            if self.clear_done_at is None:
                self.clear_done_at = self.phase_timer

            if self.phase_timer - self.clear_done_at > 90:
                self.session.player_big = self.player.big
                self.session.level_index += 1

                if self.session.level_index >= self.session.level_count:
                    self.next_state = "victory"
                else:
                    self.next_state = "level_intro"

    def _lose_life(self):
        self.session.lives -= 1
        self.session.player_big = False

        if self.session.lives <= 0:
            self.next_state = "game_over"
        else:
            self.next_state = "level_intro"

    # -----------------------------------------------------------
    # Dibujo
    # -----------------------------------------------------------
    def draw(self, screen):
        self.background.draw(screen, self.camera.offset_x)

        # Cristales saliendo: detrás de los bloques
        for crystal in self.crystals:
            if crystal.emerging:
                crystal.draw(screen, self.camera, self.frame)

        if self.level.door is not None:
            self.level.door.draw(screen, self.camera, self.frame)

        for tile in self.level.visible_tiles(self.camera):
            tile.draw(screen, self.camera, self.frame)

        for platform in self.level.moving_platforms:
            if self.camera.is_visible(platform.rect):
                platform.draw(screen, self.camera, self.frame)

        for coin in self.level.coins:
            if self.camera.is_visible(coin.rect):
                coin.draw(screen, self.camera, self.frame)

        for crystal in self.crystals:
            if not crystal.emerging:
                crystal.draw(screen, self.camera, self.frame)

        for enemy in self.level.enemies:
            if self.camera.is_visible(enemy.rect, 40):
                enemy.draw(screen, self.camera)

        if not (self.phase == "clear" and self.phase_timer > 30):
            self.player.draw(screen, self.camera)

        for effect in self.effects:
            effect.draw(screen, self.camera, self.frame)

        self.hud.draw(screen, self.session, f"{self.level.name}", self.time_left)

        if self.paused:
            self._overlay(screen, "PAUSA", "P / ENTER - Continuar    ESC - Menú")

        elif self.phase == "clear" and self.phase_timer > 30:
            self.draw_text(screen, self.big_font, "¡NIVEL COMPLETADO!", (WIDTH // 2, HEIGHT // 2 - 30), HIGHLIGHT_COLOR)

    def _overlay(self, screen, title, subtitle):
        shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        shade.fill((*OVERLAY_COLOR, 150))
        screen.blit(shade, (0, 0))
        self.draw_text(screen, self.big_font, title, (WIDTH // 2, HEIGHT // 2 - 30))
        self.draw_text(screen, self.small_font, subtitle, (WIDTH // 2, HEIGHT // 2 + 30))
