from gym.envs.registration import register
try:
    register(
        id='StandInRain-v0',
        entry_point='custom_openai_frameworks.envs:StandInRainEnv',
        max_episode_steps=800
    )
except:
    print("Unable to register custom env")

try:
    register(
        id='SimpleCrawler-v1',
        entry_point='custom_openai_frameworks.envs:SimpleCrawler',
        max_episode_steps=800
    )
except:
    print("Unable to register custom env")

try:
    register(
        id='GolfCardGame-v0',
        entry_point='custom_openai_frameworks.envs:GolfCardGameEnv',
        max_episode_steps=800
    )
except:
    print("Unable to register custom env")
