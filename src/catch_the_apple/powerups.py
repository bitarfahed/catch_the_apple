from catch_the_apple.superpowers import (
    SUPER_POWER_DEFINITIONS as POWER_UP_DEFINITIONS,
    ActiveSuperPower as ActivePowerUp,
    SuperPowerDefinition as PowerUpDefinition,
    SuperPowerState as PowerUpState,
    SuperPowerSystem,
    apply_black_hole,
    apply_magnet_pull,
    apply_shockwave,
    basket_speed_scale,
    difficulty_growth_scale,
    magnet_active_object_bonus,
    object_falling_scale,
    simulation_time_scale as power_up_time_scale,
    wind_control_scale,
)


class PowerUpSystem(SuperPowerSystem):
    def choose_power_up(self) -> PowerUpDefinition:
        return self.choose_power()
