# Flux Nuker

Flux is an advanced, high-speed Discord nuker built for maximum impact and efficiency. Designed for speed and simplicity, Flux automates the process of destroying servers with unmatched performance. This command-line tool provides server administrators with a powerful interface to manage Discord servers, including banning/kicking members, creating/deleting channels and roles, spamming messages, granting admin permissions, and renaming servers.

**⚠️ Important**: Use this script responsibly and only on Discord servers where you have explicit authorization. Unauthorized use may violate Discord's Terms of Service, leading to account bans or legal consequences.

## Features

- **Ban/Kick Members**: Remove members from a server individually or in bulk.
- **Prune Members**: Remove inactive members based on specified days.
- **Channel Management**: Create or delete channels (text or voice).
- **Role Management**: Create or delete roles with custom names and colors.
- **Spam Channels**: Send messages to multiple channels.
- **Server Renaming**: Update the server’s name.
- **Update Checker**: Check for the latest version of the script.
- **Proxy Support**: Optional proxy usage for API requests via a `proxies.txt` file.
- **Threaded Operations**: Efficiently handle multiple tasks with a thread limit.

![image](https://github.com/user-attachments/assets/09b351f3-6305-413b-879f-ad6642702856)

## Prerequisites

To run Flux Nuker, you need:
- **Python 3.6 or higher**: Ensure Python is installed on your system.
- **Pip**: Python’s package manager for installing dependencies.
- **Discord Bot Token**: Obtain a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
- **Guild ID**: The ID of the Discord server where the bot will operate.
- **Permissions**: The bot must have sufficient permissions to perform actions.

## Usage

1. **Run the Script**: python flux.py
   
2. **Enter Guild ID**: When prompted, input the ID of the target Discord server.

3. **Interact with the Menu**: The script displays a menu with options.

4. **Exit**: Select option `12` to shut down the script.

## Running on a Fresh System

If your system has no Python modules installed:
- The script includes logic to detect missing dependencies and install them via `requirements.txt` automatically.
- After installation, it restarts itself to load the new modules.
- Ensure `pip` is installed (`python -m ensurepip --upgrade`) and you have an internet connection.
- You may need to run the script twice if the initial run triggers installations.

## Troubleshooting

- **Module Import Errors**: Ensure `requirements.txt` is present and run `pip install -r requirements.txt` manually.
- **Invalid Token**: Verify your bot token in `config.json` is correct and the bot is invited to the server.
- **Permission Denied**: Ensure the bot has the necessary permissions in the server. Check the Discord Developer Portal and server roles.
- **Rate Limits**: The script handles Discord API rate limits with retries, but heavy usage may require proxies or delays.
- **Proxy Issues**: If using proxies, confirm they’re valid and correctly formatted in `proxies.txt`.

**To the Skidders**: Think you can swipe this and claim the glory? *Think again*. Flux Nuker is a *crafted beast*, not a toy for leechers. Skid off with it, and you’ll just crash and burn—lacking the skill to wield it or fix it. Respect the code, credit the source, or face the heat of your own incompetence. This fire’s too hot for posers.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Please ensure your changes are well-documented and tested.

## Credits

- Developer - [notshelbyy#0]("https://discord.com/users/452082030180565002")

## Contact
If you encounter any issues, bugs, or have questions, feel free to contact me on Discord: ['notshelby']("https://discord.com/users/452082030180565002"). I'm always open to feedback and support requests.


## Disclaimer

This script is provided for **educational and legitimate server management purposes only**. The developer is not responsible for any misuse or damage caused by this tool. Using Flux Nuker to harm Discord servers without permission is illegal and against Discord’s Terms of Service. Always obtain explicit consent from server owners before performing actions.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
