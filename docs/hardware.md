# SCOUT Hardware Notes

## Initial runtime target

- POCO X3
- Android + Termux
- ARM64 / aarch64 environment
- camera, microphone, speaker, display, Wi-Fi, Bluetooth

## M0 status

M0 does not implement hardware integration. Hardware requirements are documented here so that later milestones can be added with clear compatibility targets.

## Future platform path

- Android/Termux for phone runtime and local inference UI
- ESP32 for hardware control layer only after safety boundaries are established
- Potential future SBC or ROS 2 computer for power users or more advanced robotics work

## Safety rule

The LLM must never directly control motors, servos, or safety-critical hardware. The hardware boundary should be enforced in the software architecture and in the command-validation layer.
