import os
import sys
from setuptools import setup, find_packages

def create_desktop_entry_linux():
    home_dir = os.path.expanduser("~")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(project_dir, 'icon.png')
    exec_path = os.path.join(project_dir, 'ywp_script.py')

    desktop_entry_content = f"""
    [Desktop Entry]
    Version=13.2
    Name=YWP
    Comment=Your Wanted Products
    Exec=python3 {exec_path}
    Icon={icon_path}
    Terminal=false
    Type=Application
    Categories=Utility;
    """

    desktop_entry_path = os.path.join(home_dir, ".local", "share", "applications", "YWP.desktop")
    
    os.makedirs(os.path.dirname(desktop_entry_path), exist_ok=True)

    with open(desktop_entry_path, 'w') as f:
        f.write(desktop_entry_content)
    
    os.system(f'cp {icon_path} {os.path.join(home_dir, ".local", "share", "applications", "icon.png")}')

def create_desktop_entry_mac():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    exec_path = os.path.join(project_dir, 'ywp_script.py')
    app_dir = os.path.join(project_dir, 'dist', 'YWP.app', 'Contents', 'MacOS')
    
    os.makedirs(app_dir, exist_ok=True)
    
    with open(os.path.join(app_dir, 'ywp_script'), 'w') as f:
        f.write(f'#!/bin/bash\npython3 {exec_path}\n')

    os.chmod(os.path.join(app_dir, 'ywp_script'), 0o755)

def create_desktop_entry_windows():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(project_dir, 'icon.ico')
    exec_path = os.path.join(project_dir, 'ywp_script.py')
    script = f"""
    @echo off
    python {exec_path}
    """
    
    with open('YWP.bat', 'w') as f:
        f.write(script)

    return {
        "script": "YWP.bat",
        "icon_resources": [(0, icon_path)],
    }

if sys.platform.startswith('linux'):
    create_desktop_entry_linux()
elif sys.platform == "darwin":
    create_desktop_entry_mac()

setup_options = {
    'name': 'YWP',
    'version': '14.3',
    'packages': find_packages(),
    'install_requires': [
        "dill==0.3.8",
        "flask==3.0.3",
        "flask-cors==4.0.1",
        "gtts==2.5.1",
        "joblib==1.4.2",
        "moviepy==1.0.3",
        "nltk==3.8.1",
        "pyaudio==0.2.14",
        "pygame==2.5.2",
        "selenium==4.22.0",
        "setuptools==68.1.2",
        "sounddevice==0.4.7",
        "SpeechRecognition==3.10.4",
        "tensorflow==2.16.1",
        "tflearn==0.5.0",
        "twine==5.1.0",
        "wheel==0.43.0",
        "pycryptodome==3.20.0",
        "vosk==0.3.45",
        "tqdm==4.66.4",
        "pyttsx3==2.90",
        "requests==2.31.0",
        "googletrans==4.0.0rc1",
    ],
    'classifiers': [
        'Programming Language :: Python :: 3',
    ],
    'package_data': {
        '': ['icon.png', 'icon.ico', 'ywp_script.py'],
    },
    'python_requires': '>=3.6',
    'description': 'This is a library to simplify the Python language for beginners while adding some features that are not found in other libraries',
    'long_description': open('README.md').read(),
    'long_description_content_type': 'text/markdown',
    'author': 'Your Wanted Products (YWP)',
    'author_email': 'pbstzidr@ywp.freewebhostmost.com',
    'url': 'https://github.com/username/repo',  # ضع رابط مستودع GitHub هنا
    'entry_points': {
        'console_scripts': [
            'YWP.install_packages=YWP:inuser.install_system_packages',
            'YWP.install_libraries=YWP:inuser.install_library_packages',
            'YWP.upgrade_libraries=YWP:inuser.upgrade_required_libraries',
            'YWP.upgrade_library=YWP:inuser.upgrade_library',
            'YWP=YWP:help',
            'YWP.help=YWP:help',
            'YWP.Audios.play_sound=YWP:inuser.Audios.play_sound_inuser',
            'YWP.Audios.play_audio=YWP:inuser.Audios.play_audio_inuser',
            'YWP.Audios.record_audio=YWP:inuser.Audios.record_audio_inuser',
            'YWP.Audios.transcribe_audio_offline=YWP:inuser.Audios.transcribe_audio_offline_inuser',
            'YWP.Audios.transcribe_audio=YWP:inuser.Audios.transcribe_audio_inuser',
            'YWP.Audios.text_to_speech=YWP:inuser.Audios.text_to_speech_inuser',
            'YWP.Audios.text_to_speech_offline=YWP:inuser.Audios.text_to_speech_offline_inuser',
            'YWP.Audios.play_audio_online=YWP:inuser.Audios.play_audio_online_inuser',
            'YWP.Files.create_file=YWP:inuser.Files.create_file_inuser',
            'YWP.Files.open_file=YWP:inuser.Files.open_file_inuser',
            'YWP.Files.delete_all_files=YWP:inuser.Files.delete_all_files_inuser',
            'YWP.Websites.open_website=YWP:inuser.Websites.open_website_inuser',
            'YWP.Crypto.token_information=YWP:inuser.Crypto.token_information_inuser',
            'YWP.VideosCreator.Basic.basic_video_creator=YWP:inuser.VideosCreator.Basic.basic_video_creator_inuser',
            'YWP.endecrypt.aes.encrypt=YWP:inuser.endecrypt.aes.encrypt_inuser',
            'YWP.endecrypt.aes.decrypt=YWP:inuser.endecrypt.aes.decrypt_inuser',
            'YWP.endecrypt.BlowFish.encrypt=YWP:inuser.endecrypt.BlowFish.encrypt_inuser',
            'YWP.endecrypt.BlowFish.decrypt=YWP:inuser.endecrypt.BlowFish.decrypt_inuser',
            'YWP.endecrypt.Base64.encrypt=YWP:inuser.endecrypt.Base64.encrypt_inuser',
            'YWP.endecrypt.Base64.decrypt=YWP:inuser.endecrypt.Base64.decrypt_inuser',
            'YWP.endecrypt.Hex.encrypt=YWP:inuser.endecrypt.Hex.encrypt_inuser',
            'YWP.endecrypt.Hex.decrypt=YWP:inuser.endecrypt.Hex.decrypt_inuser',
            'YWP.Libraries.Basic.init_creator=YWP:inuser.Libraries.Basic.init_creator_inuser',
            'YWP.Libraries.Basic.basic_setup_file_creator=YWP:inuser.Libraries.Basic.basic_setup_file_creator_inuser',
            'YWP.Libraries.Basic.upload_file_creator=YWP:inuser.Libraries.Basic.upload_file_creator_inuser',
            'YWP.Files.delete_file=YWP:inuser.Files.delete_file_inuser',
            'YWP.printstyle.print_one=YWP:inuser.printstyle.print_one_inuser',
            'YWP.printstyle.print_all=YWP:inuser.printstyle.print_all_inuser',
        ],
    },
}

if sys.platform == "win32":
    import py2exe
    setup_options.update({
        'windows': [create_desktop_entry_windows()],
    })
elif sys.platform == "darwin":
    setup_options.update({
        'setup_requires': ['py2app'],
        'app': ['ywp_script.py'],
        'options': {
            'py2app': {
                'argv_emulation': True,
                'iconfile': 'icon.icns',
            },
        },
    })

setup(**setup_options)
