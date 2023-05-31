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


## The Motor Protocol

### What is the Motor Protocol?

The Motor Protocol is a basic protocol I developed for Pathfinder to speak with any controller. My initial idea was to have Pathfinder just receive controller events (i.e Key Down, Key Up, Joystick Move). However, I realized pretty quickly that this wouldn't be the best way to approach the problem, since this would require Pathfinder to have explicit support for every controller type I wanted to use. 

Instead I came to the conclusion that I should have the controller (whether thats a keyboard, joystick etc) conduct its own logic to construct motor instructions, which are instructions telling which motor to do what. This idea seemed like a good solution due to the fact that it wouldn't require Pathfinder explicitly supporting every controller type, and instead would need the controllers to do their own work to figure out what motor they wanted to control and what it should do.

### Structure of the Motor Protocol

The structure of the Motor Protocol is fairly basic. Here I've represented it as Rust structs & enums as it would be within the code.

```rust
#[derive(Serialize)]
pub enum Motor {
    Left,
    Right,
    Both
}

#[derive(Serialize)]
pub enum Direction {
    Forward,
    Backward
}

#[derive(Serialize)]
pub struct MotorInstruction {
    pub motor: Motor,
    pub direction: Direction,
    pub speed: f32 // 0 -> 1
}
```

See, fairly simple right? Here's a quick example in case you don't understand. Let's move the rover forward with this payload:

```rust
let payload = MotorInstruction {
    motor: Motor::Both,
    direction: Motor::Forward,
    speed: 1.0
}
```