# AutoBoarding - Planning Document

## 1. Project Goal

To create an open-source Krita plugin that enables non-technical animators to generate consistent, high-quality storyboards using locally run AI image generation technology. The focus is on streamlining workflow, ensuring character/style consistency, and integrating seamlessly with Krita's interface.

## 2. Target Audience

* Animators and storyboard artists (professional, hobbyist, student) using Krita
* Users with limited technical expertise who want AI-assisted storyboarding
* Users preferring local AI generation to maintain privacy and avoid per-image costs
* Users willing to set up local AI generation tools but desiring a streamlined interface

## 3. Core Features

* **Text-to-Image Generation**: Convert textual descriptions into storyboard frames
* **Character Consistency**: Ensure uniform appearance of characters across multiple frames using:
  * IP-Adapter for facial consistency
  * ControlNet for pose/structure consistency 
  * LoRA support for character-specific models
* **Integration with Krita**: Seamless embedding within Krita's interface (leveraging existing Storyboard Docker)
* **Local Model Deployment**: Use locally run AI models to maintain privacy and eliminate API costs
* **Simple UI**: Intuitive interface for inputting prompts, selecting consistency references, and configuring parameters

## 4. Scope

### In Scope (Initial Version - MVP)

* Integration with **local** AI generation backends via their APIs (ComfyUI and/or AUTOMATIC1111)
* Implementation of **IP-Adapter (Face)** using reference images for character consistency
* Implementation of **ControlNet** (e.g., OpenPose) for structural consistency
* Support for loading and using user-provided **LoRA** files for character/style consistency
* Basic prompt input UI within Krita
* UI for selecting reference images and LoRA files
* Generate images based on prompt and consistency settings
* Insert generated images onto new layers in the Krita document
* Basic error handling (API connection errors, configuration issues)

### Out of Scope (Initial Version)

* In-plugin training of LoRA or other models (users must train/acquire models externally)
* Bundling AI models or backends (users must install and run these separately)
* Cloud API integration (focus is explicitly on local)
* Complex scene management beyond single-character focus
* Advanced animation features
* Automatic generation of complex pose references
* Complex layer/frame management within Krita

## 5. Technical Stack

* **Programming Language**: Python (leveraging Krita's scripting API)
* **Krita API**: `libkis` via Krita's Python bindings
* **UI Framework**: PyQt/PySide (provided by Krita's environment)
* **AI Generation Backend**:
  * **Primary Targets**: ComfyUI API, AUTOMATIC1111 Web UI API
  * **Core Model**: Stable Diffusion SDXL (via the local backend)
* **Consistency Methods**:
  * **IP-Adapter (Face)**: Using reference images for facial consistency
  * **ControlNet**: OpenPose (for pose), Reference (for style), or Depth/Canny/Lineart (for structure)
  * **LoRA Loading**: Support for character-specific models
* **Dependencies**:
  * Local Stable Diffusion installation (user-provided)
  * `requests` for API communication
  * Potentially Pillow/PIL for image handling

## 6. Consistency Strategy

Leverage the strengths of local, open-source tools, allowing combinations for best results:

1. **Identity (Face/Character)**:
   * **Primary**: Use **IP-Adapter (Face)** with user-provided reference images
   * **Secondary**: Allow user to specify a **LoRA** file trained for specific characters

2. **Pose/Structure**:
   * Use **ControlNet** (OpenPose, Depth, Canny, etc.) with user-provided reference images
   * Implement seed locking and control for deterministic outputs

3. **Workflow**: 
   * The plugin UI will allow users to select their desired combination of techniques
   * Users can configure parameters for each method
   * Combined request sent to the local backend API

## 7. User Experience (UX)

* **Simplicity**: Abstract the complexity of backend API calls
* **Configuration**: Setup screen to configure the local backend API endpoint
* **Feedback**: Clear indicators of connection status, generation progress, errors
* **Integration**: Native Krita Docker, respecting Krita's UI conventions

## 8. Efficiency & Performance

* Use quantized or distilled models for reduced GPU memory usage
* Optimize for CPU/GPU hybrid inference to support low-resource devices
* Implement caching for frequently used prompts/characters
* Support low-resolution proxies during development

## 9. Implementation Phases

* **Phase 1**: Single-image generation with character/style consistency
* **Phase 2**: Multi-shot sequence generation using temporal attention
* **Phase 3**: Export to Krita's animation timeline and PDF/SVG storyboards

## 10. Potential Challenges

* **User Setup**: Users must install and run the local backend and download required models
* **Backend API Differences**: ComfyUI and AUTOMATIC1111 APIs work differently
* **Performance**: Generation speed depends on the user's hardware
* **Error Handling**: Need robust handling for various failure modes
* **Dependency Management**: Keeping plugin dependencies minimal

## 11. Open-Source Considerations

* **License**: MIT License to encourage widespread adoption and contribution
* **Repository**: Host on GitHub with clear contribution guidelines
* **Documentation**: Comprehensive guides and tutorials for users and contributors
* **Compliance**: Avoid proprietary models; use community-trained or open models

## 12. Success Metrics

* User adoption within the Krita community
* Positive feedback on ease of use compared to manual backend usage
* Demonstrable consistency improvements in user-generated storyboards
* Plugin stability and clear error reporting
* Community contributions and extensions