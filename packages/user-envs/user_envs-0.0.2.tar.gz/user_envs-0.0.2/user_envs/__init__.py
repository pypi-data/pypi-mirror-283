from gym.envs.registration import register


register(
    id='newlunar-v0',
    entry_point='user_envs.envs: Agent_Lunar',
)
