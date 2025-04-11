# Autoboarding

A professional-grade Krita plugin that helps animators generate consistent storyboards using locally-run AI models. This plugin integrates with local Stable Diffusion backends to provide a seamless, user-friendly interface for AI-assisted storyboard creation.

## Features

- Clean, intuitive interface integrated into Krita's docker system
- Direct integration with local Stable Diffusion backends (AUTOMATIC1111/ComfyUI)
- Customizable generation parameters (size, steps, guidance, sampler)
- One-click insertion of generated images into Krita documents
- Error-resistant design with clear feedback
- Cross-platform support (Windows/Linux)

## Requirements

- Krita 5.0.0 or higher
- Python 3.8 or higher
- PyQt5/PySide2
- A running local Stable Diffusion backend:
  - [AUTOMATIC1111 WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
  - [ComfyUI](https://github.com/comfyanonymous/ComfyUI) (coming soon)

## Installation

1. Download or clone this repository
2. Copy the `autoboarding` folder to your Krita resources directory:
   - Windows: `%APPDATA%\krita\pykrita\`
   - Linux: `~/.local/share/krita/pykrita/`
   - macOS: `~/Library/Application Support/krita/pykrita/`

3. Enable the plugin in Krita:
   - Open Krita
   - Go to Settings → Configure Krita → Python Plugin Manager
   - Check "Autoboarding"
   - Restart Krita

## Usage

1. Start your local Stable Diffusion backend (AUTOMATIC1111 WebUI)
2. In Krita, open Settings → Dockers → Autoboarding
3. Click "Check Connection" to verify backend communication
4. Enter your prompt and adjust generation parameters
5. Click "Generate" to create an image
6. When satisfied, click "Insert into Document" to add the image to your Krita document

## Configuration

The plugin creates a configuration file at:
- Windows: `%APPDATA%\krita\autoboarding.json`
- Linux/macOS: `~/.config/krita/autoboarding.json`

You can edit this file to change default settings like backend URL, timeout values, and default generation parameters.

## Development

This plugin is designed for easy extension. Key areas for development:

- Additional backend support (ComfyUI integration)
- Advanced consistency features (IP-Adapter, ControlNet)
- Custom model management
- Batch generation capabilities

### Building from Source

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Run tests:
   ```bash
   pytest tests/
   ```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Krita Development Team
- AUTOMATIC1111 WebUI Team
- Stable Diffusion Community

## Support

For bug reports and feature requests, please use the GitHub issue tracker. For general questions and discussions, join our [Discussions](https://github.com/yourusername/autoboarding/discussions) page.
