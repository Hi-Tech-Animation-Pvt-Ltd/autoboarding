# Krita Storyboard AI Plugin - Initial Tasks

This document outlines the initial tasks to kickstart the development of the Krita Storyboard AI Plugin, focusing on **local, open-source AI integration**.

## Phase 1: Research & Setup (1-2 weeks)

*   [ ] **Task 1.1:** Deep dive into Krita Python Plugin Development (same as before).
    *   [ ] Understand plugin structure (`.desktop` files, `__init__.py`) [20, 42].
    *   [ ] Explore Krita API (`libkis`) for document/layer manipulation, UI creation (Dockers), and accessing selections [20, 42, 44].
    *   [ ] Set up a Krita plugin development environment [44, 45].
    *   [ ] Experiment with the Scripter tool [20, 40].
*   [ ] **Task 1.2:** Local Backend API Research & Setup:
    *   [ ] **Install and configure** a local backend: **ComfyUI** and/or **AUTOMATIC1111**. Include necessary models: SDXL base, VAE, **IP-Adapter (Face)** models, **ControlNet (OpenPose, etc.)** models for SDXL.
    *   [ ] **Study the API documentation** for the chosen backend(s) (ComfyUI API, A1111 API). Focus on endpoints for:
        *   Text-to-image generation with SDXL.
        *   Loading/applying **ControlNets** with reference images and parameters.
        *   Loading/applying **IP-Adapters** with reference images and parameters (often integrated via ControlNet or specific nodes/extensions).
        *   Loading/applying **LoRAs** with specified weights.
        *   Checking server status / available models.
    *   [ ] **Test API calls** outside of Krita (using `requests` or `curl`) to generate images using IP-Adapter, ControlNet, and LoRAs via the local backend API. Confirm parameter passing works as expected.
*   [ ] **Task 1.3:** Refine Consistency Strategy via Manual Tests:
    *   [ ] Manually use the chosen local backend UI (ComfyUI/A1111) to test workflows combining **IP-Adapter (Face) + ControlNet (OpenPose)**.
    *   [ ] Test workflows combining **LoRA + ControlNet (OpenPose)**.
    *   [ ] Document the exact parameters, model names, and reference image types that yield good results. This informs the plugin's default settings and API calls.
*   [ ] **Task 1.4:** Setup Project Infrastructure (same as before).
    *   [ ] Create Git repository.
    *   [ ] Define basic project structure.
    *   [ ] Set up virtual environment (`requests`, etc.).

## Phase 2: Core Plugin Structure & Basic Local Generation (2-3 weeks)

*   [ ] **Task 2.1:** Create Basic Krita Plugin Skeleton (same as before).
    *   [ ] Set up directory structure, `.desktop`, `__init__.py`.
    *   [ ] Implement basic plugin loading/unloading.
    *   [ ] Create a simple Krita Docker UI placeholder (PyQt/PySide).
*   [ ] **Task 2.2:** Implement Local Backend API Communication:
    *   [ ] Add a configuration setting within the plugin/Krita for the user to input their local backend API URL (e.g., `http://127.0.0.1:8188/prompt` for ComfyUI).
    *   [ ] Write Python functions to construct the JSON payload/request for the **local backend API** based on user input (prompt, basic parameters).
    *   [ ] Implement functions to send requests (`requests.post`) to the configured local API endpoint.
    *   [ ] Handle API responses (parsing JSON, extracting image data often base64 encoded).
    *   [ ] Implement robust error handling for connection errors (`ConnectionRefusedError`), timeouts, and API errors returned by the backend. Provide clear feedback to the user (e.g., "Could not connect to backend at [URL]. Is it running?").
*   [ ] **Task 2.3:** Implement Basic Text-to-Image UI & Logic:
    *   [ ] Add UI elements: Text input for prompt, "Generate" button, status/feedback area.
    *   [ ] Connect UI: Trigger API call on button press.
    *   [ ] Display loading/progress indicators. Display errors clearly.
*   [ ] **Task 2.4:** Implement Basic Image Insertion (same as before).
    *   [ ] Use Krita API to decode image data (likely base64).
    *   [ ] Create a new layer.
    *   [ ] Place the generated image onto the new layer.

## Phase 3: Consistency Feature Implementation (via Local API) (3-4 weeks)

*   [ ] **Task 3.1:** Implement IP-Adapter (Face) Workflow via API:
    *   [ ] Add UI: Button to select reference image file(s) for IP-Adapter. Display thumbnail(s). Slider/input for IP-Adapter weight.
    *   [ ] Read image file(s), likely encode as base64.
    *   [ ] Modify API call construction logic to include IP-Adapter parameters and reference image data, formatted correctly for the **target backend's API** (e.g., within ControlNet unit parameters if using A1111, or specific nodes/inputs for ComfyUI).
*   [ ] **Task 3.2:** Implement ControlNet (Pose/Structure) Workflow via API:
    *   [ ] Add UI: Button to select reference image file for ControlNet (e.g., pose image). Dropdown to select ControlNet type (OpenPose, Depth, etc.). Sliders/inputs for weight/strength.
    *   [ ] Read/encode reference image.
    *   [ ] Modify API call construction to include ControlNet parameters, model selection, and reference image data, formatted correctly for the **target backend's API**.
*   [ ] **Task 3.3:** Implement LoRA Loading Workflow via API:
    *   [ ] Add UI: Button to select LoRA file (`.safetensors`). Input for LoRA weight.
    *   [ ] Modify API call construction to include LoRA name(s) and weight(s) as expected by the **target backend's API**. (Note: LoRA file itself isn't sent, just its name assuming it's accessible by the backend).
*   [ ] **Task 3.4:** Refine UI for Consistency Options:
    *   [ ] Organize UI logically (Prompt, Identity [IP-Adapter/LoRA], Structure [ControlNet], Settings).
    *   [ ] Allow enabling/disabling different consistency methods and combining them (e.g., IP-Adapter + ControlNet).

## Phase 4: Initial Testing & Refinement (1-2 weeks)

*   [ ] **Task 4.1:** Internal Testing (Focus on Local Backend Interaction):
    *   [ ] Test core generation with various prompts via the plugin -> local backend -> Krita layer.
    *   [ ] Test IP-Adapter consistency workflow.
    *   [ ] Test ControlNet consistency workflow (various types like OpenPose).
    *   [ ] Test LoRA loading workflow.
    *   [ ] Test combinations (IP-Adapter + ControlNet).
    *   [ ] Test error handling extensively (backend down, wrong URL, missing models on backend, invalid image references).
*   [ ] **Task 4.2:** Code Cleanup & Documentation:
    *   [ ] Refactor API communication logic.
    *   [ ] Add comments, docstrings.
    *   [ ] **Crucially:** Write initial README detailing:
        *   Plugin purpose.
        *   **Required local backend setup** (e.g., "Requires ComfyUI running with SDXL, IP-Adapter models, ControlNet models installed"). Link to relevant backend/model resources.
        *   How to configure the backend URL in the plugin.
        *   Basic usage instructions.

## Next Steps (Beyond Initial Tasks)

*   User feedback collection (especially regarding setup complexity and workflow).
*   Supporting both ComfyUI and A1111 APIs.
*   More sophisticated UI (previewing ControlNet interpretations?).
*   Handling image-to-image pipelines.
*   Packaging/distribution for Krita.