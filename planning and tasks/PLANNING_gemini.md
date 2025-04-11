# Krita Storyboard AI Plugin - Planning Document

**Version:** 0.2
**Date:** 2025-04-11

## 1. Project Goal

To create an open-source Krita plugin that allows animators, particularly those with limited technical expertise, to efficiently generate consistent storyboard panels using locally run AI image generation technology. The focus is on simplifying the workflow, ensuring character/style consistency, and integrating seamlessly with free, open-source tools.

## 2. Target Audience

*   Animators (professional, hobbyist, student) using Krita.
*   Storyboard artists using Krita.
*   Users willing to set up local AI generation tools (like ComfyUI or AUTOMATIC1111) but desire a streamlined interface within Krita.
*   Users prioritizing free, open-source solutions and avoiding per-image generation costs.

## 3. Core Features

*   **Simple UI:** An intuitive Krita docker/panel for inputting prompts, selecting consistency references (images, LoRAs), configuring basic generation parameters, and managing poses.
*   **Local AI Integration:** Communication via API with locally running Stable Diffusion backends (ComfyUI, AUTOMATIC1111).
*   **Advanced Consistency Management:** Leveraging powerful open-source techniques like IP-Adapter (especially for faces) and ControlNet (for pose/structure) using reference images/data. Support for loading user-provided LoRAs for high-fidelity characters.
*   **Panel Insertion:** Automatically add generated images as new layers or frames within the Krita document.
*   **Efficiency:** Streamline the creation of multiple, consistent storyboard panels.

## 4. Scope

### In Scope (Initial Version - MVP)

*   Integration with **local** AI generation backends via their APIs (prioritizing ComfyUI and/or AUTOMATIC1111).
*   Implementation of **IP-Adapter (Face)** using a reference image for character consistency.
*   Implementation of **ControlNet (e.g., OpenPose)** using a reference pose image/data for structural consistency.
*   Support for loading and using user-provided **LoRA** files (`.safetensors`) for character/style consistency.
*   Basic prompt input UI within Krita.
*   UI for selecting reference images (for IP-Adapter, ControlNet) and LoRA files.
*   Generate a single panel based on prompt and consistency settings.
*   Insert generated image onto a new layer in the current Krita document.
*   Basic error handling (API connection errors, configuration issues).

### Out of Scope (Initial Version - MVP)

*   In-plugin training of LoRA or other models. Users must train/acquire models beforehand.
*   Bundling AI models or backends. Users must install and run these separately.
*   Cloud API integration (focus is explicitly on local).
*   Complex scene management beyond single-character focus with consistent pose/identity.
*   Advanced animation features.
*   Automatic generation of complex pose references (user provides them).
*   Complex layer/frame management within Krita.

## 5. Technology Stack

*   **Plugin Language:** Python [20, 42]
*   **Krita API:** `libkis` via Krita's Python bindings [42]
*   **UI Framework:** PyQt / PySide (provided by Krita's environment) [20]
*   **AI Generation Backend (Local Focus):**
    *   **Primary Targets:** ComfyUI API, AUTOMATIC1111 Web UI API.
    *   **Requires:** User must have one of these backends installed and running locally with appropriate models (SDXL, ControlNet, IP-Adapter) loaded.
*   **Core AI Model:** Stable Diffusion **SDXL** (via the local backend).
*   **Consistency Methods (Local & Open Source):**
    *   **IP-Adapter (Face, SDXL version):** Using reference image(s) passed via the backend's API [7, 10, 37].
    *   **ControlNet (SDXL versions):** Primarily OpenPose (for pose), potentially Reference (for style) or Depth/Canny/Lineart (for structure), using reference images/data passed via API [2, 9, 21, 23].
    *   **LoRA Loading:** Instructing the backend API to load and apply user-specified `.safetensors` LoRA files [5, 14, 41].
*   **Libraries:** `requests` (for API communication), potentially Pillow/PIL for basic image handling within the plugin if needed.

## 6. Consistency Strategy

Leverage the strengths of local, open-source tools, allowing combination for best results:

1.  **Identity (Face/Character):**
    *   **Primary:** Use **IP-Adapter (Face)** with one or more user-provided reference images of the character's face. Plugin sends image(s) and parameters (weight) via API [10, 37].
    *   **Secondary/High-Fidelity:** Allow user to specify a **LoRA** file trained for the specific character. Plugin sends LoRA name and weight via API [5, 14].
2.  **Pose/Structure:**
    *   Use **ControlNet (OpenPose, Depth, Canny, etc.)** with a user-provided reference image (e.g., a simple sketch of the pose, a previous panel's render). Plugin sends reference image and ControlNet model choice/parameters via API [9, 21].
3.  **Workflow:** The plugin UI will allow users to select their desired combination (e.g., IP-Adapter for face + ControlNet OpenPose for pose + Base Prompt), configuring parameters for each, and sending the combined request to the local backend API.

## 7. User Experience (UX)

*   **Simplicity:** Abstract the complexity of backend API calls. UI focuses on selecting references (images, files), typing prompts, and adjusting key parameters (weights, strength).
*   **Configuration:** Initial setup screen to configure the local backend API endpoint (e.g., `http://127.0.0.1:7860` or `http://127.0.0.1:8188`).
*   **Feedback:** Clear indicators of connection status to the local backend, generation progress, errors.
*   **Integration:** Native Krita Docker, respecting Krita's UI conventions.

## 8. Potential Challenges

*   **User Setup:** Users *must* install and run the local backend (ComfyUI/A1111) and download required models (SDXL, ControlNet, IP-Adapter). This is a significant technical hurdle compared to cloud APIs, but aligns with the open-source/local focus. Clear documentation is crucial.
*   **Backend API Differences:** ComfyUI and A1111 APIs work differently; supporting both may require separate logic or choosing one primary target initially. ComfyUI's graph-based API might map better to complex workflows.
*   **Performance:** Generation speed depends entirely on the user's hardware (GPU VRAM).
*   **Error Handling:** Need robust handling for backend connection failures, missing models on the backend, invalid user inputs, etc.
*   **Dependency Management:** Keeping plugin dependencies minimal or ensuring they are correctly packaged/installed.

## 9. Success Metrics

*   User adoption within the Krita community preferring local generation.
*   Positive feedback on the ease of using IP-Adapter/ControlNet/LoRA through the plugin compared to manual backend usage.
*   Demonstrable consistency improvements in user-generated storyboards.
*   Plugin stability and clear error reporting regarding the local backend connection.
*   Community contributions (since it's open source).