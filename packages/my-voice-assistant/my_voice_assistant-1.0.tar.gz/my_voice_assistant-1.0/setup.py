from setuptools import setup, find_packages

setup(
    name='my_voice_assistant',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyttsx3',
        'google.generativeai',  # Adjust based on the actual library name
    ],
    entry_points={
        'console_scripts': [
            'my-voice-assistant = my_voice_assistant.main:main',
        ],
    },
)
