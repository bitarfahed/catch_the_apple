import os
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

import pygame

from catch_the_apple import __version__, config, get_version
from catch_the_apple.audio import AudioSettings
from catch_the_apple.cheats import CHEAT_DEFINITIONS, CheatState
from catch_the_apple.game import Game, is_valid_player_name
from catch_the_apple.collision import detect_basket_collision
from catch_the_apple.difficulty_profiles import DIFFICULTY_PROFILES, EXPERT, INTERMEDIATE
from catch_the_apple.dynamic_environment import EnvironmentManager, WEATHER_PRESETS
from catch_the_apple.entities import FallingObject
from catch_the_apple.environment import ProceduralEnvironmentRenderer
from catch_the_apple.events import ObjectCaughtEvent, ObjectMissedEvent
from catch_the_apple.input import InputState
from catch_the_apple.input import poll_input
from catch_the_apple.lighting import LightingSystem
from catch_the_apple.math2d import Transform2D, clamp, vec2
from catch_the_apple.object_definitions import OBJECT_DEFINITIONS
from catch_the_apple.particles import EmitterConfig, ParticleSystem
from catch_the_apple.persistence import PersistenceStore
from catch_the_apple.powerups import (
    POWER_UP_DEFINITIONS,
    PowerUpSystem,
    apply_magnet_pull,
    difficulty_growth_scale,
    power_up_time_scale,
)
from catch_the_apple.procedural_assets import ProceduralAssetRenderer
from catch_the_apple.rendering import Renderer
from catch_the_apple.session import GameSession
from catch_the_apple.states import DeveloperConsoleState, PausedState, PlayingState
from catch_the_apple.superpowers import SuperPowerState, SuperPowerSystem
from catch_the_apple.systems.difficulty import apply_score_progression
from catch_the_apple.systems.game_rules import apply_game_rules
from catch_the_apple.systems.movement import update_movement
from catch_the_apple.systems.spawning import SpawnSystem
from catch_the_apple.world import World


def input_state(**overrides: bool) -> InputState:
    values = {
        "quit_requested": False,
        "left_pressed": False,
        "right_pressed": False,
        "dash_pressed": False,
        "debug_collision_toggled": False,
        "start_pressed": False,
        "pause_pressed": False,
        "restart_pressed": False,
        "debug_overlay_toggled": False,
        "mute_toggled": False,
        "volume_up_pressed": False,
        "volume_down_pressed": False,
        "mouse_left_clicked": False,
        "mouse_position": (0, 0),
        "console_requested": False,
        "console_submit_pressed": False,
        "text_input": "",
        "backspace_pressed": False,
    }
    values.update(overrides)
    return InputState(**values)


class CoreSystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls) -> None:
        pygame.quit()

    def test_transform_and_clamp_math_helpers_are_reusable(self) -> None:
        transform = Transform2D(position=vec2(10.0, 20.0), rotation=15.0, scale=vec2(2.0, 3.0))

        self.assertEqual(transform.position, vec2(10.0, 20.0))
        self.assertEqual(transform.rotation, 15.0)
        self.assertEqual(transform.scale, vec2(2.0, 3.0))
        self.assertEqual(clamp(-5.0, 0.0, 10.0), 0.0)
        self.assertEqual(clamp(15.0, 0.0, 10.0), 10.0)
        self.assertEqual(clamp(6.0, 0.0, 10.0), 6.0)

    def test_sdk_exposes_project_version(self) -> None:
        self.assertEqual(get_version(), __version__)

    def test_package_version_matches_project_metadata(self) -> None:
        pyproject = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

        self.assertEqual(__version__, pyproject["project"]["version"])

    def test_object_registry_contains_only_regular_apple_in_spawn_config(self) -> None:
        expected_ids = {"regular_apple", "golden_apple", "rotten_apple", "bomb", "power_up", "player_name"}

        self.assertEqual(set(OBJECT_DEFINITIONS), expected_ids)
        self.assertEqual(config.SPAWN_CONFIG.enabled_object_ids, ("regular_apple",))

    def test_seeded_spawn_system_is_deterministic(self) -> None:
        spawn_config = config.SpawnConfig(seed=42)
        first = SpawnSystem(spawn_config).create_falling_object()
        second = SpawnSystem(spawn_config).create_falling_object()

        self.assertEqual(first.definition.identifier, "regular_apple")
        self.assertEqual(second.definition.identifier, "regular_apple")
        self.assertEqual(first.x, second.x)
        self.assertEqual(first.y, config.SPAWN_CONFIG.spawn_y)

    def test_single_difficulty_profile_adjusts_existing_spawn_and_wind_config(self) -> None:
        profile_names = [profile.display_name for profile in DIFFICULTY_PROFILES]

        self.assertEqual(profile_names, ["Standard"])
        self.assertIs(EXPERT, INTERMEDIATE)
        self.assertIn("player_name", INTERMEDIATE.spawn_config.enabled_object_ids)
        self.assertLess(INTERMEDIATE.spawn_config.spawn_weights[-1][1], 0.01)
        self.assertGreater(INTERMEDIATE.gameplay_wind_scale, 3.0)
        self.assertIn("golden_apple", EXPERT.spawn_config.enabled_object_ids)
        self.assertIn("rotten_apple", EXPERT.spawn_config.enabled_object_ids)
        self.assertIn("bomb", EXPERT.spawn_config.enabled_object_ids)
        self.assertIn("power_up", EXPERT.spawn_config.enabled_object_ids)

    def test_spawn_reset_reselects_object_definition_from_weights(self) -> None:
        spawn_config = config.SpawnConfig(
            enabled_object_ids=("regular_apple", "golden_apple"),
            spawn_weights=(("regular_apple", 0.0), ("golden_apple", 1.0)),
        )
        spawn_system = SpawnSystem(spawn_config)
        falling_object = spawn_system.create_falling_object()

        spawn_system.reset_falling_object(falling_object)

        self.assertEqual(falling_object.definition.identifier, "golden_apple")

    def test_golden_rain_biases_existing_spawn_weights(self) -> None:
        spawn_system = SpawnSystem(
            config.SpawnConfig(
                seed=1,
                enabled_object_ids=("regular_apple", "golden_apple"),
                spawn_weights=(("regular_apple", 1.0), ("golden_apple", 0.0)),
            )
        )
        session = GameSession()
        session.powerups.activate(POWER_UP_DEFINITIONS["golden_rain"])
        spawn_system.power_state = session.powerups

        self.assertEqual(spawn_system.choose_object_definition().identifier, "regular_apple")

        spawn_system.spawn_weights = {"regular_apple": 0.05, "golden_apple": 0.05}
        golden_count = sum(
            1
            for _ in range(25)
            if spawn_system.choose_object_definition().identifier == "golden_apple"
        )
        self.assertGreater(golden_count, 12)

    def test_score_progression_is_profile_based_and_clamped(self) -> None:
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)

        self.assertFalse(apply_score_progression(1, spawn_system, INTERMEDIATE.difficulty_config))
        self.assertEqual(spawn_system.current_object_speed, INTERMEDIATE.spawn_config.object_speed)

        self.assertTrue(apply_score_progression(5, spawn_system, INTERMEDIATE.difficulty_config))
        self.assertEqual(
            spawn_system.current_object_speed,
            INTERMEDIATE.spawn_config.object_speed + INTERMEDIATE.difficulty_config.speed_increase,
        )

        spawn_system.current_object_speed = INTERMEDIATE.difficulty_config.max_object_speed
        apply_score_progression(10, spawn_system, INTERMEDIATE.difficulty_config)
        self.assertEqual(spawn_system.current_object_speed, INTERMEDIATE.difficulty_config.max_object_speed)

    def test_slow_motion_scales_difficulty_growth(self) -> None:
        session = GameSession()
        session.powerups.activate(POWER_UP_DEFINITIONS["slow_motion"])

        self.assertLess(difficulty_growth_scale(session.powerups), 1.0)
        self.assertLess(power_up_time_scale(session.powerups), 0.6)

    def test_movement_uses_velocity_acceleration_drag_and_dash_state(self) -> None:
        world = World()
        start_x = world.basket.x

        update_movement(world, input_state(right_pressed=True), 0.1)
        self.assertGreater(world.basket.x, start_x)
        self.assertGreater(world.basket.velocity.x, 0.0)
        self.assertEqual(world.basket.movement_direction.x, 1.0)

        update_movement(world, input_state(dash_pressed=True, right_pressed=True), 0.016)
        self.assertTrue(world.basket.movement.is_dashing)
        self.assertGreater(world.basket.movement.dash_cooldown_remaining, 0.0)

        velocity_before_drag = world.basket.velocity.x
        update_movement(world, input_state(), 0.2)
        self.assertLessEqual(abs(world.basket.velocity.x), abs(velocity_before_drag))

    def test_cycle_cheat_wraps_basket_with_modulo_arithmetic(self) -> None:
        world = World()
        world.basket.x = config.SCREEN_WIDTH - 4
        world.basket.movement.velocity.x = 220.0

        update_movement(world, input_state(right_pressed=True), 0.1, cycle_wrap=True)

        self.assertLess(world.basket.x, 30.0)

    def test_wind_influence_eases_object_trajectory(self) -> None:
        world = World()
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        manager = EnvironmentManager(
            wind_config=INTERMEDIATE.wind_config,
            gameplay_wind_scale=INTERMEDIATE.gameplay_wind_scale,
        )
        falling_object = world.falling_objects[0]
        start_x = falling_object.x

        manager.update(0.1)
        update_movement(world, input_state(), 0.1, manager)
        first_wind_velocity = falling_object.wind_velocity.x
        update_movement(world, input_state(), 0.1, manager)

        self.assertNotEqual(falling_object.x, start_x)
        self.assertNotEqual(first_wind_velocity, 0.0)
        self.assertGreater(abs(falling_object.wind_velocity.x), abs(first_wind_velocity))

    def test_wind_vector_field_moves_left_and_right_smoothly(self) -> None:
        manager = EnvironmentManager(
            wind_config=INTERMEDIATE.wind_config,
            gameplay_wind_scale=INTERMEDIATE.gameplay_wind_scale,
        )
        samples = []

        for index in range(80):
            manager.update(0.5)
            samples.append(manager.gameplay_wind_velocity().x)

        self.assertTrue(any(value < 0.0 for value in samples))
        self.assertTrue(any(value > 0.0 for value in samples))
        self.assertLess(
            max(abs(samples[index + 1] - samples[index]) for index in range(len(samples) - 1)),
            230.0,
        )

    def test_poll_input_uses_escape_only_for_pause_not_p_key(self) -> None:
        pygame.event.clear()
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))

        self.assertFalse(poll_input().pause_pressed)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))

        self.assertTrue(poll_input().pause_pressed)

    def test_freeze_bombs_stops_only_hazard_falling_motion(self) -> None:
        world = World()
        spawn_system = SpawnSystem(
            config.SpawnConfig(max_active_objects=2, enabled_object_ids=("regular_apple",))
        )
        spawn_system.update(world)
        world.falling_objects[0].definition = OBJECT_DEFINITIONS["bomb"]
        world.falling_objects[1].definition = OBJECT_DEFINITIONS["regular_apple"]
        session = GameSession()
        session.powerups.activate(POWER_UP_DEFINITIONS["freeze_bombs"])
        start_positions = [falling_object.y for falling_object in world.falling_objects]

        update_movement(world, input_state(), 0.1, power_state=session.powerups)

        self.assertEqual(world.falling_objects[0].y, start_positions[0])
        self.assertGreater(world.falling_objects[1].y, start_positions[1])

    def test_catch_rule_updates_score_combo_and_emits_event(self) -> None:
        world = World()
        session = GameSession()
        spawn_system = SpawnSystem(config.SpawnConfig(seed=1))
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.score, 1)
        self.assertEqual(session.combo, 1)
        self.assertEqual(session.best_combo, 1)
        self.assertFalse(session.game_over)
        self.assertIsInstance(events[0], ObjectCaughtEvent)

    def test_missing_regular_apple_reduces_score_without_life_loss(self) -> None:
        world = World()
        session = GameSession(lives=3, score=4, combo=2, best_combo=2, has_earned_score=True)
        spawn_system = SpawnSystem(config.SpawnConfig(seed=2))
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["regular_apple"]
        falling_object.y = config.SCREEN_HEIGHT + 1
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.score, 2)
        self.assertEqual(session.lives, 3)
        self.assertEqual(session.combo, 0)
        self.assertFalse(session.game_over)
        self.assertIsInstance(events[0], ObjectMissedEvent)

    def test_missing_regular_apple_to_zero_ends_game_after_points_were_earned(self) -> None:
        world = World()
        session = GameSession(lives=3, score=1, has_earned_score=True)
        spawn_system = SpawnSystem(config.SpawnConfig(seed=2))
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["regular_apple"]
        falling_object.y = config.SCREEN_HEIGHT + 1

        apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.score, 0)
        self.assertEqual(session.lives, 3)
        self.assertTrue(session.game_over)

    def test_lives_reaching_zero_still_ends_game(self) -> None:
        world = World()
        session = GameSession(lives=1, score=3, has_earned_score=True)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["bomb"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        apply_game_rules(world, session, spawn_system, INTERMEDIATE.difficulty_config)

        self.assertEqual(session.lives, 0)
        self.assertTrue(session.game_over)

    def test_apple_storm_missed_bonus_apples_do_not_cost_lives(self) -> None:
        world = World()
        session = GameSession(lives=3, score=5, combo=2)
        session.powerups.activate(POWER_UP_DEFINITIONS["magnet"])
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["golden_apple"]
        falling_object.y = config.SCREEN_HEIGHT + 1

        events = apply_game_rules(
            world,
            session,
            spawn_system,
            INTERMEDIATE.difficulty_config,
            PowerUpSystem(seed=1),
        )

        self.assertEqual(session.lives, 3)
        self.assertEqual(session.score, 5)
        self.assertEqual(session.combo, 2)
        self.assertEqual(events[0].damage, 0)

    def test_missed_hazards_do_not_cost_lives(self) -> None:
        for identifier in ("rotten_apple", "bomb"):
            with self.subTest(identifier=identifier):
                world = World()
                session = GameSession(lives=3, score=4, combo=2)
                spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
                spawn_system.update(world)
                falling_object = world.falling_objects[0]
                falling_object.definition = OBJECT_DEFINITIONS[identifier]
                falling_object.y = config.SCREEN_HEIGHT + 1

                events = apply_game_rules(
                    world,
                    session,
                    spawn_system,
                    INTERMEDIATE.difficulty_config,
                    PowerUpSystem(seed=1),
                )

                self.assertEqual(session.lives, 3)
                self.assertEqual(session.score, 4)
                self.assertEqual(session.combo, 2)
                self.assertFalse(session.game_over)
                self.assertEqual(events[0].damage, 0)

    def test_missed_golden_apple_does_not_cost_lives(self) -> None:
        world = World()
        session = GameSession(lives=3, score=4, combo=2)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["golden_apple"]
        falling_object.y = config.SCREEN_HEIGHT + 1

        events = apply_game_rules(
            world,
            session,
            spawn_system,
            INTERMEDIATE.difficulty_config,
            PowerUpSystem(seed=1),
        )

        self.assertEqual(session.lives, 3)
        self.assertEqual(session.score, 4)
        self.assertEqual(session.combo, 2)
        self.assertFalse(session.game_over)
        self.assertEqual(events[0].damage, 0)

    def test_catching_rotten_apple_reduces_score_without_life_loss(self) -> None:
        world = World()
        session = GameSession(lives=3, score=5, combo=2, has_earned_score=True)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["rotten_apple"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(
            world,
            session,
            spawn_system,
            INTERMEDIATE.difficulty_config,
            PowerUpSystem(seed=1),
        )

        self.assertEqual(session.score, 3)
        self.assertEqual(session.lives, 3)
        self.assertEqual(session.combo, 0)
        self.assertFalse(session.game_over)
        self.assertIsInstance(events[0], ObjectCaughtEvent)

    def test_score_returning_to_zero_after_earning_points_ends_game(self) -> None:
        world = World()
        session = GameSession(lives=3, score=1, combo=1, has_earned_score=True)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["rotten_apple"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        apply_game_rules(
            world,
            session,
            spawn_system,
            INTERMEDIATE.difficulty_config,
            PowerUpSystem(seed=1),
        )

        self.assertEqual(session.score, 0)
        self.assertEqual(session.lives, 3)
        self.assertTrue(session.game_over)

    def test_initial_zero_score_does_not_immediately_end_game(self) -> None:
        world = World()
        session = GameSession(lives=3, score=0)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)

        apply_game_rules(
            world,
            session,
            spawn_system,
            INTERMEDIATE.difficulty_config,
            PowerUpSystem(seed=1),
        )

        self.assertFalse(session.game_over)

    def test_player_name_object_grants_capped_extra_life_and_has_no_miss_penalty(self) -> None:
        world = World()
        session = GameSession(player_name="Ada", lives=2)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["player_name"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(world, session, spawn_system, INTERMEDIATE.difficulty_config)

        self.assertEqual(session.lives, 3)
        self.assertEqual(events[0].object_identifier, "player_name")

        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["player_name"]
        falling_object.y = config.SCREEN_HEIGHT + 1
        events = apply_game_rules(world, session, spawn_system, INTERMEDIATE.difficulty_config)

        self.assertEqual(session.lives, 3)
        self.assertEqual(events[0].damage, 0)

    def test_hazard_collision_costs_life_without_awarding_score(self) -> None:
        world = World()
        session = GameSession(lives=3)
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["bomb"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.score, 0)
        self.assertEqual(session.lives, 2)
        self.assertEqual(session.combo, 0)
        self.assertIsInstance(events[0], ObjectMissedEvent)

    def test_shield_cheat_filters_bomb_collision_damage(self) -> None:
        world = World()
        session = GameSession(lives=3)
        session.cheats.activate(CHEAT_DEFINITIONS["shield"])
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["bomb"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.lives, 3)
        self.assertEqual(events[0].damage, 0)

    def test_fahed_cheat_auto_collects_apples_and_blocks_hazard_damage(self) -> None:
        world = World()
        session = GameSession(score=0, lives=2)
        session.cheats.activate(CHEAT_DEFINITIONS["fahed"])
        spawn_system = SpawnSystem(
            config.SpawnConfig(max_active_objects=1, enabled_object_ids=("regular_apple",))
        )
        spawn_system.update(world)

        events = apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.score, 1)
        self.assertIsInstance(events[0], ObjectCaughtEvent)

        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["bomb"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)
        events = apply_game_rules(world, session, spawn_system)

        self.assertEqual(session.lives, 2)
        self.assertEqual(events[0].damage, 0)

    def test_power_up_collision_activates_reusable_power_up_state(self) -> None:
        world = World()
        session = GameSession()
        spawn_system = SpawnSystem(INTERMEDIATE.spawn_config)
        power_up_system = PowerUpSystem(seed=1)
        spawn_system.update(world)
        falling_object = world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["power_up"]
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.y = world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(
            world,
            session,
            spawn_system,
            INTERMEDIATE.difficulty_config,
            power_up_system,
        )

        self.assertEqual(session.score, 0)
        self.assertTrue(session.powerups.active)
        self.assertIsInstance(events[0], ObjectCaughtEvent)

    def test_super_power_cheat_codes_resolve_definitions(self) -> None:
        system = SuperPowerSystem(seed=1)

        self.assertEqual(system.by_cheat_code("MAGNET").identifier, "magnet")
        self.assertEqual(system.by_cheat_code("void").identifier, "black_hole")
        self.assertIsNone(system.by_cheat_code("NOPE"))
        self.assertTrue(all(definition.spawn_weight > 0.0 for definition in system.definitions))

    def test_cheat_state_expires_temporary_commands(self) -> None:
        state = CheatState()
        state.activate(CHEAT_DEFINITIONS["easy"])

        state.update(19.0)
        self.assertTrue(state.is_active("easy"))
        state.update(2.0)
        self.assertFalse(state.is_active("easy"))

    def test_magnet_only_pulls_regular_and_golden_apples(self) -> None:
        world = World()
        spawn_system = SpawnSystem(
            config.SpawnConfig(max_active_objects=4, enabled_object_ids=("regular_apple",))
        )
        spawn_system.update(world)
        identifiers = ("regular_apple", "golden_apple", "rotten_apple", "bomb")
        for falling_object, identifier in zip(world.falling_objects, identifiers, strict=True):
            falling_object.definition = OBJECT_DEFINITIONS[identifier]
            falling_object.x = 50.0
        session = GameSession()
        session.powerups.activate(POWER_UP_DEFINITIONS["magnet"])

        apply_magnet_pull(world, 0.25, session.powerups)

        moved = [falling_object.x > 50.0 for falling_object in world.falling_objects]
        self.assertEqual(moved, [True, True, False, False])

    def test_continuous_collision_detection_catches_fast_vertical_sweep(self) -> None:
        world = World()
        falling_object = SpawnSystem(config.SpawnConfig(seed=3)).create_falling_object()
        falling_object.x = world.basket.x + world.basket.width / 2 - falling_object.radius
        falling_object.previous_position.update(falling_object.x, world.basket.y - 140)
        falling_object.y = world.basket.y + world.basket.height + 40

        result = detect_basket_collision(world.basket, falling_object)

        self.assertTrue(result.caught)
        self.assertTrue(result.used_ccd)

    def test_particle_system_uses_fixed_pool_and_expires_particles(self) -> None:
        particle_system = ParticleSystem(pool_size=5, seed=5)
        emitter = EmitterConfig(
            count=12,
            speed_min=10.0,
            speed_max=20.0,
            lifetime_min=0.05,
            lifetime_max=0.05,
            start_size=4.0,
            end_size=1.0,
            start_alpha=200,
            end_alpha=0,
            start_color=(255, 0, 0),
            end_color=(255, 255, 0),
        )

        particle_system.emit(vec2(10.0, 10.0), emitter)
        self.assertLessEqual(len(list(particle_system.active_particles())), 5)

        particle_system.update(0.1)
        self.assertEqual(len(list(particle_system.active_particles())), 0)

    def test_persistence_handles_corrupted_files_and_saves_session_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            save_path = Path(temp_dir) / "save.json"
            save_path.write_text("{not-valid-json", encoding="utf-8")
            store = PersistenceStore(save_path)

            self.assertEqual(store.data.high_score, 0)

            store.save_settings(AudioSettings(master_volume=0.25, muted=True))
            store.finish_session(GameSession(score=7, best_combo=3))

            reloaded = PersistenceStore(save_path)
            self.assertEqual(reloaded.data.high_score, 7)
            self.assertEqual(reloaded.data.best_combo, 3)
            self.assertEqual(reloaded.data.settings.master_volume, 0.25)
            self.assertTrue(reloaded.data.settings.muted)

    def test_environment_manager_exposes_weather_wind_and_lighting_state(self) -> None:
        manager = EnvironmentManager("clear")

        self.assertGreaterEqual(len(WEATHER_PRESETS), 6)
        self.assertEqual(manager.state.weather.name, "Clear")

        manager.set_weather("strong_wind")
        state = manager.update(0.5)

        self.assertEqual(state.weather.name, "Strong Wind")
        self.assertGreaterEqual(state.wind.strength, 0.0)
        self.assertGreaterEqual(state.lighting.ambient, 0.0)
        self.assertGreater(manager.particle_wind_velocity().length(), manager.gameplay_wind_velocity().length())

    def test_procedural_rendering_and_lighting_cache_surfaces(self) -> None:
        assets = ProceduralAssetRenderer()
        first = assets.get_falling_object_surface("regular_apple", 30, (213, 50, 80))
        second = assets.get_falling_object_surface("regular_apple", 30, (213, 50, 80))
        basket = assets.get_basket_surface(100, 20)
        lighting = LightingSystem()
        lit_first = lighting.apply_lighting(first, 0.2)
        lit_second = lighting.apply_lighting(first, 0.2)
        shadow = lighting.get_ground_shadow(30, 30, 0.4)

        self.assertIs(first, second)
        self.assertEqual(first.get_size(), (30, 30))
        self.assertEqual(basket.get_size(), (100, 20))
        self.assertIs(lit_first, lit_second)
        self.assertGreater(shadow.get_width(), 0)

    def test_renderer_uses_dedicated_night_palette_for_readability(self) -> None:
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        renderer = Renderer(screen)
        manager = EnvironmentManager("clear")
        manager.day_night.progress = 0.0
        manager.update(0.0)

        self.assertEqual(
            renderer.object_color_for_environment("regular_apple", config.RED, 0.0),
            config.RED,
        )
        self.assertEqual(renderer.night_factor(manager.state), 1.0)
        self.assertEqual(
            renderer.object_color_for_environment("regular_apple", config.RED, 1.0),
            (245, 255, 255),
        )
        self.assertEqual(
            renderer.object_color_for_environment("bomb", (32, 32, 32), 1.0),
            (32, 32, 32),
        )

        self.assertEqual(
            renderer.object_color_for_environment("golden_apple", (255, 215, 0), 1.0),
            (255, 215, 0),
        )

    def test_name_entry_renders_supported_characters(self) -> None:
        from catch_the_apple.ui import UI

        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        ui = UI()

        ui.render_name_entry(screen, "Ada7", "")
        rendered_text = ui.large_font.render("Ada7", True, config.WHITE)

        self.assertGreater(rendered_text.get_width(), 0)
        self.assertGreater(rendered_text.get_height(), 0)

    def test_player_name_validation_accepts_one_alphanumeric_word(self) -> None:
        self.assertTrue(is_valid_player_name("Ada7"))
        self.assertFalse(is_valid_player_name(""))
        self.assertFalse(is_valid_player_name("Ada Lovelace"))
        self.assertFalse(is_valid_player_name("NameThatIsTooLong"))

    def test_environment_renderer_caches_parallax_layers(self) -> None:
        manager = EnvironmentManager("clear")
        renderer = ProceduralEnvironmentRenderer(160, 120, seed=9)
        target = pygame.Surface((160, 120)).convert()

        renderer.render(target, manager.state)
        first_layers = renderer.layers
        renderer.render(target, manager.update(0.1))

        self.assertIs(first_layers, renderer.layers)
        self.assertEqual([layer.name for layer in first_layers], ["sky", "mountains", "trees", "bushes", "grass"])

    def test_weather_cycle_reaches_rain_without_changing_gameplay_wind_override(self) -> None:
        manager = EnvironmentManager(
            wind_config=INTERMEDIATE.wind_config,
            gameplay_wind_scale=INTERMEDIATE.gameplay_wind_scale,
        )
        initial_velocity = manager.gameplay_wind_velocity().length()

        manager.update(48.1)

        self.assertEqual(manager.state.weather.name, "Rain")
        self.assertGreater(manager.gameplay_wind_velocity().length(), initial_velocity * 0.5)

    def test_developer_cheats_activate_and_restore_through_game(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()
        game.session.score = 6

        self.assertTrue(game.activate_cheat_code("easy"))
        self.assertTrue(game.session.cheats.is_active("easy"))
        self.assertEqual(game.cheat_falling_time_scale(), 0.55)

        self.assertTrue(game.activate_cheat_code("shield"))
        self.assertEqual(game.session.score, 1)
        self.assertTrue(game.session.cheats.is_active("shield"))

        self.assertTrue(game.activate_cheat_code("flip 270"))
        self.assertEqual(game.session.cheats.value("flip"), 270.0)

        self.assertTrue(game.activate_cheat_code("nosound"))
        self.assertTrue(game.audio.settings.muted)
        self.assertTrue(game.activate_cheat_code("sound"))
        self.assertFalse(game.audio.settings.muted)

        self.assertTrue(game.activate_cheat_code("wind"))
        game.apply_cheat_environment()
        self.assertEqual(game.environment_manager.state.weather.name, "Rain")
        game.session.cheats.update(21.0)
        game.apply_cheat_environment()
        self.assertEqual(game.environment_manager.state.weather.name, "Clear")

    def test_pause_console_workflow_activates_cheat_and_resumes(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()

        game.states.handle_input(game, input_state(pause_pressed=True))
        self.assertIsInstance(game.states.current, PausedState)

        game.states.handle_input(game, input_state(console_requested=True))
        self.assertIsInstance(game.states.current, DeveloperConsoleState)

        game.states.handle_input(game, input_state(text_input="easy"))
        game.states.handle_input(game, input_state(console_submit_pressed=True))
        self.assertTrue(game.session.cheats.is_active("easy"))

        game.states.handle_input(game, input_state(pause_pressed=True))
        self.assertIsInstance(game.states.current, PausedState)

        game.states.handle_input(game, input_state(pause_pressed=True))
        self.assertIsInstance(game.states.current, PlayingState)

    def test_typing_cheat_codes_during_active_gameplay_is_ignored(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()

        game.states.handle_input(game, input_state(text_input="easy", console_submit_pressed=True))

        self.assertIsInstance(game.states.current, PlayingState)
        self.assertFalse(game.session.cheats.is_active("easy"))

    def test_console_accepts_full_flip_command_without_resuming_gameplay(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()

        game.states.handle_input(game, input_state(pause_pressed=True))
        game.states.handle_input(game, input_state(console_requested=True))
        game.states.handle_input(game, input_state(text_input="flip 180"))
        game.states.handle_input(game, input_state(console_submit_pressed=True))

        self.assertIsInstance(game.states.current, DeveloperConsoleState)
        self.assertEqual(game.session.cheats.value("flip"), 180.0)

    def test_temporary_developer_cheats_toggle_off(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()
        game.session.score = 6

        for code, identifier in (
            ("easy", "easy"),
            ("wind", "wind"),
            ("cycle", "cycle"),
            ("fahed", "fahed"),
            ("insane", "insane"),
        ):
            with self.subTest(code=code):
                self.assertTrue(game.activate_cheat_code(code))
                self.assertTrue(game.session.cheats.is_active(identifier))
                self.assertTrue(game.activate_cheat_code(code))
                self.assertFalse(game.session.cheats.is_active(identifier))

        self.assertTrue(game.activate_cheat_code("shield"))
        self.assertTrue(game.session.cheats.is_active("shield"))
        self.assertTrue(game.activate_cheat_code("shield"))
        self.assertFalse(game.session.cheats.is_active("shield"))

    def test_wind_cheat_emits_visible_rain_particles(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()

        self.assertTrue(game.activate_cheat_code("wind"))
        game.update_playing(input_state(), 0.1)

        self.assertEqual(game.environment_manager.state.weather.name, "Rain")
        self.assertGreater(sum(1 for _ in game.effects.particles.active_particles()), 40)

    def test_magnet_attracts_only_regular_and_golden_apples(self) -> None:
        world = World()
        basket_center = world.basket.rect.centerx
        objects = []
        for index, identifier in enumerate(
            ("regular_apple", "golden_apple", "rotten_apple", "bomb")
        ):
            definition = OBJECT_DEFINITIONS[identifier]
            objects.append(
                FallingObject(
                    transform=Transform2D(vec2(40.0 + index * 45.0, 100.0)),
                    definition=definition,
                )
            )
        world.falling_objects = objects
        state = SuperPowerState()
        power = POWER_UP_DEFINITIONS["magnet"]
        state.activate(power)

        before = {obj.definition.identifier: abs(basket_center - obj.center.x) for obj in objects}
        apply_magnet_pull(world, 0.2, state)
        after = {obj.definition.identifier: abs(basket_center - obj.center.x) for obj in objects}

        self.assertLess(after["regular_apple"], before["regular_apple"])
        self.assertLess(after["golden_apple"], before["golden_apple"])
        self.assertEqual(after["rotten_apple"], before["rotten_apple"])
        self.assertEqual(after["bomb"], before["bomb"])
        self.assertNotEqual(objects[0].magnet_velocity.x, 0.0)
        self.assertNotEqual(objects[1].magnet_velocity.x, 0.0)
        self.assertEqual(objects[2].magnet_velocity.x, 0.0)
        self.assertEqual(objects[3].magnet_velocity.x, 0.0)

        state.update(power.duration + 0.1)
        self.assertFalse(state.is_active("magnet"))
        previous_velocity = objects[0].magnet_velocity.x
        apply_magnet_pull(world, 0.2, state)
        self.assertLess(abs(objects[0].magnet_velocity.x), abs(previous_velocity))

    def test_power_up_pickup_can_activate_magnet_during_gameplay(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()
        game.power_up_system = PowerUpSystem(seed=1)
        falling_object = game.world.falling_objects[0]
        falling_object.definition = OBJECT_DEFINITIONS["power_up"]
        falling_object.x = game.world.basket.x + game.world.basket.width / 2 - falling_object.radius
        falling_object.y = game.world.basket.y - falling_object.radius
        falling_object.previous_position.update(falling_object.transform.position)

        events = apply_game_rules(
            game.world,
            game.session,
            game.spawn_system,
            game.selected_profile.difficulty_config,
            game.power_up_system,
        )

        self.assertTrue(game.session.powerups.is_active("magnet"))
        self.assertEqual(events[0].object_identifier, "power_up")

    def test_insane_cheat_scales_apples_and_adjusts_golden_score(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()
        game.activate_cheat_code("insane")

        regular_scales = [
            game.spawn_system.scale_for_definition(OBJECT_DEFINITIONS["regular_apple"])
            for _ in range(8)
        ]
        self.assertTrue(all(3.0 <= scale <= 6.0 for scale in regular_scales))
        self.assertGreater(len(set(round(scale, 2) for scale in regular_scales)), 1)
        self.assertEqual(
            game.spawn_system.scale_for_definition(OBJECT_DEFINITIONS["golden_apple"]),
            10.0,
        )
        self.assertEqual(game.spawn_system.scale_for_definition(OBJECT_DEFINITIONS["bomb"]), 1.0)

        golden = FallingObject(
            transform=Transform2D(vec2(game.world.basket.x, game.world.basket.y)),
            definition=OBJECT_DEFINITIONS["golden_apple"],
            scale=10.0,
        )
        game.world.falling_objects = [golden]
        apply_game_rules(
            game.world,
            game.session,
            game.spawn_system,
            game.selected_profile.difficulty_config,
            game.power_up_system,
        )
        self.assertEqual(game.session.score, 3)

        self.assertTrue(game.activate_cheat_code("insane"))
        self.assertFalse(game.session.cheats.is_active("insane"))

    def test_bomb_collision_uses_distinct_explosion_sound(self) -> None:
        from catch_the_apple.audio import AudioSystem

        audio = AudioSystem(AudioSettings())
        played: list[str] = []
        audio.play_effect = played.append

        audio.play_object_effect("bomb", caught=False)

        self.assertEqual(played, ["bomb_explosion"])

    def test_all_documented_super_power_cheats_activate_and_expire(self) -> None:
        game = Game()
        game.player_name_input = "Ada"
        game.start_named_session()

        for code, identifier in (
            ("MAGNET", "magnet"),
            ("TIME", "slow_motion"),
            ("DASH", "speed_boost"),
            ("WIND", "wind_control"),
            ("WAVE", "shockwave"),
            ("VOID", "black_hole"),
            ("GRAV", "gravity_control"),
            ("GOLD", "golden_rain"),
            ("FREEZE", "freeze_bombs"),
        ):
            with self.subTest(code=code):
                self.assertTrue(game.activate_cheat_code(code))
                self.assertTrue(game.session.powerups.is_active(identifier))
                game.session.powerups.update(99.0)
                self.assertFalse(game.session.powerups.is_active(identifier))

    def test_audio_system_generates_distinct_object_effects_when_available(self) -> None:
        from catch_the_apple.audio import AudioSystem

        audio = AudioSystem(AudioSettings())
        if not audio.available:
            self.skipTest("pygame mixer unavailable in this environment")

        expected = {
            "regular_apple",
            "golden_apple",
            "rotten_apple",
            "bomb",
            "bomb_explosion",
            "power_up",
            "player_name",
        }
        self.assertTrue(expected.issubset(audio.sound_effects))
        self.assertTrue({"confirm", "error", "cheat"}.issubset(audio.ui_sounds))

        audio.play_effect("regular_apple")
        audio.play_ui("confirm")


if __name__ == "__main__":
    unittest.main()
