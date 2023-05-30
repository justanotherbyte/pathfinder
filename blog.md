Pathfinder is a visually-blind rover, meaning it does not have the ability to see proper images, but can produce sound-waves to detect where it is (like dolphins). I've taken up this project as a challenge to my problem solving and mathematical skills. My goal with this project is to create a small robot that can navigate small areas with nothing but distance measurements, as well as being able to map small areas (obviously at a fixed y-level).

## Hardware

Let's talk a bit about the hardware. The hardware that I specifically used for this project includes:

- [Trilobot Base Kit](https://shop.pimoroni.com/products/trilobot?variant=39594077093971)
- Raspberry Pi 3/4 (I don't remember which one)
- 22.5w battery pack (portable power source)

## Library Choices

### Python

| Library | Usage 
| ------- | -------
| [redis](https://pypi.org/project/redis/) | Connect to the redis instance for communication
| [gpiozero](https://pypi.org/project/gpiozero/) | Interact with GPIO pins easily
| [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) | Use just for the distance sensor

### Rust

| Crate | Usage
| ----- | ------
| [redis](https://crates.io/crates/redis) | Connect to the redis instance for communication
| [device_query](https://crates.io/crates/device_query) | Listen for keyboard events on my laptop
| [egui](https://crates.io/crates/egui) | Quick UI creation